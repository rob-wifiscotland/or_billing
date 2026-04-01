"""Database pool helpers."""

from __future__ import annotations

from psycopg_pool import ConnectionPool


def create_pool(dsn: str, min_size: int, max_size: int) -> ConnectionPool:
    """Create a Psycopg connection pool.

    Args:
        dsn: PostgreSQL DSN.
        min_size: Minimum pool size.
        max_size: Maximum pool size.

    Returns:
        ConnectionPool: Open connection pool.

    Raises:
        ValueError: If DSN is empty.
    """
    if not dsn:
        raise ValueError("BILLING_DB_DSN is required")

    return ConnectionPool(conninfo=dsn, min_size=min_size, max_size=max_size, open=True)
