"""Nuke commands for TITAN bot.

Provides server destruction capabilities with comprehensive logging and safety features.
All operations are logged to audit.log for analysis and rollback.

WARNING: These commands permanently delete server data. Use only on test servers.
"""

import discord
from discord.ext import commands
from typing import List, Dict, Optional
import asyncio
from utils.logger import logger
from utils.audit import audit_logger
from config import config


class NukeCommands(commands.Cog):
    """Server nuke operations with logging."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _is_owner(self, ctx: commands.Context) -> bool:
        """Check if user is the bot owner.
        
        Args:
            ctx: Command context.
            
        Returns:
            bool: True if user is owner, False otherwise.
        """
        return ctx.author.id == config.owner_id

    async def _is_whitelisted_server(self, guild: discord.Guild) -> bool:
        """Check if server is whitelisted for nuke operations.
        
        Args:
            guild: Discord guild/server.
            
        Returns:
            bool: True if server is whitelisted, False otherwise.
        """
        return config.is_whitelisted_server(guild.id)

    async def _confirm(self, ctx: commands.Context, prompt: str) -> bool:
        """Ask user for confirmation before destructive operation.
        
        Args:
            ctx: Command context.
            prompt: Confirmation prompt message.
            
        Returns:
            bool: True if user confirms (reacts with ✅), False otherwise.
        """
        msg = await ctx.send(f"⚠️ {prompt}\n\nReact with ✅ to confirm or ❌ to cancel.")
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == msg.id

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
            await msg.delete()
            return reaction.emoji == "✅"
        except asyncio.TimeoutError:
            await msg.delete()
            return False

    @commands.command(name="nuke", hidden=True)
    async def nuke(self, ctx: commands.Context) -> None:
        """Nuclear option: delete all channels, roles, and kick all members.
        
        DESTRUCTIVE: This cannot be undone. Server will be empty.
        Owner-only. Whitelisted servers only.
        
        Args:
            ctx: Command context.
        """
        # Permission checks
        if not await self._is_owner(ctx):
            await ctx.send("❌ This command is owner-only.")
            logger.warning(
                f"Unauthorized nuke attempt by {ctx.author} (ID: {ctx.author.id})"
            )
            return

        if not await self._is_whitelisted_server(ctx.guild):
            await ctx.send(
                f"❌ This server is not whitelisted for TITAN operations. "
                f"Server ID: {ctx.guild.id}\n"
                f"Add it to `config.py` whitelist_servers to enable."
            )
            logger.warning(
                f"Nuke attempt on non-whitelisted server: {ctx.guild.name} (ID: {ctx.guild.id})"
            )
            audit_logger.log_operation(
                "nuke",
                ctx.guild.id,
                ctx.guild.name,
                ctx.author.id,
                str(ctx.author),
                False,
                {"error": "Server not whitelisted"},
            )
            return

        # Confirmation
        if not await self._confirm(ctx, f"NUKE SERVER '{ctx.guild.name}'? This deletes ALL channels, roles, and kicks ALL members."):
            await ctx.send("❌ Nuke cancelled.")
            return

        await ctx.send("🔴 **INITIATING NUCLEAR DETONATION** 🔴")
        logger.info(f"Nuke initiated on {ctx.guild.name} by {ctx.author}")

        details = {
            "channels_deleted": 0,
            "roles_deleted": 0,
            "members_kicked": 0,
            "errors": [],
        }

        try:
            # Delete all channels
            for channel in ctx.guild.channels:
                try:
                    await channel.delete()
                    details["channels_deleted"] += 1
                    audit_logger.log_deletion(
                        ctx.guild.id, "channel", channel.name, channel.id, True
                    )
                except Exception as e:
                    details["errors"].append(f"Channel {channel.name}: {str(e)}")
                    logger.error(f"Failed to delete channel {channel.name}: {e}")
                    audit_logger.log_deletion(
                        ctx.guild.id, "channel", channel.name, channel.id, False
                    )

            # Delete all roles (except @everyone)
            for role in ctx.guild.roles:
                if role.name == "@everyone":
                    continue
                try:
                    await role.delete()
                    details["roles_deleted"] += 1
                    audit_logger.log_deletion(
                        ctx.guild.id, "role", role.name, role.id, True
                    )
                except Exception as e:
                    details["errors"].append(f"Role {role.name}: {str(e)}")
                    logger.error(f"Failed to delete role {role.name}: {e}")
                    audit_logger.log_deletion(
                        ctx.guild.id, "role", role.name, role.id, False
                    )

            # Kick all members except bot
            for member in ctx.guild.members:
                if member.id == self.bot.user.id:
                    continue
                try:
                    await member.kick()
                    details["members_kicked"] += 1
                    audit_logger.log_deletion(
                        ctx.guild.id, "member", str(member), member.id, True
                    )
                except Exception as e:
                    details["errors"].append(f"Member {member}: {str(e)}")
                    logger.error(f"Failed to kick member {member}: {e}")
                    audit_logger.log_deletion(
                        ctx.guild.id, "member", str(member), member.id, False
                    )

            # Log the complete operation
            audit_logger.log_operation(
                "nuke",
                ctx.guild.id,
                ctx.guild.name,
                ctx.author.id,
                str(ctx.author),
                True,
                details,
            )

            await ctx.send(
                f"☢️ **DETONATION COMPLETE** ☢️\n"
                f"Channels deleted: {details['channels_deleted']}\n"
                f"Roles deleted: {details['roles_deleted']}\n"
                f"Members kicked: {details['members_kicked']}\n"
                f"Errors: {len(details['errors'])}"
            )
            logger.info(
                f"Nuke complete on {ctx.guild.name}: "
                f"{details['channels_deleted']} channels, "
                f"{details['roles_deleted']} roles, "
                f"{details['members_kicked']} members"
            )

        except Exception as e:
            error_msg = f"Critical error during nuke: {str(e)}"
            await ctx.send(f"❌ {error_msg}")
            logger.error(error_msg, exc_info=e)
            audit_logger.log_operation(
                "nuke",
                ctx.guild.id,
                ctx.guild.name,
                ctx.author.id,
                str(ctx.author),
                False,
                {"error": str(e)},
            )

    @commands.command(name="nuke-channels", hidden=True)
    async def nuke_channels(self, ctx: commands.Context) -> None:
        """Delete all channels in the server.
        
        Owner-only. Whitelisted servers only.
        
        Args:
            ctx: Command context.
        """
        if not await self._is_owner(ctx):
            await ctx.send("❌ This command is owner-only.")
            return

        if not await self._is_whitelisted_server(ctx.guild):
            await ctx.send(
                f"❌ This server is not whitelisted. Server ID: {ctx.guild.id}"
            )
            return

        if not await self._confirm(ctx, f"Delete ALL channels in '{ctx.guild.name}'?"):
            await ctx.send("❌ Operation cancelled.")
            return

        deleted = 0
        errors = []

        for channel in ctx.guild.channels:
            try:
                await channel.delete()
                deleted += 1
                audit_logger.log_deletion(
                    ctx.guild.id, "channel", channel.name, channel.id, True
                )
            except Exception as e:
                errors.append(f"{channel.name}: {str(e)}")
                audit_logger.log_deletion(
                    ctx.guild.id, "channel", channel.name, channel.id, False
                )

        audit_logger.log_operation(
            "nuke-channels",
            ctx.guild.id,
            ctx.guild.name,
            ctx.author.id,
            str(ctx.author),
            len(errors) == 0,
            {"deleted": deleted, "errors": errors},
        )

        await ctx.send(f"✅ Deleted {deleted} channels. Errors: {len(errors)}")

    @commands.command(name="nuke-roles", hidden=True)
    async def nuke_roles(self, ctx: commands.Context) -> None:
        """Delete all roles in the server.
        
        Owner-only. Whitelisted servers only.
        
        Args:
            ctx: Command context.
        """
        if not await self._is_owner(ctx):
            await ctx.send("❌ This command is owner-only.")
            return

        if not await self._is_whitelisted_server(ctx.guild):
            await ctx.send(
                f"❌ This server is not whitelisted. Server ID: {ctx.guild.id}"
            )
            return

        if not await self._confirm(ctx, f"Delete ALL roles in '{ctx.guild.name}'?"):
            await ctx.send("❌ Operation cancelled.")
            return

        deleted = 0
        errors = []

        for role in ctx.guild.roles:
            if role.name == "@everyone":
                continue
            try:
                await role.delete()
                deleted += 1
                audit_logger.log_deletion(
                    ctx.guild.id, "role", role.name, role.id, True
                )
            except Exception as e:
                errors.append(f"{role.name}: {str(e)}")
                audit_logger.log_deletion(
                    ctx.guild.id, "role", role.name, role.id, False
                )

        audit_logger.log_operation(
            "nuke-roles",
            ctx.guild.id,
            ctx.guild.name,
            ctx.author.id,
            str(ctx.author),
            len(errors) == 0,
            {"deleted": deleted, "errors": errors},
        )

        await ctx.send(f"✅ Deleted {deleted} roles. Errors: {len(errors)}")

    @commands.command(name="nuke-members", hidden=True)
    async def nuke_members(self, ctx: commands.Context) -> None:
        """Kick all members from the server.
        
        Owner-only. Whitelisted servers only.
        
        Args:
            ctx: Command context.
        """
        if not await self._is_owner(ctx):
            await ctx.send("❌ This command is owner-only.")
            return

        if not await self._is_whitelisted_server(ctx.guild):
            await ctx.send(
                f"❌ This server is not whitelisted. Server ID: {ctx.guild.id}"
            )
            return

        if not await self._confirm(ctx, f"Kick ALL members from '{ctx.guild.name}'?"):
            await ctx.send("❌ Operation cancelled.")
            return

        kicked = 0
        errors = []

        for member in ctx.guild.members:
            if member.id == self.bot.user.id:
                continue
            try:
                await member.kick()
                kicked += 1
                audit_logger.log_deletion(
                    ctx.guild.id, "member", str(member), member.id, True
                )
            except Exception as e:
                errors.append(f"{member}: {str(e)}")
                audit_logger.log_deletion(
                    ctx.guild.id, "member", str(member), member.id, False
                )

        audit_logger.log_operation(
            "nuke-members",
            ctx.guild.id,
            ctx.guild.name,
            ctx.author.id,
            str(ctx.author),
            len(errors) == 0,
            {"kicked": kicked, "errors": errors},
        )

        await ctx.send(f"✅ Kicked {kicked} members. Errors: {len(errors)}")


async def setup(bot: commands.Bot) -> None:
    """Load the NukeCommands cog.
    
    Args:
        bot: The bot instance.
    """
    await bot.add_cog(NukeCommands(bot))
