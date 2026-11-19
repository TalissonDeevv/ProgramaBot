"""Comando /help: central de ajuda com menu de seleção.

A parte visual (o menu e os embeds) fica em ``bot/views/help_menu.py``.
Este arquivo apenas registra o comando e envia a mensagem.
"""

import discord
from discord import app_commands
from discord.ext import commands

from bot.views.help_menu import HelpView, build_overview_embed


class Help(commands.Cog):
    """Cog que contém o /help."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="help", description="Mostra todos os comandos do ProgramaBot.")
    async def help(self, interaction: discord.Interaction) -> None:
        # ephemeral=True: só quem usou o comando vê a resposta.
        await interaction.response.send_message(
            embed=build_overview_embed(),
            view=HelpView(),
            ephemeral=True,
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Help(bot))
