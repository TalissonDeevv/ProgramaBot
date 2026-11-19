"""Comando /ping: mostra a latência do bot.

Latência é o tempo que uma mensagem leva para ir do bot até o Discord e voltar.
É o primeiro comando que todo bot costuma ter, porque serve para testar se
ele está online e respondendo.
"""

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import info_embed


def latency_status(latency_ms: int) -> str:
    """Classifica a latência em uma frase fácil de entender."""
    if latency_ms < 100:
        return "🟢 Excelente"
    if latency_ms < 250:
        return "🟡 Boa"
    return "🔴 Alta"


class Ping(commands.Cog):
    """Cog (grupo de comandos) que contém o /ping."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="Mostra a latência (tempo de resposta) do bot.")
    async def ping(self, interaction: discord.Interaction) -> None:
        # bot.latency vem em segundos (ex.: 0.087). Multiplicamos por 1000 para ter milissegundos.
        latency_ms = round(self.bot.latency * 1000)
        embed = info_embed(
            f"🏓 Pong! Latência: **{latency_ms} ms**\nQualidade: {latency_status(latency_ms)}",
            title="Ping",
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """Função chamada pelo ``bot.load_extension`` para registrar o Cog."""
    await bot.add_cog(Ping(bot))
