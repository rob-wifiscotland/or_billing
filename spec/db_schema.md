                                                           Table "openreach.billing_adjustments"
           Column           |            Type             | Collation | Nullable |      Default       | Storage  | Compression | Stats target | Description
----------------------------+-----------------------------+-----------+----------+--------------------+----------+-------------+--------------+-------------
 adjustment_id              | uuid                        |           | not null | uuid_generate_v4() | plain    |             |              |
 invoice_id                 | uuid                        |           |          |                    | plain    |             |              |
 adjustment_name            | character varying(40)       |           |          |                    | extended |             |              |
 product_tariff_name        | character varying(40)       |           |          |                    | extended |             |              |
 adjustment_free_text_field | character varying(255)      |           |          |                    | extended |             |              |
 charge_description_type    | character varying(20)       |           |          |                    | extended |             |              |
 charge_reason              | character varying(40)       |           |          |                    | extended |             |              |
 adjustment_date            | date                        |           |          |                    | plain    |             |              |
 end_date                   | date                        |           |          |                    | plain    |             |              |
 address_line_1             | character varying(80)       |           |          |                    | extended |             |              |
 postcode                   | character varying(16)       |           |          |                    | extended |             |              |
 css_seibel_job_number      | character varying(20)       |           |          |                    | extended |             |              |
 sp_order_fault_number_1    | character varying(20)       |           |          |                    | extended |             |              |
 sp_order_fault_number_2    | character varying(20)       |           |          |                    | extended |             |              |
 quantity                   | smallint                    |           |          |                    | plain    |             |              |
 units                      | character varying(40)       |           |          |                    | extended |             |              |
 unit_rate                  | numeric(10,2)               |           |          |                    | main     |             |              |
 net_value                  | numeric(10,2)               |           |          |                    | main     |             |              |
 vat_status                 | smallint                    |           |          |                    | plain    |             |              |
 css_account_number         | character varying(20)       |           |          |                    | extended |             |              |
 product_type               | character varying(20)       |           |          |                    | extended |             |              |
 or_service_id              | character varying(20)       |           |          |                    | extended |             |              |
 circuit_id                 | character varying(20)       |           |          |                    | extended |             |              |
 mdf_site                   | character varying(20)       |           |          |                    | extended |             |              |
 room_id                    | character varying(20)       |           |          |                    | extended |             |              |
 service_id                 | character varying(40)       |           |          |                    | extended |             |              |
 event_class                | character varying(20)       |           |          |                    | extended |             |              |
 event_name                 | character varying(20)       |           |          |                    | extended |             |              |
 cbuk_reference_number      | character varying(20)       |           |          |                    | extended |             |              |
 cli                        | character varying(20)       |           |          |                    | extended |             |              |
 mac_code                   | character varying(20)       |           |          |                    | extended |             |              |
 trc_start_date_time        | timestamp without time zone |           |          |                    | plain    |             |              |
 clear_code                 | character varying(20)       |           |          |                    | extended |             |              |
 trc_description_code       | character varying(20)       |           |          |                    | extended |             |              |
 price_list_reference       | character varying(256)      |           |          |                    | extended |             |              |
 price_list_description     | character varying(256)      |           |          |                    | extended |             |              |
Indexes:
    "adjustments_pkey" PRIMARY KEY, btree (adjustment_id)
Foreign-key constraints:
    "adjustments_invoice_id_fkey" FOREIGN KEY (invoice_id) REFERENCES billing_invoices(invoice_id)
Access method: heap


postgis_db=# \d+ openreach.billing_circuit_summary
                                                    Table "openreach.billing_circuit_summary"
        Column         |         Type          | Collation | Nullable |      Default       | Storage  | Compression | Stats target | Description
-----------------------+-----------------------+-----------+----------+--------------------+----------+-------------+--------------+-------------
 circuit_summary_id    | uuid                  |           | not null | uuid_generate_v4() | plain    |             |              |
 invoice_id            | uuid                  |           |          |                    | plain    |             |              |
 circuit_number        | character varying(20) |           |          |                    | extended |             |              |
 a_end_1141_code       | character varying(20) |           |          |                    | extended |             |              |
 b_end_1141_code       | character varying(20) |           |          |                    | extended |             |              |
 customer_order_number | character varying(20) |           |          |                    | extended |             |              |
 distance              | bigint                |           |          |                    | plain    |             |              |
 provide_order_date    | date                  |           |          |                    | plain    |             |              |
 cease_date            | date                  |           |          |                    | plain    |             |              |
 connection_charge     | numeric(10,2)         |           |          |                    | main     |             |              |
 bpr_days              | smallint              |           |          |                    | plain    |             |              |
 bpr_rental            | smallint              |           |          |                    | plain    |             |              |
 rental_charge         | numeric(10,2)         |           |          |                    | main     |             |              |
 credit_rental         | numeric(10,2)         |           |          |                    | main     |             |              |
 total_rental          | numeric(10,2)         |           |          |                    | main     |             |              |
 other_charges         | numeric(10,2)         |           |          |                    | main     |             |              |
 total_circuit_charges | numeric(10,2)         |           |          |                    | main     |             |              |
Indexes:
    "circuit_summary_pkey" PRIMARY KEY, btree (circuit_summary_id)
Foreign-key constraints:
    "circuit_summary_invoice_id_fkey" FOREIGN KEY (invoice_id) REFERENCES billing_invoices(invoice_id)
Access method: heap


postgis_db=# \d+ openreach.billing_event_charges
                                                         Table "openreach.billing_event_charges"
            Column             |          Type          | Collation | Nullable |      Default       | Storage  | Compression | Stats target | Description
-------------------------------+------------------------+-----------+----------+--------------------+----------+-------------+--------------+-------------
 event_id                      | uuid                   |           | not null | uuid_generate_v4() | plain    |             |              |
 invoice_id                    | uuid                   |           |          |                    | plain    |             |              |
 event_source                  | character varying(40)  |           |          |                    | extended |             |              |
 event_description             | character varying(40)  |           |          |                    | extended |             |              |
 charge_reason                 | character varying(40)  |           |          |                    | extended |             |              |
 event_date                    | date                   |           |          |                    | plain    |             |              |
 end_date                      | date                   |           |          |                    | plain    |             |              |
 address_line_1                | character varying(80)  |           |          |                    | extended |             |              |
 postcode                      | character varying(16)  |           |          |                    | extended |             |              |
 or_order_number               | character varying(80)  |           |          |                    | extended |             |              |
 quantity                      | smallint               |           |          |                    | plain    |             |              |
 event_cost                    | numeric(10,2)          |           |          |                    | main     |             |              |
 vat_status                    | smallint               |           |          |                    | plain    |             |              |
 service_id                    | character varying(40)  |           |          |                    | extended |             |              |
 price_list_reference          | character varying(256) |           |          |                    | extended |             |              |
 price_list_description        | character varying(256) |           |          |                    | extended |             |              |
 product_set                   | character varying(40)  |           |          |                    | extended |             |              |
 unique_price_code             | character varying(60)  |           |          |                    | extended |             |              |
 event_class                   | character varying(80)  |           |          |                    | extended |             |              |
 customer_event_seibel_ref     | character varying(40)  |           |          |                    | extended |             |              |
 exchange_name                 | character varying(40)  |           |          |                    | extended |             |              |
 associated_product_service_id | character varying(40)  |           |          |                    | extended |             |              |
 trc_chargeable_hours          | smallint               |           |          |                    | plain    |             |              |
 event_end_date                | date                   |           |          |                    | plain    |             |              |
 attribute1_name               | character varying(40)  |           |          |                    | extended |             |              |
 attribute1_value              | character varying(40)  |           |          |                    | extended |             |              |
 attribute2_name               | character varying(40)  |           |          |                    | extended |             |              |
 attribute2_value              | character varying(40)  |           |          |                    | extended |             |              |
 css_seibel_job_number         | character varying(20)  |           |          |                    | extended |             |              |
 mdf_site_id                   | character varying(40)  |           |          |                    | extended |             |              |
Indexes:
    "events_pkey" PRIMARY KEY, btree (event_id)
Foreign-key constraints:
    "events_invoices_fkey" FOREIGN KEY (invoice_id) REFERENCES billing_invoices(invoice_id)
Access method: heap


postgis_db=# \d+ openreach.billing_invoices
                                                         Table "openreach.billing_invoices"
          Column           |         Type          | Collation | Nullable |      Default       | Storage  | Compression | Stats target | Description
---------------------------+-----------------------+-----------+----------+--------------------+----------+-------------+--------------+-------------
 invoice_id                | uuid                  |           | not null | uuid_generate_v4() | plain    |             |              |
 customer_reference        | character varying(20) |           |          |                    | extended |             |              |
 account_reference         | character varying(20) |           |          |                    | extended |             |              |
 invoice_reference         | character varying(20) |           |          |                    | extended |             |              |
 bill_tax_date             | date                  |           |          |                    | plain    |             |              |
 bill_type                 | character varying(9)  |           |          |                    | extended |             |              |
 bill_title                | character varying(80) |           |          |                    | extended |             |              |
 net_total                 | numeric(10,2)         |           |          |                    | main     |             |              |
 total_vat                 | numeric(10,2)         |           |          |                    | main     |             |              |
 non_vat_total             | numeric(10,2)         |           |          |                    | main     |             |              |
 invoice_total             | numeric(10,2)         |           |          |                    | main     |             |              |
 one_off_charges           | numeric(10,2)         |           |          |                    | main     |             |              |
 periodic_charges          | numeric(10,2)         |           |          |                    | main     |             |              |
 event_charges             | numeric(10,2)         |           |          |                    | main     |             |              |
 non_product_event_charges | numeric(10,2)         |           |          |                    | main     |             |              |
 total_usage_charges       | numeric(10,2)         |           |          |                    | main     |             |              |
 total_adjustments         | numeric(10,2)         |           |          |                    | main     |             |              |
Indexes:
    "billing_invoices_pkey" PRIMARY KEY, btree (invoice_id)
Check constraints:
    "billing_invoices_bill_type_check" CHECK (bill_type::text = ANY (ARRAY['Periodic'::text, 'Interim'::text, 'Initiation'::text, 'Termination'::text, 'VAT Credit'::text, 'Budget Cente
r Report'::text, 'Post Termination'::text, 'Suspension'::text]))
Referenced by:
    TABLE "billing_adjustments" CONSTRAINT "adjustments_invoice_id_fkey" FOREIGN KEY (invoice_id) REFERENCES billing_invoices(invoice_id)
    TABLE "billing_circuit_summary" CONSTRAINT "circuit_summary_invoice_id_fkey" FOREIGN KEY (invoice_id) REFERENCES billing_invoices(invoice_id)
    TABLE "billing_event_charges" CONSTRAINT "events_invoices_fkey" FOREIGN KEY (invoice_id) REFERENCES billing_invoices(invoice_id)
    TABLE "billing_product_charges" CONSTRAINT "product_charges_invoices_fkey" FOREIGN KEY (invoice_id) REFERENCES billing_invoices(invoice_id)
    TABLE "billing_rcs_adjustments" CONSTRAINT "rcs_adjustments_invoice_id_fkey" FOREIGN KEY (invoice_id) REFERENCES billing_invoices(invoice_id)
Access method: heap


postgis_db=# \d+ openreach.billing_product_charges
                                                         Table "openreach.billing_product_charges"
             Column              |          Type          | Collation | Nullable |      Default       | Storage  | Compression | Stats target | Description
---------------------------------+------------------------+-----------+----------+--------------------+----------+-------------+--------------+-------------
 product_charge_id               | uuid                   |           | not null | uuid_generate_v4() | plain    |             |              |
 invoice_id                      | uuid                   |           |          |                    | plain    |             |              |
 product_description             | character varying      |           |          |                    | extended |             |              |
 tariff_name                     | character varying      |           |          |                    | extended |             |              |
 product_label                   | character varying(80)  |           |          |                    | extended |             |              |
 charge_description              | character varying      |           |          |                    | extended |             |              |
 start_date                      | date                   |           |          |                    | plain    |             |              |
 end_date                        | date                   |           |          |                    | plain    |             |              |
 address_line_1                  | character varying(80)  |           |          |                    | extended |             |              |
 postcode                        | character varying(16)  |           |          |                    | extended |             |              |
 or_order_number                 | character varying(80)  |           |          |                    | extended |             |              |
 quantity                        | smallint               |           |          |                    | plain    |             |              |
 unit_rate                       | numeric(10,2)          |           |          |                    | main     |             |              |
 price                           | numeric(10,2)          |           |          |                    | main     |             |              |
 vat_status                      | smallint               |           |          |                    | plain    |             |              |
 service_id                      | character varying      |           |          |                    | extended |             |              |
 price_list_reference            | character varying(256) |           |          |                    | extended |             |              |
 price_list_description          | character varying(256) |           |          |                    | extended |             |              |
 transmission_medium             | character varying      |           |          |                    | extended |             |              |
 upstream_bandwidth              | smallint               |           |          |                    | plain    |             |              |
 downstream_bandwidth            | smallint               |           |          |                    | plain    |             |              |
 tier_values                     | character varying      |           |          |                    | extended |             |              |
 unique_price_code               | character varying(60)  |           |          |                    | extended |             |              |
 htt_bill_backup_message         | character varying(40)  |           |          |                    | extended |             |              |
 site_sub_prem_name              | character varying(40)  |           |          |                    | extended |             |              |
 site_prem_name                  | character varying(40)  |           |          |                    | extended |             |              |
 site_thoroughfare_number        | character varying(40)  |           |          |                    | extended |             |              |
 site_thoroughfare_name          | character varying(40)  |           |          |                    | extended |             |              |
 site_locality_name              | character varying(40)  |           |          |                    | extended |             |              |
 site_post_town_name             | character varying(40)  |           |          |                    | extended |             |              |
 site_county_name                | character varying(40)  |           |          |                    | extended |             |              |
 zone_description                | character varying(40)  |           |          |                    | extended |             |              |
 exchange_1141_code              | character varying(40)  |           |          |                    | extended |             |              |
 exchange_id                     | character varying(40)  |           |          |                    | extended |             |              |
 exchange_name                   | character varying(40)  |           |          |                    | extended |             |              |
 floor                           | character varying(40)  |           |          |                    | extended |             |              |
 room                            | character varying(40)  |           |          |                    | extended |             |              |
 location                        | character varying(40)  |           |          |                    | extended |             |              |
 zone_name                       | character varying(40)  |           |          |                    | extended |             |              |
 circuit_m140_code               | character varying(40)  |           |          |                    | extended |             |              |
 associated_product_service_id   | character varying(40)  |           |          |                    | extended |             |              |
 associated_product_service_id_2 | character varying(40)  |           |          |                    | extended |             |              |
 associated_product_service_id_3 | character varying(40)  |           |          |                    | extended |             |              |
 resilience_option_indicator     | character varying(40)  |           |          |                    | extended |             |              |
 circuit_classification          | character varying(40)  |           |          |                    | extended |             |              |
 enable_syncronisation           | boolean                |           |          |                    | plain    |             |              |
 channel_reference               | character varying(40)  |           |          |                    | extended |             |              |
 attribute1_name                 | character varying(40)  |           |          |                    | extended |             |              |
 attribute1_value                | character varying(40)  |           |          |                    | extended |             |              |
 attribute2_name                 | character varying(40)  |           |          |                    | extended |             |              |
 attribute2_value                | character varying(40)  |           |          |                    | extended |             |              |
 circuit_id                      | character varying(40)  |           |          |                    | extended |             |              |
 mdf_site                        | character varying(40)  |           |          |                    | extended |             |              |
 room_id                         | character varying(40)  |           |          |                    | extended |             |              |
 units                           | character varying(20)  |           |          |                    | extended |             |              |
 css_seibel_job_number           | character varying(20)  |           |          |                    | extended |             |              |
Indexes:
    "product_charges_pkey" PRIMARY KEY, btree (product_charge_id)
Foreign-key constraints:
    "product_charges_invoices_fkey" FOREIGN KEY (invoice_id) REFERENCES billing_invoices(invoice_id)
Access method: heap


postgis_db=# \d+ openreach.billing_rcs_adjustments
                                                         Table "openreach.billing_rcs_adjustments"
           Column           |            Type             | Collation | Nullable |      Default       | Storage  | Compression | Stats target | Description
----------------------------+-----------------------------+-----------+----------+--------------------+----------+-------------+--------------+-------------
 rcs_adjustment_id          | uuid                        |           | not null | uuid_generate_v4() | plain    |             |              |
 invoice_id                 | uuid                        |           |          |                    | plain    |             |              |
 adjustment_name            | character varying(40)       |           |          |                    | extended |             |              |
 product_tariff_name        | character varying(40)       |           |          |                    | extended |             |              |
 adjustment_free_text_field | character varying(255)      |           |          |                    | extended |             |              |
 charge_description_type    | character varying(20)       |           |          |                    | extended |             |              |
 charge_reason              | character varying(40)       |           |          |                    | extended |             |              |
 adjustment_date            | date                        |           |          |                    | plain    |             |              |
 end_date                   | date                        |           |          |                    | plain    |             |              |
 address_line_1             | character varying(80)       |           |          |                    | extended |             |              |
 postcode                   | character varying(16)       |           |          |                    | extended |             |              |
 css_seibel_job_number      | character varying(20)       |           |          |                    | extended |             |              |
 sp_order_fault_number_1    | character varying(20)       |           |          |                    | extended |             |              |
 sp_order_fault_number_2    | character varying(20)       |           |          |                    | extended |             |              |
 quantity                   | smallint                    |           |          |                    | plain    |             |              |
 units                      | character varying(40)       |           |          |                    | extended |             |              |
 unit_rate                  | numeric(10,2)               |           |          |                    | main     |             |              |
 net_value                  | numeric(10,2)               |           |          |                    | main     |             |              |
 vat_status                 | smallint                    |           |          |                    | plain    |             |              |
 css_account_number         | character varying(20)       |           |          |                    | extended |             |              |
 product_type               | character varying(20)       |           |          |                    | extended |             |              |
 or_service_id              | character varying(20)       |           |          |                    | extended |             |              |
 circuit_id                 | character varying(20)       |           |          |                    | extended |             |              |
 mdf_site                   | character varying(20)       |           |          |                    | extended |             |              |
 room_id                    | character varying(20)       |           |          |                    | extended |             |              |
 service_id                 | character varying(40)       |           |          |                    | extended |             |              |
 event_class                | character varying(20)       |           |          |                    | extended |             |              |
 event_name                 | character varying(20)       |           |          |                    | extended |             |              |
 cbuk_reference_number      | character varying(20)       |           |          |                    | extended |             |              |
 cli                        | character varying(20)       |           |          |                    | extended |             |              |
 mac_code                   | character varying(20)       |           |          |                    | extended |             |              |
 trc_start_date_time        | timestamp without time zone |           |          |                    | plain    |             |              |
 clear_code                 | character varying(20)       |           |          |                    | extended |             |              |
 trc_description_code       | character varying(20)       |           |          |                    | extended |             |              |
 price_list_reference       | character varying(256)      |           |          |                    | extended |             |              |
 price_list_description     | character varying(256)      |           |          |                    | extended |             |              |
Indexes:
    "rcs_adjustments_pkey" PRIMARY KEY, btree (rcs_adjustment_id)
Foreign-key constraints:
    "rcs_adjustments_invoice_id_fkey" FOREIGN KEY (invoice_id) REFERENCES billing_invoices(invoice_id)
Access method: heap