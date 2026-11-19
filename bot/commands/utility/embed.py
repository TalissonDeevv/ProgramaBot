"""Comando /embed: abre um formulário (modal) para criar um embed personalizado.

O formulário está em ``bot/views/embed_modal.py``.
"""

import discord
from discord import app_commands
from discord.ext import commands

from bot.views.embed_modal import EmbedModal


class EmbedBuilder(commands.Cog):
    """Cog que contém o /embed."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="embed", description="Abre um formulário para criar um embed.")
    @app_commands.checks.cooldown(1, 30.0)  # 1 uso a cada 30 segundos por pessoa.
    async def embed(self, interaction: discord.Interaction) -> None:
        # Abrir um modal é uma forma de responder à interação.
        await interaction.response.send_modal(EmbedModal())


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(EmbedBuilder(bot))
