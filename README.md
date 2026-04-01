# Openreach Billing Parser

Python/Flask-based billing parser for Openreach generic bill backup files (`.dat`).

The parser:
- scans an input folder for `.dat` files,
- identifies product type from `CUSTOMERRECORD` header data,
- parses supported sections,
- inserts data into PostgreSQL with Psycopg3 (no ORM),
- moves files to `processed/` on success or `failed/` on failure.

## Supported Sections
- `CUSTOMERRECORD` -> `openreach.billing_invoices`
- `PRODUCTCHARGE` -> `openreach.billing_product_charges`
- `EVENT` -> `openreach.billing_event_charges`
- `ADJUSTMENT` / `ADJUSTMENTS` -> `openreach.billing_adjustments`
- `RCSADJUSTMENT` -> `openreach.billing_rcs_adjustments`
- `CIRCUITSUMMARY` -> `openreach.billing_circuit_summary`
- `BILLSUMMARYRECORD` -> invoice totals in `openreach.billing_invoices`

## Prerequisites
- Python `3.10+`
- PostgreSQL `13+`
- `psql` CLI available on path (for schema bootstrap)

## Quick Start
1. Clone the repo.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Configure `.env`.
5. Initialize DB schema.
6. Put billing files into `incoming/`.
7. Run parser.

### 1) Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Configure Environment
Create `.env` from the template:
```bash
cp .env.example .env
```

Set required values:
- `BILLING_DB_DSN`
- `BILLING_INPUT_DIR`
- `BILLING_PROCESSED_DIR`
- `BILLING_FAILED_DIR`

Optional but recommended:
- `BILLING_LOG_LEVEL` (`DEBUG`, `INFO`, `WARNING`, `ERROR`)
- `BILLING_LOG_FILE` (path to rolling log file)

Product account mapping values (`CUSTOMERRECORD` column 3):
- `DARK_FIBRE`, `ETHERNET`, `GEA`, `LLU_CABLELINK`, `LLU_UNBUNDLING`, `ACCESS_LOCATE`, `PIA`, `SOGEA`, `WLR`

These mappings are used first for product detection. If a mapping is not found, parser falls back to header-title heuristics.

### 3) Initialize Database Schema
Use the provided schema bootstrap script:
```bash
./scripts/init_db.sh
```

Equivalent manual command:
```bash
psql "$BILLING_DB_DSN" -v ON_ERROR_STOP=1 -f db/schema.sql
```

## Running the Parser
### Standard ingest
```bash
python3 run_parser.py
```

### Dry-run (parse only, no DB writes, no file moves)
```bash
python3 run_parser.py --dry-run
```

## Logging
Logging configuration is environment-driven:
- `BILLING_LOG_LEVEL` controls verbosity.
- `BILLING_LOG_FILE` enables rotating file logs (5MB, 5 backups).

Logs are always written to stdout and optionally to the configured log file.

## Repository Layout
- `app/` parser and DB code
- `db/schema.sql` schema bootstrap SQL
- `scripts/init_db.sh` schema init helper
- `incoming/` files waiting to ingest
- `processed/` successful files
- `failed/` failed files
- `spec/` source guides and sample files

## Notes
- Monetary values in input rows are interpreted as pence and stored as GBP.
- `bill_type` is mapped from header code (`1=Periodic`, `2=Interim`, `5=VAT Credit`).
- SOGEA EVENT records map `event_description` from column 4.

## Troubleshooting
- `permission denied for table ...`
  - grant `INSERT/SELECT/UPDATE/DELETE` on `openreach.*` tables for your DB role.
- `BILLING_DB_DSN is required`
  - set `BILLING_DB_DSN` in `.env`.
- Files moving to `failed/`
  - check parser logs for section/column/value errors.
