#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -f "$ROOT_DIR/.env" ]]; then
  # shellcheck disable=SC1090
  set -a
  source "$ROOT_DIR/.env"
  set +a
fi

if [[ -z "${BILLING_DB_DSN:-}" ]]; then
  echo "BILLING_DB_DSN is not set. Define it in .env or your shell environment." >&2
  exit 1
fi

echo "Initializing schema on database from BILLING_DB_DSN..."
psql "$BILLING_DB_DSN" -v ON_ERROR_STOP=1 -f "$ROOT_DIR/db/schema.sql"
echo "Schema initialization complete."
