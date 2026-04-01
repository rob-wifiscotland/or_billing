"""Conversion helpers for parser field values."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Optional


DATE_FORMAT = "%Y%m%d"


def clean_text(value: str | None) -> str | None:
    """Normalize string values from input rows.

    Args:
        value: Raw field value.

    Returns:
        str | None: Trimmed string or ``None`` for blank input.
    """
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


def to_date(value: str | None) -> date | None:
    """Convert a YYYYMMDD value to date.

    Args:
        value: Raw date field.

    Returns:
        date | None: Parsed date or ``None`` if blank.
    """
    value = clean_text(value)
    if value is None:
        return None
    if len(value) >= 8 and value[:8].isdigit():
        return datetime.strptime(value[:8], DATE_FORMAT).date()
    try:
        return datetime.fromisoformat(value).date()
    except ValueError as exc:
        raise ValueError(f"Invalid date value: {value}") from exc


def to_decimal(value: str | None) -> Decimal | None:
    """Convert string value to Decimal.

    Args:
        value: Raw numeric field.

    Returns:
        Decimal | None: Parsed decimal value or ``None``.
    """
    value = clean_text(value)
    if value is None:
        return None
    try:
        return Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"Invalid decimal value: {value}") from exc


def pence_to_gbp(value: str | None) -> Decimal | None:
    """Convert pence integer string to GBP decimal value.

    Example: ``12284`` -> ``Decimal('122.84')``.

    Args:
        value: Raw value in pence.

    Returns:
        Decimal | None: GBP decimal amount or ``None``.
    """
    amount = to_decimal(value)
    if amount is None:
        return None
    return amount / Decimal("100")


def to_smallint(value: str | None) -> int | None:
    """Convert string value to int.

    Args:
        value: Raw integer field.

    Returns:
        int | None: Parsed integer value or ``None``.
    """
    value = clean_text(value)
    if value is None:
        return None
    return int(value)


def to_int(value: str | None) -> int | None:
    """Convert string value to int.

    Args:
        value: Raw integer field.

    Returns:
        int | None: Parsed integer value or ``None``.
    """
    value = clean_text(value)
    if value is None:
        return None
    return int(value)


def to_bool(value: str | None) -> Optional[bool]:
    """Convert common truthy/falsey values to bool.

    Args:
        value: Raw boolean field.

    Returns:
        bool | None: Boolean value or ``None`` if blank/unknown.
    """
    value = clean_text(value)
    if value is None:
        return None

    lowered = value.lower()
    if lowered in {"true", "t", "1", "y", "yes"}:
        return True
    if lowered in {"false", "f", "0", "n", "no"}:
        return False
    return None


def to_timestamp(value: str | None) -> datetime | None:
    """Convert value to datetime when possible.

    Args:
        value: Raw timestamp field.

    Returns:
        datetime | None: Parsed datetime or ``None``.
    """
    value = clean_text(value)
    if value is None:
        return None

    normalized = value.replace("T", " ")
    if len(normalized) == 8 and normalized.isdigit():
        return datetime.strptime(normalized, DATE_FORMAT)
    if len(normalized) >= 14 and normalized[:14].isdigit():
        return datetime.strptime(normalized[:14], "%Y%m%d%H%M%S")
    if len(normalized) >= 17 and normalized[:8].isdigit():
        try:
            return datetime.strptime(normalized[:19], "%Y%m%d %H:%M:%S")
        except ValueError:
            pass
    try:
        return datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"Invalid timestamp value: {value}") from exc
