"""Audit logging for TITAN operations.

Tracks all nuke operations with detailed information for analysis and rollback.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from config import LOG_DIR
from datetime import datetime
import json


def setup_audit_logger() -> logging.Logger:
    """Set up audit logging for nuke operations.
    
    Creates audit.log with detailed operation records in JSON format.
    
    Returns:
        logging.Logger: Configured audit logger instance.
    """
    audit_logger = logging.getLogger("audit")
    audit_logger.setLevel(logging.INFO)

    # Audit log format (structured for easy parsing)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Audit handler
    audit_handler = RotatingFileHandler(
        LOG_DIR / "audit.log",
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=10,
        encoding="utf-8",
    )
    audit_handler.setLevel(logging.INFO)
    audit_handler.setFormatter(formatter)
    audit_logger.addHandler(audit_handler)

    return audit_logger


class AuditLogger:
    """Structured audit logging for nuke operations."""

    def __init__(self):
        self.logger = setup_audit_logger()

    def log_operation(
        self,
        operation: str,
        guild_id: int,
        guild_name: str,
        user_id: int,
        user_name: str,
        success: bool,
        details: dict = None,
    ) -> None:
        """Log a nuke operation with full details.
        
        Args:
            operation: Type of operation (nuke, nuke-channels, etc.)
            guild_id: Discord guild/server ID
            guild_name: Guild name
            user_id: User who ran the command
            user_name: User's Discord username
            success: Whether the operation succeeded
            details: Additional operation details (deleted items, errors, etc.)
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "guild": {
                "id": guild_id,
                "name": guild_name,
            },
            "user": {
                "id": user_id,
                "name": user_name,
            },
            "success": success,
            "details": details or {},
        }
        
        self.logger.info(json.dumps(log_entry))

    def log_deletion(
        self,
        guild_id: int,
        item_type: str,
        item_name: str,
        item_id: int,
        success: bool,
    ) -> None:
        """Log a specific deletion (channel, role, member, etc.).
        
        Args:
            guild_id: Guild ID
            item_type: Type of item (channel, role, member, etc.)
            item_name: Name of the deleted item
            item_id: ID of the deleted item
            success: Whether deletion succeeded
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "delete",
            "item_type": item_type,
            "item_name": item_name,
            "item_id": item_id,
            "guild_id": guild_id,
            "success": success,
        }
        
        self.logger.info(json.dumps(log_entry))


# Create global audit logger instance
audit_logger = AuditLogger()
