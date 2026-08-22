"""Structured logging setup with contextvars, JSON formatting, and correlation ID support."""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict

import structlog
from structlog.contextvars import (
    bind_contextvars,
    clear_contextvars,
    get_contextvars,
    merge_contextvars,
    unbind_contextvars,
)

# Standard logging configuration
logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.INFO,
)

# Structlog processors pipeline
_shared_processors = [
    merge_contextvars,
    structlog.stdlib.add_log_level,
    structlog.stdlib.add_logger_name,
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.dict_tracebacks,
    structlog.processors.StackInfoRenderer(),
]

structlog.configure(
    processors=_shared_processors + [
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Root application logger
logger = structlog.get_logger("adpilot")


def get_logger(name: str = "adpilot") -> structlog.stdlib.BoundLogger:
    """Return a contextualized structlog logger instance."""
    return structlog.get_logger(name)


class JSONFormatter(logging.Formatter):
    """Formats standard Python logging.LogRecord to JSON format."""

    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
        }

        # Include any contextvars attached
        context = get_contextvars()
        if context:
            log_data.update(context)

        return json.dumps(log_data)


__all__ = [
    "logger",
    "get_logger",
    "JSONFormatter",
    "bind_contextvars",
    "clear_contextvars",
    "get_contextvars",
    "unbind_contextvars",
]
