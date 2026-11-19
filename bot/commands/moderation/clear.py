"""Comando /clear: apaga mensagens recentes do canal."""

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import error_embed, success_embed

# Tipos de canal que possuem o método purge (apagar mensagens em massa).
PURGEABLE_CHANNELS = (discord.TextChannel, discord.Thread, discord.VoiceChannel)


class Clear(commands.Cog):
    """Cog que contém o /clear."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="clear", description="Apaga mensagens recentes deste canal.")
    @app_commands.describe(quantidade="Quantas mensagens apagar (1 a 100).")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True, read_message_history=True)
    async def clear(
        self,
        interaction: discord.Interaction,
        quantidade: app_commands.Range[int, 1, 100],
    ) -> None:
        channel = interaction.channel
        if not isinstance(channel, PURGEABLE_CHANNELS):
            await interaction.response.send_message(
                embed=error_embed("Não é possível apagar mensagens neste tipo de canal."), ephemeral=True
            )
            return

        # Apagar mensagens pode levar mais de 3 segundos. defer() avisa ao Discord
        # que a resposta vai demorar ("ProgramaBot está pensando...").
        await interaction.response.defer(ephemeral=True, thinking=True)
        deleted = await channel.purge(limit=quantidade, reason=f"/clear usado por {interaction.user}")

        word = "mensagem apagada" if len(deleted) == 1 else "mensagens apagadas"
        await interaction.followup.send(embed=success_embed(f"🧹 {len(deleted)} {word}."), ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Clear(bot))
