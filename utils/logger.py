"""Logging configuration for TITAN bot.

Sets up file and console logging with proper rotation and formatting.
Logs normal activity to titan.log and errors to errors.log.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from config import LOG_DIR, BOT_NAME


def setup_logger(name: str = "titan") -> logging.Logger:
    """Set up application logging.
    
    Creates two rotating file handlers:
    - titan.log: Normal activity logs
    - errors.log: Error logs with stack traces
    
    Args:
        name: Logger name (default: "titan").
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Log format
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Normal log handler (all levels)
    normal_handler = RotatingFileHandler(
        LOG_DIR / "titan.log",
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5,
        encoding="utf-8",
    )
    normal_handler.setLevel(logging.DEBUG)
    normal_handler.setFormatter(formatter)
    logger.addHandler(normal_handler)

    # Error log handler (errors and warnings only)
    error_handler = RotatingFileHandler(
        LOG_DIR / "errors.log",
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.WARNING)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    return logger


# Create global logger instance
logger = setup_logger()
