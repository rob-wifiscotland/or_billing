"""Logging configuration helpers."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


DEFAULT_LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"


def _parse_log_level(level_name: str) -> int:
    """Parse a log level name into a logging module integer level.

    Args:
        level_name: Environment-configured level name.

    Returns:
        int: Logging level.
    """
    return getattr(logging, (level_name or "INFO").upper(), logging.INFO)


def configure_logging(level_name: str, log_file: str | None = None) -> None:
    """Configure application logging handlers.

    Args:
        level_name: Root logging level name.
        log_file: Optional log file path.
    """
    level = _parse_log_level(level_name)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Avoid duplicate handlers when reconfigured during tests/manual reruns.
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(logging.Formatter(DEFAULT_LOG_FORMAT))
    root_logger.addHandler(stream_handler)

    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(DEFAULT_LOG_FORMAT))
        root_logger.addHandler(file_handler)

    logging.getLogger(__name__).debug("Logging configured level=%s file=%s", level_name, log_file)
