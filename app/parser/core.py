"""Core parser entrypoints and section routing."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from app.parser.errors import ParseError
from app.parser.mappings import (
    detect_product_type,
    map_adjustment,
    map_bill_summary,
    map_circuit_summary,
    map_event_charge,
    map_invoice_header,
    map_product_charge,
)


@dataclass
class ParsedBillingFile:
    """Container for parsed billing file content."""

    source_file: Path
    product_type: str = "UNKNOWN"
    header: dict = field(default_factory=dict)
    bill_summary: dict = field(default_factory=dict)
    product_charges: list[dict] = field(default_factory=list)
    event_charges: list[dict] = field(default_factory=list)
    adjustments: list[dict] = field(default_factory=list)
    rcs_adjustments: list[dict] = field(default_factory=list)
    circuit_summaries: list[dict] = field(default_factory=list)
    skipped_sections: Counter = field(default_factory=Counter)


def _read_lines(file_path: Path) -> list[str]:
    """Read file with UTF-8 fallback to latin-1.

    Args:
        file_path: Source file path.

    Returns:
        list[str]: File lines.
    """
    for encoding in ("utf-8", "latin-1"):
        try:
            return file_path.read_text(encoding=encoding).splitlines()
        except UnicodeDecodeError:
            continue
    return file_path.read_text(encoding="latin-1", errors="replace").splitlines()


def _split_row(raw_line: str) -> list[str]:
    """Split a raw input row into fields.

    Args:
        raw_line: Single raw line from input file.

    Returns:
        list[str]: Row fields.
    """
    return raw_line.rstrip("\n").split("|")


def parse_dat_file(
    file_path: Path,
    account_product_map: dict[str, str] | None = None,
) -> ParsedBillingFile:
    """Parse a billing `.dat` file into section payloads.

    Args:
        file_path: Input file path.

    Returns:
        ParsedBillingFile: Parsed representation.

    Raises:
        ParseError: If required sections are missing.
    """
    parsed = ParsedBillingFile(source_file=file_path)

    for line_number, raw_line in enumerate(_read_lines(file_path), start=1):
        if not raw_line.strip():
            continue

        row = _split_row(raw_line)
        section = row[0].strip().upper() if row else ""

        if section == "CUSTOMERRECORD":
            parsed.header = map_invoice_header(row)
            parsed.product_type = detect_product_type(
                row,
                account_product_map=account_product_map,
            )
        elif section == "PRODUCTCHARGE":
            parsed.product_charges.append(map_product_charge(row))
        elif section == "EVENT":
            parsed.event_charges.append(map_event_charge(row, product_type=parsed.product_type))
        elif section in {"ADJUSTMENT", "ADJUSTMENTS"}:
            parsed.adjustments.append(map_adjustment(row))
        elif section == "RCSADJUSTMENT":
            parsed.rcs_adjustments.append(map_adjustment(row))
        elif section == "CIRCUITSUMMARY":
            parsed.circuit_summaries.append(map_circuit_summary(row))
        elif section == "BILLSUMMARYRECORD":
            parsed.bill_summary = map_bill_summary(row)
        else:
            parsed.skipped_sections[section or "UNKNOWN"] += 1

        if line_number == 1 and section != "CUSTOMERRECORD":
            raise ParseError("First row must be CUSTOMERRECORD")

    if not parsed.header:
        raise ParseError("Missing CUSTOMERRECORD section")

    return parsed
