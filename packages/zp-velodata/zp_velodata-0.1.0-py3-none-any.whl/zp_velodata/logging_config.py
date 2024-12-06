"""Logging configuration module for zp_velodata"""

import logging
import logging.config
import sys
from pathlib import Path

# Default logging format
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Default logging configuration
DEFAULT_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": DEFAULT_FORMAT},
        "detailed": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "package.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
    },
    "loggers": {"zp_velodata": {"level": "INFO", "handlers": ["console", "file"], "propagate": False}},
    "root": {"level": "WARNING", "handlers": ["console"]},
}


def setup_logging(
    config_path: str | Path | None = None,
    config_dict: dict | None = None,
    default_level: str = "INFO",
    log_file: str | Path | None = None,
) -> None:
    """Setup logging configuration for the package.

    Args:
        config_dict: Dictionary containing logging configuration
        default_level: Default logging level if configuration fails
        log_file: Path to log file (overrides the one in config)

    Priority of configuration sources:
    1. config_dict (if provided)
    2. DEFAULT_CONFIG

    Example:
        >>> setup_logging(default_level="DEBUG")
        >>> setup_logging(config_dict=custom_config)

    """
    config = DEFAULT_CONFIG.copy()

    try:
        if config_dict is not None:
            config.update(config_dict)

        # Override log file path if provided
        if log_file is not None:
            config["handlers"]["file"]["filename"] = str(log_file)

        logging.config.dictConfig(config)

    except Exception as e:
        # If configuration fails, set up basic logging
        print(f"Error in logging configuration: {e}", file=sys.stderr)
        print("Falling back to basic logging configuration", file=sys.stderr)
        logging.basicConfig(level=default_level, format=DEFAULT_FORMAT)


def get_logger(name: str | None = None) -> logging.Logger:
    """Get a logger instance for the package.

    Args:
        name: Logger name (usually __name__ from the calling module)
              If None, returns the root logger for the package

    Returns:
        logging.Logger: Configured logger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("This is an info message")
        >>> logger.error("This is an error message")

    """
    if name is None:
        name = "your_package"  # Replace with your package name
    return logging.getLogger(name)


# Example usage in your package's __init__.py:
"""
from .logging_config import setup_logging, get_logger

# Set up default logging configuration
setup_logging()

# Create a logger for the package
logger = get_logger(__name__)
"""
