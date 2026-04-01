"""Repository functions for Phase 1 billing inserts."""

from __future__ import annotations

from typing import Any

from psycopg import Connection


def insert_invoice(conn: Connection, payload: dict[str, Any]) -> str:
    """Insert billing invoice and return invoice ID.

    Args:
        conn: Active database connection.
        payload: Invoice payload.

    Returns:
        str: Inserted invoice UUID.
    """
    sql = """
        INSERT INTO openreach.billing_invoices (
            customer_reference,
            account_reference,
            invoice_reference,
            bill_tax_date,
            bill_type,
            bill_title,
            net_total,
            total_vat,
            non_vat_total,
            invoice_total,
            one_off_charges,
            periodic_charges,
            event_charges,
            non_product_event_charges,
            total_usage_charges,
            total_adjustments
        ) VALUES (
            %(customer_reference)s,
            %(account_reference)s,
            %(invoice_reference)s,
            %(bill_tax_date)s,
            %(bill_type)s,
            %(bill_title)s,
            %(net_total)s,
            %(total_vat)s,
            %(non_vat_total)s,
            %(invoice_total)s,
            %(one_off_charges)s,
            %(periodic_charges)s,
            %(event_charges)s,
            %(non_product_event_charges)s,
            %(total_usage_charges)s,
            %(total_adjustments)s
        )
        RETURNING invoice_id
    """
    with conn.cursor() as cur:
        cur.execute(sql, payload)
        row = cur.fetchone()
    return str(row[0])


def insert_product_charge(conn: Connection, invoice_id: str, payload: dict[str, Any]) -> None:
    """Insert a product charge row.

    Args:
        conn: Active database connection.
        invoice_id: Parent invoice UUID.
        payload: Product row payload.
    """
    sql = """
        INSERT INTO openreach.billing_product_charges (
            invoice_id,
            product_description,
            tariff_name,
            product_label,
            charge_description,
            start_date,
            end_date,
            address_line_1,
            postcode,
            or_order_number,
            quantity,
            units,
            unit_rate,
            price,
            vat_status,
            service_id,
            price_list_reference,
            price_list_description,
            unique_price_code
        ) VALUES (
            %(invoice_id)s,
            %(product_description)s,
            %(tariff_name)s,
            %(product_label)s,
            %(charge_description)s,
            %(start_date)s,
            %(end_date)s,
            %(address_line_1)s,
            %(postcode)s,
            %(or_order_number)s,
            %(quantity)s,
            %(units)s,
            %(unit_rate)s,
            %(price)s,
            %(vat_status)s,
            %(service_id)s,
            %(price_list_reference)s,
            %(price_list_description)s,
            %(unique_price_code)s
        )
    """
    insert_payload = {"invoice_id": invoice_id, **payload}
    with conn.cursor() as cur:
        cur.execute(sql, insert_payload)


def insert_event_charge(conn: Connection, invoice_id: str, payload: dict[str, Any]) -> None:
    """Insert an event charge row.

    Args:
        conn: Active database connection.
        invoice_id: Parent invoice UUID.
        payload: Event row payload.
    """
    sql = """
        INSERT INTO openreach.billing_event_charges (
            invoice_id,
            event_source,
            event_description,
            charge_reason,
            event_date,
            end_date,
            address_line_1,
            postcode,
            or_order_number,
            quantity,
            event_cost,
            vat_status,
            service_id,
            price_list_reference,
            price_list_description,
            product_set,
            unique_price_code
        ) VALUES (
            %(invoice_id)s,
            %(event_source)s,
            %(event_description)s,
            %(charge_reason)s,
            %(event_date)s,
            %(end_date)s,
            %(address_line_1)s,
            %(postcode)s,
            %(or_order_number)s,
            %(quantity)s,
            %(event_cost)s,
            %(vat_status)s,
            %(service_id)s,
            %(price_list_reference)s,
            %(price_list_description)s,
            %(product_set)s,
            %(unique_price_code)s
        )
    """
    insert_payload = {"invoice_id": invoice_id, **payload}
    with conn.cursor() as cur:
        cur.execute(sql, insert_payload)


def insert_adjustment(
    conn: Connection,
    invoice_id: str,
    payload: dict[str, Any],
    table_name: str = "openreach.billing_adjustments",
) -> None:
    """Insert an adjustment row.

    Args:
        conn: Active database connection.
        invoice_id: Parent invoice UUID.
        payload: Adjustment row payload.
        table_name: Target adjustment table.
    """
    allowed_tables = {
        "openreach.billing_adjustments",
        "openreach.billing_rcs_adjustments",
    }
    if table_name not in allowed_tables:
        raise ValueError(f"Unsupported adjustments table: {table_name}")

    sql = f"""
        INSERT INTO {table_name} (
            invoice_id,
            adjustment_name,
            product_tariff_name,
            adjustment_free_text_field,
            charge_description_type,
            charge_reason,
            adjustment_date,
            end_date,
            address_line_1,
            postcode,
            css_seibel_job_number,
            sp_order_fault_number_1,
            sp_order_fault_number_2,
            quantity,
            units,
            unit_rate,
            net_value,
            vat_status,
            css_account_number,
            product_type,
            or_service_id,
            circuit_id,
            mdf_site,
            room_id,
            service_id,
            event_class,
            event_name,
            cbuk_reference_number,
            cli,
            mac_code,
            trc_start_date_time,
            clear_code,
            trc_description_code,
            price_list_reference,
            price_list_description
        ) VALUES (
            %(invoice_id)s,
            %(adjustment_name)s,
            %(product_tariff_name)s,
            %(adjustment_free_text_field)s,
            %(charge_description_type)s,
            %(charge_reason)s,
            %(adjustment_date)s,
            %(end_date)s,
            %(address_line_1)s,
            %(postcode)s,
            %(css_seibel_job_number)s,
            %(sp_order_fault_number_1)s,
            %(sp_order_fault_number_2)s,
            %(quantity)s,
            %(units)s,
            %(unit_rate)s,
            %(net_value)s,
            %(vat_status)s,
            %(css_account_number)s,
            %(product_type)s,
            %(or_service_id)s,
            %(circuit_id)s,
            %(mdf_site)s,
            %(room_id)s,
            %(service_id)s,
            %(event_class)s,
            %(event_name)s,
            %(cbuk_reference_number)s,
            %(cli)s,
            %(mac_code)s,
            %(trc_start_date_time)s,
            %(clear_code)s,
            %(trc_description_code)s,
            %(price_list_reference)s,
            %(price_list_description)s
        )
    """
    insert_payload = {"invoice_id": invoice_id, **payload}
    with conn.cursor() as cur:
        cur.execute(sql, insert_payload)


def insert_circuit_summary(conn: Connection, invoice_id: str, payload: dict[str, Any]) -> None:
    """Insert a circuit summary row.

    Args:
        conn: Active database connection.
        invoice_id: Parent invoice UUID.
        payload: Circuit summary row payload.
    """
    sql = """
        INSERT INTO openreach.billing_circuit_summary (
            invoice_id,
            circuit_number,
            a_end_1141_code,
            b_end_1141_code,
            customer_order_number,
            distance,
            provide_order_date,
            cease_date,
            connection_charge,
            bpr_days,
            bpr_rental,
            rental_charge,
            credit_rental,
            total_rental,
            other_charges,
            total_circuit_charges
        ) VALUES (
            %(invoice_id)s,
            %(circuit_number)s,
            %(a_end_1141_code)s,
            %(b_end_1141_code)s,
            %(customer_order_number)s,
            %(distance)s,
            %(provide_order_date)s,
            %(cease_date)s,
            %(connection_charge)s,
            %(bpr_days)s,
            %(bpr_rental)s,
            %(rental_charge)s,
            %(credit_rental)s,
            %(total_rental)s,
            %(other_charges)s,
            %(total_circuit_charges)s
        )
    """
    insert_payload = {"invoice_id": invoice_id, **payload}
    with conn.cursor() as cur:
        cur.execute(sql, insert_payload)
