"""Example commands for TITAN bot.

Demonstrates safe, read-only commands for a Discord bot.
"""

import discord
from discord.ext import commands
from datetime import datetime
from utils.logger import logger
from config import BOT_NAME, BOT_FULL_NAME, VERSION


class Commands(commands.Cog):
    """Example commands for TITAN."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = datetime.now()

    @commands.command(name="ping", aliases=["p"])
    async def ping(self, ctx: commands.Context) -> None:
        """Show bot latency.
        
        Args:
            ctx: Command context.
        """
        latency_ms = round(self.bot.latency * 1000)
        await ctx.send(f"🏓 Pong! Latency: {latency_ms}ms")
        logger.info(f"Ping command: {latency_ms}ms latency")

    @commands.command(name="help", aliases=["h", "commands"])
    async def help_command(self, ctx: commands.Context) -> None:
        """List all available commands.
        
        Args:
            ctx: Command context.
        """
        commands_list = []
        for cmd in self.bot.commands:
            if not cmd.hidden:
                aliases_str = f" ({', '.join(cmd.aliases)})" if cmd.aliases else ""
                commands_list.append(f"!{cmd.name}{aliases_str} - {cmd.help or 'No description'}")
        
        commands_text = "\n".join(sorted(commands_list))
        await ctx.send(f"```\n{commands_text}\n```")
        logger.debug(f"Help command invoked by {ctx.author}")

    @commands.command(name="about", aliases=["info"])
    async def about(self, ctx: commands.Context) -> None:
        """Show information about TITAN.
        
        Args:
            ctx: Command context.
        """
        about_text = f"""
{BOT_NAME} - {BOT_FULL_NAME}
Version {VERSION}

{BOT_NAME} is a demonstration Discord bot showcasing clean architecture,
security best practices, and professional logging. It runs as an official
bot account and respects Discord's API limits.

Use !help to see available commands.
        """
        await ctx.send(about_text.strip())
        logger.debug(f"About command invoked by {ctx.author}")

    @commands.command(name="status", aliases=["stats"])
    async def status(self, ctx: commands.Context) -> None:
        """Show bot status and statistics.
        
        Args:
            ctx: Command context.
        """
        uptime_seconds = (datetime.now() - self.start_time).total_seconds()
        uptime_minutes = int(uptime_seconds // 60)
        uptime_seconds = int(uptime_seconds % 60)
        latency_ms = round(self.bot.latency * 1000)
        
        status_text = f"""
**{BOT_NAME} Status**
Version: {VERSION}
Latency: {latency_ms}ms
Uptime: {uptime_minutes}m {uptime_seconds}s
Guilds: {len(self.bot.guilds)}
Users: {len(self.bot.users)}
        """
        await ctx.send(status_text.strip())
        logger.debug(f"Status command invoked by {ctx.author}")

    @commands.command(name="userinfo", aliases=["user", "whois"])
    async def userinfo(self, ctx: commands.Context, member: discord.Member = None) -> None:
        """Show information about a user.
        
        Args:
            ctx: Command context.
            member: The member to get info about (default: command invoker).
        """
        if member is None:
            member = ctx.author
        
        account_age = datetime.now() - member.created_at
        account_age_days = account_age.days
        
        userinfo_text = f"""
**User Information**
Name: {member}
ID: {member.id}
Bot: {'Yes' if member.bot else 'No'}
Account Age: {account_age_days} days
Joined Server: {member.joined_at.strftime('%Y-%m-%d') if member.joined_at else 'N/A'}
Roles: {len(member.roles)}
        """
        await ctx.send(userinfo_text.strip())
        logger.debug(f"Userinfo command: fetched info for {member}")


async def setup(bot: commands.Bot) -> None:
    """Load the Commands cog.
    
    Args:
        bot: The bot instance.
    """
    await bot.add_cog(Commands(bot))
