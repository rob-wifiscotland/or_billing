# Billing Parser Design Solution

## Objective
Design and build a Python/Flask billing data parser to process Openreach custom pipe-delimited `.dat` files, identify product and section types, map fields using product-specific schemas, and persist parsed records into the target Postgres tables using Psycopg3 with connection pooling.

## Scope and Requirements
- Use Python and Flask for the main application structure.
- Scan an input folder for `.dat` files.
- Parse each file sequentially.
- Move successfully processed files to a completed folder.
- Move failed files to a failed folder.
- Use Psycopg3 only (no ORM).
- Implement database connection pooling.
- Follow PEP8.
- Document all functions with Google-style docstrings.

## File Processing Workflow
1. Discover `.dat` files in configured input directory.
2. For each file:
   - Open and parse line-by-line.
   - Determine section type from first column.
   - Determine product type from header/product identifiers.
   - Route row to the relevant section parser.
   - Convert/validate field values using product+section mapping.
   - Persist data in a single file-level database transaction.
3. On full success:
   - Commit transaction.
   - Move file to `processed/` directory.
4. On failure:
   - Roll back transaction.
   - Record structured error details.
   - Move file to `failed/` directory.

## Section Handling
Each row is classified by first column into one of:
- Header
- Product Charges
- Event Charges
- Adjustments
- Bill Summary

The parser supports rows up to 60 columns and applies product-specific column mappings to determine which fields are used by each section.

## Product and Schema Mapping Strategy
- Maintain a mapping registry keyed by product type.
- For each product, define section-level mapping rules:
  - Source column index
  - Target database field name
  - Converter/type function
  - Optionality/validation rules
- Mapping definitions are derived from `spec/billing_guide.doc`.
- Unknown/unsupported products are rejected with explicit error logging.

## Database Persistence Design
### Technology
- `psycopg` + `psycopg_pool.ConnectionPool`
- Parameterized SQL statements only
- No ORM

### Target Tables
- `openreach.billing_invoices`
- `openreach.billing_product_charges`
- `openreach.billing_event_charges`
- `openreach.billing_adjustments`
- `openreach.billing_rcs_adjustments`
- `openreach.billing_circuit_summary`

### Relational Strategy
- Insert invoice/header record first to obtain `invoice_id`.
- Insert all section rows with `invoice_id` as foreign key.
- Keep one transaction per file for consistency.

## Data Conversion and Validation
Implement reusable converters for:
- `date`
- `timestamp`
- `numeric(10,2)`
- `smallint`
- `boolean`

Rules:
- Empty strings map to `NULL`.
- Invalid values raise typed parse/validation errors.
- Required invoice fields must be present before child inserts.

## Error Handling and Logging
- Structured error format includes:
  - filename
  - line number
  - section
  - product
  - failure reason
- Log per-file processing summary:
  - section counts
  - insert counts
  - elapsed time
  - final status

## Application Structure (Proposed)
- `app/__init__.py` (Flask app factory)
- `app/config.py` (paths, DB DSN, pool settings)
- `app/file_processor.py` (directory scan + file lifecycle)
- `app/parser/core.py` (row routing, section dispatch)
- `app/parser/mappings.py` (product/section mapping registry)
- `app/parser/converters.py` (typed conversion helpers)
- `app/db/pool.py` (connection pool setup)
- `app/db/repositories/*.py` (table-specific insert operations)
- `run_parser.py` (entrypoint for batch execution)

## Testing Approach
- Unit tests:
  - section routing
  - type conversion
  - mapping resolution
- Integration tests:
  - transaction rollback behavior
  - foreign key linkage via `invoice_id`
  - insert correctness for each section
- Golden-file tests:
  - sample `.dat` files with expected parsed outcomes

## Delivery Phases
1. **Phase 1**
   - Project scaffold
   - Input file scanning
   - Core parser routing
   - Invoice/Product/Event persistence
2. **Phase 2**
   - Adjustments/RCS adjustments/Circuit summary support
   - Full converter and validator coverage
3. **Phase 3**
   - Logging hardening
   - Dry-run option
   - Full test coverage and edge-case handling

## Initial Assumptions
1. Execution model is scheduled batch run (e.g., cron/systemd), not continuous daemon watch.
2. `spec/billing_guide.doc` is the authoritative schema source.
3. Failed files are moved to `failed/` and not retried automatically during the same run.
