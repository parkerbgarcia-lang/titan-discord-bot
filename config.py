"""Configuration module for TITAN bot.

Loads and validates environment variables from .env file.
Defines application constants and configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Application constants
BOT_NAME = "TITAN"
BOT_FULL_NAME = "Total Infrastructure Tickrate Alignment Normalizer"
VERSION = "1.0.0"
DEFAULT_PREFIX = "!"
LOG_DIR = Path(__file__).parent / "logs"

# Create logs directory if it doesn't exist
LOG_DIR.mkdir(exist_ok=True)

# Configuration class
class Config:
    """Bot configuration from environment variables."""

    def __init__(self):
        self.token = os.getenv("DISCORD_TOKEN")
        self.prefix = os.getenv("COMMAND_PREFIX", DEFAULT_PREFIX)
        self.log_dir = LOG_DIR

    def validate(self) -> bool:
        """Validate that all required configuration is present.
        
        Returns:
            bool: True if valid, raises exception otherwise.
            
        Raises:
            ValueError: If required configuration is missing.
        """
        if not self.token:
            raise ValueError(
                "DISCORD_TOKEN not found in .env file. "
                "Please copy .env.example to .env and add your bot token."
            )
        if not self.token or len(self.token) < 50:
            raise ValueError(
                "DISCORD_TOKEN appears invalid (too short). "
                "Check your .env file."
            )
        return True


# Create global config instance
config = Config()
