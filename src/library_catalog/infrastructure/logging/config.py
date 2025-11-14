import json
import logging
import sys
from logging import LogRecord
from os import getenv
from typing import Any, ClassVar


# ANSI color codes
class Colors:
    """ANSI color codes for terminal output."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Colors
    GRAY = "\033[90m"
    BLUE = "\033[34m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    MAGENTA = "\033[35m"

    # Bright colors
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_RED = "\033[91m"


class ColoredFormatter(logging.Formatter):
    """Formatter with colored output and level at the start of line."""

    LEVEL_COLORS: ClassVar[dict[str, str]] = {
        "DEBUG": Colors.GRAY,
        "INFO": Colors.GREEN,
        "WARNING": Colors.YELLOW,
        "ERROR": Colors.RED,
        "CRITICAL": Colors.BRIGHT_RED,
    }

    def format(self, record: LogRecord) -> str:
        """Format log record with colors and level prefix."""
        level_name = record.levelname
        color = self.LEVEL_COLORS.get(level_name, Colors.RESET)

        # Format message
        message = record.getMessage()

        # Add extra fields if present
        extra_parts = []
        standard_attrs = {
            "name",
            "msg",
            "args",
            "created",
            "filename",
            "funcName",
            "levelname",
            "levelno",
            "lineno",
            "module",
            "msecs",
            "message",
            "pathname",
            "process",
            "processName",
            "relativeCreated",
            "thread",
            "threadName",
            "exc_info",
            "exc_text",
            "stack_info",
        }

        for key, value in record.__dict__.items():
            if key not in standard_attrs and value is not None:
                extra_parts.append(f"{key}={value}")

        if extra_parts:
            message = f"{message} | {' | '.join(extra_parts)}"

        # Format exception if present
        if record.exc_info:
            message = f"{message}\n{self.formatException(record.exc_info)}"

        # Format: "LEVEL:     message"
        formatted = f"{level_name}:     {message}"

        # Add color
        if color != Colors.RESET:
            formatted = f"{color}{formatted}{Colors.RESET}"

        return formatted


class JSONFormatter(logging.Formatter):
    def format(self, record: LogRecord) -> str:
        log_data: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields from record (all non-standard attributes)
        # Standard LogRecord attributes are already handled above
        # We need to get custom attributes that were added via extra parameter
        standard_attrs = {
            "name",
            "msg",
            "args",
            "created",
            "filename",
            "funcName",
            "levelname",
            "levelno",
            "lineno",
            "module",
            "msecs",
            "message",
            "pathname",
            "process",
            "processName",
            "relativeCreated",
            "thread",
            "threadName",
            "exc_info",
            "exc_text",
            "stack_info",
        }
        for key, value in record.__dict__.items():
            # Skip standard LogRecord attributes
            if key not in standard_attrs and value is not None:
                log_data[key] = value

        return json.dumps(log_data, ensure_ascii=False)


def setup_logging() -> None:
    """Configure logging for the application."""
    log_level = getenv("LOG_LEVEL", "INFO").upper()
    use_json = getenv("LOG_JSON", "false").lower() in ("true", "1", "yes")

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers
    root_logger.handlers.clear()

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    # Set formatter
    formatter = JSONFormatter() if use_json else ColoredFormatter()

    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Set level for third-party libraries
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
