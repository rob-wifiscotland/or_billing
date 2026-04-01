"""File-processing orchestration for billing parser."""

from __future__ import annotations

import logging
import shutil
from dataclasses import dataclass
from pathlib import Path

from psycopg_pool import ConnectionPool

from app.db.repositories import (
    insert_adjustment,
    insert_circuit_summary,
    insert_event_charge,
    insert_invoice,
    insert_product_charge,
)
from app.parser.core import parse_dat_file
from app.parser.errors import ParseError


LOGGER = logging.getLogger(__name__)


@dataclass
class ProcessingResult:
    """Aggregated file processing results."""

    processed: int = 0
    failed: int = 0


def _merge_invoice_payload(header_payload: dict, summary_payload: dict) -> dict:
    """Merge header and summary values into one invoice payload.

    Args:
        header_payload: Header mapped fields.
        summary_payload: Bill summary mapped fields.

    Returns:
        dict: Combined invoice payload.
    """
    return {**header_payload, **summary_payload}


class BillingFileProcessor:
    """Process pending billing files and persist parsed rows."""

    def __init__(
        self,
        db_pool: ConnectionPool,
        input_dir: Path,
        processed_dir: Path,
        failed_dir: Path,
        account_product_map: dict[str, str] | None = None,
    ) -> None:
        """Initialize file processor.

        Args:
            db_pool: Open Psycopg connection pool.
            input_dir: Directory containing source `.dat` files.
            processed_dir: Destination directory for successful files.
            failed_dir: Destination directory for failed files.
            account_product_map: Optional account-reference to product mapping.
        """
        self.db_pool = db_pool
        self.input_dir = input_dir
        self.processed_dir = processed_dir
        self.failed_dir = failed_dir
        self.account_product_map = account_product_map or {}

    def process_pending_files(self) -> ProcessingResult:
        """Parse and persist all pending `.dat` files.

        Returns:
            ProcessingResult: Counts of processed and failed files.
        """
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.failed_dir.mkdir(parents=True, exist_ok=True)

        result = ProcessingResult()
        for file_path in sorted(self.input_dir.glob("*.dat")):
            if self._process_single_file(file_path):
                result.processed += 1
            else:
                result.failed += 1
        return result

    def _process_single_file(self, file_path: Path) -> bool:
        """Process a single billing file.

        Args:
            file_path: Source file path.

        Returns:
            bool: ``True`` on success, otherwise ``False``.
        """
        LOGGER.info("Processing file: %s", file_path.name)
        try:
            parsed = parse_dat_file(
                file_path,
                account_product_map=self.account_product_map,
            )
            with self.db_pool.connection() as conn:
                with conn.transaction():
                    invoice_payload = _merge_invoice_payload(parsed.header, parsed.bill_summary)
                    invoice_id = insert_invoice(conn, invoice_payload)

                    for payload in parsed.product_charges:
                        insert_product_charge(conn, invoice_id, payload)

                    for payload in parsed.event_charges:
                        insert_event_charge(conn, invoice_id, payload)

                    for payload in parsed.adjustments:
                        insert_adjustment(conn, invoice_id, payload)

                    for payload in parsed.rcs_adjustments:
                        insert_adjustment(
                            conn,
                            invoice_id,
                            payload,
                            table_name="openreach.billing_rcs_adjustments",
                        )

                    for payload in parsed.circuit_summaries:
                        insert_circuit_summary(conn, invoice_id, payload)

            destination = self.processed_dir / file_path.name
            shutil.move(file_path, destination)
            LOGGER.info(
                "Processed %s (product=%s, product_rows=%d, event_rows=%d, adjustments=%d, rcs_adjustments=%d, circuit_summaries=%d, skipped=%s)",
                file_path.name,
                parsed.product_type,
                len(parsed.product_charges),
                len(parsed.event_charges),
                len(parsed.adjustments),
                len(parsed.rcs_adjustments),
                len(parsed.circuit_summaries),
                dict(parsed.skipped_sections),
            )
            return True
        except (ParseError, ValueError, RuntimeError) as exc:
            LOGGER.exception("Parse/validation error in %s: %s", file_path.name, exc)
        except Exception as exc:  # pragma: no cover
            LOGGER.exception("Unhandled error in %s: %s", file_path.name, exc)

        destination = self.failed_dir / file_path.name
        shutil.move(file_path, destination)
        LOGGER.info("Moved failed file to %s", destination)
        return False
