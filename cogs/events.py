"""Event handlers for TITAN bot.

Handles Discord lifecycle events like ready, connect, and errors.
"""

import discord
from discord.ext import commands
from utils.terminal import print_info, print_success, print_error
from utils.logger import logger
from config import BOT_NAME, VERSION


class Events(commands.Cog):
    """Discord event handlers."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self) -> None:
        """Called when bot connects to Discord."""
        print_info(f"Connecting to Discord...")
        logger.info("Connected to Discord")

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Called when bot is fully ready."""
        print_success(f"{BOT_NAME} is ready")
        print_info(f"Logged in as: {self.bot.user}")
        print_info(f"Bot ID: {self.bot.user.id}")
        logger.info(f"Bot ready as {self.bot.user} (ID: {self.bot.user.id})")
        logger.info(f"Watching {len(self.bot.guilds)} guild(s)")

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context) -> None:
        """Called when a command is invoked."""
        logger.info(
            f"Command invoked: {ctx.command.name} | "
            f"User: {ctx.author} (ID: {ctx.author.id}) | "
            f"Guild: {ctx.guild.name if ctx.guild else 'DM'} "
            f"(ID: {ctx.guild.id if ctx.guild else 'N/A'})"
        )

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        """Global command error handler.
        
        Args:
            ctx: Command context.
            error: The error that occurred.
        """
        # Don't handle if the command has its own error handler
        if hasattr(ctx.command, "on_error"):
            return

        # Log the error
        logger.error(
            f"Command error in {ctx.command.name}: {type(error).__name__}: {error}",
            exc_info=error,
        )

        # Handle specific error types
        if isinstance(error, commands.CommandNotFound):
            print_error(f"Command not found: {ctx.message.content}")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Missing required argument: {error.param.name}")
            return

        if isinstance(error, commands.MissingPermissions):
            perms = ", ".join(error.missing_permissions)
            await ctx.send(f"❌ You need these permissions: {perms}")
            logger.warning(
                f"Permission denied for {ctx.author}: needed {perms}"
            )
            return

        if isinstance(error, commands.BotMissingPermissions):
            perms = ", ".join(error.missing_permissions)
            await ctx.send(f"❌ I need these permissions: {perms}")
            logger.warning(f"Bot missing permissions: {perms}")
            return

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"❌ Command on cooldown. Try again in {error.retry_after:.1f}s"
            )
            return

        # Generic error response
        await ctx.send(
            f"❌ An error occurred: {type(error).__name__}"
        )
        print_error(f"{type(error).__name__}: {error}")


async def setup(bot: commands.Bot) -> None:
    """Load the Events cog.
    
    Args:
        bot: The bot instance.
    """
    await bot.add_cog(Events(bot))
