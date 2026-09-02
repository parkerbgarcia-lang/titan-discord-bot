"""TITAN Discord Bot - Main entry point.

Total Infrastructure Tickrate Alignment Normalizer
An official Discord bot demonstrating cybersecurity attack/defense capabilities.

WARNING: This bot performs destructive operations on whitelisted test servers only.
Unauthorized use is prohibited.
"""

import asyncio
import sys
import discord
from discord.ext import commands
from pathlib import Path

from config import config, BOT_NAME, BOT_FULL_NAME, VERSION, DEFAULT_PREFIX
from utils.terminal import (
    print_banner,
    print_section,
    print_info,
    print_success,
    print_error,
    print_warning,
)
from utils.logger import logger


def validate_startup() -> bool:
    """Validate startup conditions.
    
    Returns:
        bool: True if startup is valid, False otherwise.
    """
    print_section("Startup Validation")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print_error(f"Python 3.8+ required, found {sys.version_info.major}.{sys.version_info.minor}")
        return False
    print_success(f"Python {sys.version_info.major}.{sys.version_info.minor} OK")
    
    # Validate configuration
    try:
        config.validate()
        print_success("Configuration validated")
    except ValueError as e:
        print_error(str(e))
        logger.error(f"Configuration validation failed: {e}")
        return False
    
    # Check logs directory
    if config.log_dir.exists():
        print_success(f"Logs directory ready: {config.log_dir}")
    else:
        print_warning(f"Logs directory not found, will create at runtime")
    
    # Display whitelisted servers
    print_info(f"Whitelisted servers: {config.whitelist_servers}")
    print_info(f"Bot owner ID: {config.owner_id}")
    
    return True


def create_bot() -> commands.Bot:
    """Create and configure the Discord bot.
    
    Returns:
        commands.Bot: Configured bot instance.
    """
    # Intents with members enabled for kick operations
    intents = discord.Intents.default()
    intents.message_content = True  # Read message content
    intents.members = True  # Track member join/leave and kick
    intents.guilds = True  # Track guild updates
    
    bot = commands.Bot(
        command_prefix=config.prefix,
        intents=intents,
        help_command=None,  # We provide our own help command
    )
    
    return bot


async def load_cogs(bot: commands.Bot) -> None:
    """Load all cogs from the cogs directory.
    
    Args:
        bot: The bot instance.
    """
    print_section("Loading Cogs")
    
    cogs_to_load = ["cogs.events", "cogs.commands", "cogs.nuke"]
    
    for cog in cogs_to_load:
        try:
            await bot.load_extension(cog)
            print_success(f"Loaded {cog}")
            logger.info(f"Cog loaded: {cog}")
        except Exception as e:
            print_error(f"Failed to load {cog}: {e}")
            logger.error(f"Cog loading failed: {cog}", exc_info=e)


async def main() -> None:
    """Main entry point."""
    # Show banner
    print_banner()
    
    # Validate startup
    if not validate_startup():
        logger.critical("Startup validation failed")
        sys.exit(1)
    
    # Create bot
    print_section("Initializing Bot")
    bot = create_bot()
    print_info(f"Bot name: {BOT_NAME}")
    print_info(f"Command prefix: {config.prefix}")
    print_success("Bot created")
    
    # Load cogs
    await load_cogs(bot)
    
    # Start bot
    print_section("Starting Bot")
    print_info(f"Connecting to Discord...")
    logger.info(f"Starting {BOT_NAME} v{VERSION}")
    
    try:
        await bot.start(config.token)
    except discord.LoginFailure:
        print_error("Invalid token provided")
        logger.critical("Login failed: invalid token")
        sys.exit(1)
    except KeyboardInterrupt:
        print_info("Shutdown requested")
        logger.info("Bot shutdown requested by user")
        await bot.close()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        logger.critical(f"Unexpected error: {e}", exc_info=e)
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print_info("Exiting...")
        sys.exit(0)
