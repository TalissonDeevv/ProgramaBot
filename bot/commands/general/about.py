"""Comando /about: apresenta o projeto ProgramaBot.

Também mostra como criar *botões de link*, que abrem um site quando clicados
e não precisam de nenhum código de callback.
"""

import discord
from discord import app_commands
from discord.ext import commands

from bot import REPOSITORY_URL, __maintainer__, __version__
from bot.utils.embeds import base_embed

DOCS_URL = f"{REPOSITORY_URL}/tree/main/education"


def build_about_view() -> discord.ui.View:
    """Cria uma view com botões que levam ao GitHub e à documentação."""
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Código no GitHub", url=REPOSITORY_URL, emoji="💻"))
    view.add_item(discord.ui.Button(label="Trilha de estudos", url=DOCS_URL, emoji="📚"))
    return view


class About(commands.Cog):
    """Cog que contém o /about."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="about", description="Conheça o projeto ProgramaBot.")
    async def about(self, interaction: discord.Interaction) -> None:
        embed = base_embed(
            "🤖 Sobre o ProgramaBot",
            "Um bot de Discord **open source** criado para ensinar programação na prática.\n"
            "Todo o código está disponível e explicado, arquivo por arquivo.",
        )
        embed.add_field(name="Versão", value=__version__)
        embed.add_field(name="discord.py", value=discord.__version__)
        embed.add_field(name="Mantenedor", value=__maintainer__)
        embed.add_field(name="Servidores", value=str(len(self.bot.guilds)))
        embed.add_field(name="Licença", value="MIT")
        if self.bot.user is not None:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        await interaction.response.send_message(embed=embed, view=build_about_view())


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(About(bot))
