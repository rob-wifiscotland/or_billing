"""Application configuration for billing parser."""

from __future__ import annotations

import os
from pathlib import Path


def load_dotenv(dotenv_path: Path) -> None:
    """Load environment variables from a `.env` file if present.

    Args:
        dotenv_path: Absolute path to `.env` file.
    """
    if not dotenv_path.exists():
        return

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        os.environ.setdefault(key, value)


def _split_accounts(value: str) -> list[str]:
    """Split account list text into normalized account IDs.

    Args:
        value: Comma-separated account values.

    Returns:
        list[str]: Parsed account IDs.
    """
    return [part.strip() for part in value.split(",") if part.strip()]


def load_product_account_map() -> dict[str, str]:
    """Build account-reference to product map from environment.

    Supports both:
    - Named keys in `.env` (e.g. ``GEA=GM123...,GM456...``)
    - Prefixed keys (e.g. ``BILLING_ACCOUNT_SOGEA=...``)

    Returns:
        dict[str, str]: Mapping of account reference -> product type.
    """
    named_keys = {
        "DARK_FIBRE": "DARK_FIBRE",
        "ETHERNET": "ETHERNET",
        "GEA": "NGA",
        "LLU_CABLELINK": "LLU",
        "LLU_UNBUNDLING": "LLU",
        "ACCESS_LOCATE": "LLU",
        "PIA": "PIA",
        "SOGEA": "SOGEA",
        "WLR": "WLR",
    }
    account_map: dict[str, str] = {}

    for key, product in named_keys.items():
        raw_value = os.getenv(key, "")
        for account in _split_accounts(raw_value):
            account_map[account] = product

    prefix_map = {
        "BILLING_ACCOUNT_": "",
        "PRODUCT_ACCOUNT_": "",
    }
    normalize_product = {
        "GEA": "NGA",
        "LLU_CABLELINK": "LLU",
        "LLU_UNBUNDLING": "LLU",
        "ACCESS_LOCATE": "LLU",
        "DARK_FIBRE": "DARK_FIBRE",
    }
    for key, value in os.environ.items():
        for prefix in prefix_map:
            if not key.startswith(prefix):
                continue
            suffix = key[len(prefix) :].strip()
            if not suffix:
                continue
            product = normalize_product.get(suffix, suffix)
            for account in _split_accounts(value):
                account_map[account] = product

    return account_map


class Config:
    """Runtime configuration values loaded from environment variables."""

    BASE_DIR = Path(__file__).resolve().parent.parent

    load_dotenv(BASE_DIR / ".env")

    INPUT_DIR = Path(os.getenv("BILLING_INPUT_DIR", BASE_DIR / "incoming"))
    PROCESSED_DIR = Path(os.getenv("BILLING_PROCESSED_DIR", BASE_DIR / "processed"))
    FAILED_DIR = Path(os.getenv("BILLING_FAILED_DIR", BASE_DIR / "failed"))

    DB_DSN = os.getenv("BILLING_DB_DSN", "")
    DB_MIN_SIZE = int(os.getenv("BILLING_DB_MIN_POOL", "1"))
    DB_MAX_SIZE = int(os.getenv("BILLING_DB_MAX_POOL", "5"))

    LOG_LEVEL = os.getenv("BILLING_LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("BILLING_LOG_FILE", str(BASE_DIR / "logs" / "billing_parser.log"))
    PRODUCT_ACCOUNT_MAP = load_product_account_map()
