"""Batch runner for Openreach billing parser."""

from __future__ import annotations

import argparse
import logging

from app import create_app
from app.db.pool import create_pool
from app.file_processor import BillingFileProcessor
from app.logging_config import configure_logging


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed args namespace.
    """
    parser = argparse.ArgumentParser(description="Run billing parser over pending .dat files")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse files and log findings without writing to database or moving files",
    )
    return parser.parse_args()


def main() -> int:
    """Execute parser run.

    Returns:
        int: Process exit code.
    """
    args = parse_args()
    app = create_app()
    configure_logging(
        app.config["LOG_LEVEL"],
        app.config["LOG_FILE"],
    )

    if args.dry_run:
        from app.parser.core import parse_dat_file

        input_dir = app.config["INPUT_DIR"]
        files = sorted(input_dir.glob("*.dat"))
        failures = 0
        for file_path in files:
            try:
                parsed = parse_dat_file(
                    file_path,
                    account_product_map=app.config["PRODUCT_ACCOUNT_MAP"],
                )
                logging.info(
                    "Dry run %s: product=%s product_rows=%d event_rows=%d adjustments=%d rcs_adjustments=%d circuit_summaries=%d skipped=%s",
                    file_path.name,
                    parsed.product_type,
                    len(parsed.product_charges),
                    len(parsed.event_charges),
                    len(parsed.adjustments),
                    len(parsed.rcs_adjustments),
                    len(parsed.circuit_summaries),
                    dict(parsed.skipped_sections),
                )
            except Exception as exc:
                failures += 1
                logging.exception("Dry run failed for %s: %s", file_path.name, exc)
        logging.info("Dry run complete. files=%d failures=%d", len(files), failures)
        return 0 if failures == 0 else 1

    pool = create_pool(
        dsn=app.config["DB_DSN"],
        min_size=app.config["DB_MIN_SIZE"],
        max_size=app.config["DB_MAX_SIZE"],
    )

    processor = BillingFileProcessor(
        db_pool=pool,
        input_dir=app.config["INPUT_DIR"],
        processed_dir=app.config["PROCESSED_DIR"],
        failed_dir=app.config["FAILED_DIR"],
        account_product_map=app.config["PRODUCT_ACCOUNT_MAP"],
    )

    try:
        result = processor.process_pending_files()
        logging.info("Run complete: processed=%d failed=%d", result.processed, result.failed)
        return 0 if result.failed == 0 else 1
    finally:
        pool.close()


if __name__ == "__main__":
    raise SystemExit(main())
