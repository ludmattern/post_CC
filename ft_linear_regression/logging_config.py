#!/usr/bin/env python3
"""
Logging configuration for linear regression project.
Provides structured logging with proper colors and centralized configuration.
"""

import logging
import sys


LOG_COLORS = {
    "DEBUG": "\033[36m",
    "INFO": "\033[32m",
    "WARNING": "\033[33m",
    "ERROR": "\033[31m",
    "CRITICAL": "\033[35m",
}
RESET_COLOR = "\033[0m"


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output."""

    def format(self, record):
        if sys.stdout.isatty():
            color = LOG_COLORS.get(record.levelname, "")
            record.levelname = f"{color}{record.levelname:<8}{RESET_COLOR}"
        else:
            record.levelname = f"{record.levelname:<8}"
        return super().format(record)


def configure_logging(level: str = "INFO"):
    """
    Configure logging for the entire project.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    numeric_level = getattr(logging, level.upper(), logging.INFO)
    root_logger.setLevel(numeric_level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = ColoredFormatter(fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s", datefmt="%H:%M:%S")
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(numeric_level)
    root_logger.addHandler(console_handler)


def get_logger(name: str = None):
    """Get a logger instance for a module."""
    if name is None:
        name = "linear_regression"
    return logging.getLogger(name)


configure_logging(level="INFO")  # Set default logging level to DEBUG for development
