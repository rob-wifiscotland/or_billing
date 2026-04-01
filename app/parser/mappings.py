"""Field mapping helpers for Phase 1 parser support."""

from __future__ import annotations

from typing import Any

from app.parser.converters import (
    clean_text,
    pence_to_gbp,
    to_date,
    to_decimal,
    to_int,
    to_smallint,
    to_timestamp,
)


def get_field(fields: list[str], *indexes: int) -> str | None:
    """Return the first non-empty field value from candidate indexes.

    Args:
        fields: Split row fields.
        *indexes: Candidate positions to evaluate in order.

    Returns:
        str | None: First non-empty value if present.
    """
    for index in indexes:
        if index < len(fields):
            value = clean_text(fields[index])
            if value is not None:
                return value
    return None


def get_smallint_field(fields: list[str], *indexes: int) -> int | None:
    """Return first valid PostgreSQL smallint value from candidate indexes.

    Args:
        fields: Split row fields.
        *indexes: Candidate positions to evaluate.

    Returns:
        int | None: Parsed smallint-compatible value.
    """
    for index in indexes:
        if index >= len(fields):
            continue
        try:
            value = to_smallint(fields[index])
        except ValueError:
            continue
        if value is None:
            continue
        if -32768 <= value <= 32767:
            return value
    return None


def detect_product_type(
    header_row: list[str],
    account_product_map: dict[str, str] | None = None,
) -> str:
    """Determine product type from header-level values.

    Args:
        header_row: Parsed header row fields.

    Returns:
        str: Product type label.
    """
    bill_title = (get_field(header_row, 11) or "").lower()
    customer_ref = (get_field(header_row, 1) or "").lower()
    account_ref = get_field(header_row, 2)

    if account_product_map and account_ref:
        mapped = account_product_map.get(account_ref)
        if mapped:
            return mapped

    if "single order generic ethernet access" in bill_title or customer_ref.startswith("sogea"):
        return "SOGEA"
    if "generic ethernet access" in bill_title or customer_ref.startswith("gea"):
        return "NGA"
    if "passive" in bill_title or "pole" in bill_title:
        return "PIA"
    if "llu" in bill_title or customer_ref.startswith("llu"):
        return "LLU"
    if customer_ref.startswith("e/"):
        return "ETHERNET"
    return "UNKNOWN"


def map_bill_type(header_row: list[str]) -> str | None:
    """Map header bill type code to bill type label.

    Args:
        header_row: Parsed header row fields.

    Returns:
        str | None: Mapped bill type label.
    """
    code = get_field(header_row, 10, 9)
    mapping = {
        "1": "Periodic",
        "2": "Interim",
        "5": "VAT Credit",
    }
    if code is None:
        return None
    return mapping.get(code)


def map_invoice_header(header_row: list[str]) -> dict[str, Any]:
    """Map header row fields to invoice columns.

    Args:
        header_row: Parsed header row.

    Returns:
        dict[str, Any]: Invoice header payload.
    """
    return {
        "customer_reference": get_field(header_row, 1),
        "account_reference": get_field(header_row, 2),
        "invoice_reference": get_field(header_row, 3),
        "bill_tax_date": to_date(get_field(header_row, 4)),
        "bill_type": map_bill_type(header_row),
        "bill_title": get_field(header_row, 11),
    }


def map_bill_summary(summary_row: list[str]) -> dict[str, Any]:
    """Map bill summary row fields to invoice summary columns.

    Args:
        summary_row: Parsed bill summary row.

    Returns:
        dict[str, Any]: Bill summary payload.
    """
    return {
        "net_total": pence_to_gbp(get_field(summary_row, 1)),
        "total_vat": pence_to_gbp(get_field(summary_row, 2)),
        "non_vat_total": pence_to_gbp(get_field(summary_row, 3)),
        "invoice_total": pence_to_gbp(get_field(summary_row, 4)),
        "one_off_charges": pence_to_gbp(get_field(summary_row, 5)),
        "periodic_charges": pence_to_gbp(get_field(summary_row, 6)),
        "event_charges": pence_to_gbp(get_field(summary_row, 7)),
        "non_product_event_charges": pence_to_gbp(get_field(summary_row, 8)),
        "total_usage_charges": pence_to_gbp(get_field(summary_row, 9)),
        "total_adjustments": pence_to_gbp(get_field(summary_row, 10)),
    }


def map_product_charge(row: list[str]) -> dict[str, Any]:
    """Map product charge row fields to product charge columns.

    Args:
        row: Parsed product row fields.

    Returns:
        dict[str, Any]: Product charge payload.
    """
    return {
        "product_description": get_field(row, 1),
        "tariff_name": get_field(row, 2),
        "product_label": get_field(row, 3),
        "charge_description": get_field(row, 4),
        "start_date": to_date(get_field(row, 6)),
        "end_date": to_date(get_field(row, 7)),
        "address_line_1": get_field(row, 8),
        "postcode": get_field(row, 9),
        "or_order_number": get_field(row, 10),
        "quantity": get_smallint_field(row, 14, 13),
        "units": get_field(row, 14, 15),
        "unit_rate": pence_to_gbp(get_field(row, 15, 16)),
        "price": pence_to_gbp(get_field(row, 16, 17)),
        "vat_status": to_smallint(get_field(row, 17, 18)),
        "service_id": get_field(row, 21, 22, 23, 24),
        "price_list_reference": get_field(row, 34),
        "price_list_description": get_field(row, 35),
        "unique_price_code": get_field(row, 59),
    }


def map_event_charge(row: list[str], product_type: str = "UNKNOWN") -> dict[str, Any]:
    """Map event row fields to event charge columns.

    Args:
        row: Parsed event row fields.

    Returns:
        dict[str, Any]: Event charge payload.
    """
    if product_type == "SOGEA":
        event_source = get_field(row, 5)
        event_description = get_field(row, 4)
    else:
        event_source = get_field(row, 4)
        event_description = get_field(row, 5)

    return {
        "event_source": event_source,
        "event_description": event_description,
        "charge_reason": get_field(row, 25),
        "event_date": to_date(get_field(row, 6)),
        "end_date": to_date(get_field(row, 7)),
        "address_line_1": get_field(row, 8),
        "postcode": get_field(row, 9),
        "or_order_number": get_field(row, 11, 10),
        "quantity": get_smallint_field(row, 13, 14),
        "event_cost": pence_to_gbp(get_field(row, 16, 15)),
        "vat_status": to_smallint(get_field(row, 17)),
        "service_id": get_field(row, 24, 3),
        "price_list_reference": get_field(row, 34),
        "price_list_description": get_field(row, 35),
        "product_set": get_field(row, 46),
        "unique_price_code": get_field(row, 59),
    }


def map_adjustment(row: list[str]) -> dict[str, Any]:
    """Map adjustment row fields to adjustment columns.

    Args:
        row: Parsed adjustment row fields.

    Returns:
        dict[str, Any]: Adjustment payload.
    """
    return {
        "adjustment_name": get_field(row, 1),
        "product_tariff_name": get_field(row, 2),
        "adjustment_free_text_field": get_field(row, 3),
        "charge_description_type": get_field(row, 4),
        "charge_reason": get_field(row, 5),
        "adjustment_date": to_date(get_field(row, 6)),
        "end_date": to_date(get_field(row, 7)),
        "address_line_1": get_field(row, 8),
        "postcode": get_field(row, 9),
        "css_seibel_job_number": get_field(row, 10),
        "sp_order_fault_number_1": get_field(row, 11),
        "sp_order_fault_number_2": get_field(row, 12),
        "quantity": get_smallint_field(row, 13, 14),
        "units": get_field(row, 14, 15),
        "unit_rate": pence_to_gbp(get_field(row, 15, 16)),
        "net_value": pence_to_gbp(get_field(row, 16, 17)),
        "vat_status": to_smallint(get_field(row, 17, 18)),
        "css_account_number": get_field(row, 19),
        "product_type": get_field(row, 20),
        "or_service_id": get_field(row, 21),
        "circuit_id": get_field(row, 22),
        "mdf_site": get_field(row, 23),
        "room_id": get_field(row, 24),
        "service_id": get_field(row, 25),
        "event_class": get_field(row, 26),
        "event_name": get_field(row, 27),
        "cbuk_reference_number": get_field(row, 28),
        "cli": get_field(row, 29),
        "mac_code": get_field(row, 30),
        "trc_start_date_time": to_timestamp(get_field(row, 31)),
        "clear_code": get_field(row, 32),
        "trc_description_code": get_field(row, 33),
        "price_list_reference": get_field(row, 34),
        "price_list_description": get_field(row, 35),
    }


def map_circuit_summary(row: list[str]) -> dict[str, Any]:
    """Map circuit summary row fields to circuit summary columns.

    Args:
        row: Parsed circuit summary row fields.

    Returns:
        dict[str, Any]: Circuit summary payload.
    """
    return {
        "circuit_number": get_field(row, 1),
        "a_end_1141_code": get_field(row, 2),
        "b_end_1141_code": get_field(row, 3),
        "customer_order_number": get_field(row, 4),
        "distance": to_int(get_field(row, 5)),
        "provide_order_date": to_date(get_field(row, 6)),
        "cease_date": to_date(get_field(row, 7)),
        "connection_charge": pence_to_gbp(get_field(row, 8)),
        "bpr_days": to_smallint(get_field(row, 9)),
        "bpr_rental": to_smallint(get_field(row, 11)),
        "rental_charge": pence_to_gbp(get_field(row, 10)),
        "credit_rental": pence_to_gbp(get_field(row, 12)),
        "total_rental": pence_to_gbp(get_field(row, 13)),
        "other_charges": pence_to_gbp(get_field(row, 14)),
        "total_circuit_charges": pence_to_gbp(get_field(row, 15)),
    }
