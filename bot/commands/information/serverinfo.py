"""Comando /serverinfo: mostra informações do servidor atual."""

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import base_embed


class ServerInfo(commands.Cog):
    """Cog que contém o /serverinfo."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="serverinfo", description="Mostra informações do servidor.")
    @app_commands.guild_only()
    async def serverinfo(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("Use este comando em um servidor.", ephemeral=True)
            return

        embed = base_embed(f"🏠 {guild.name}", guild.description)
        if guild.icon is not None:
            embed.set_thumbnail(url=guild.icon.url)

        embed.add_field(name="Dono", value=f"<@{guild.owner_id}>")
        embed.add_field(name="Membros", value=str(guild.member_count or "Desconhecido"))
        embed.add_field(name="ID", value=str(guild.id))
        embed.add_field(name="Canais de texto", value=str(len(guild.text_channels)))
        embed.add_field(name="Canais de voz", value=str(len(guild.voice_channels)))
        embed.add_field(name="Cargos", value=str(len(guild.roles)))
        embed.add_field(
            name="Impulsos (boosts)",
            value=f"{guild.premium_subscription_count or 0} (nível {guild.premium_tier})",
        )
        embed.add_field(
            name="Criado em",
            value=f"{discord.utils.format_dt(guild.created_at, 'D')} ({discord.utils.format_dt(guild.created_at, 'R')})",
            inline=False,
        )
        await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions.none())


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ServerInfo(bot))
