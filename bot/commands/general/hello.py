"""Comando /hello: cumprimenta o usuário de acordo com o horário.

Ótimo para estudar condicionais (``if``/``elif``/``else``), parâmetros
opcionais e o módulo ``random``.
"""

import random
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

STUDY_TIPS = (
    "Que tal abrir o arquivo bot/commands/general/hello.py e mudar esta mensagem?",
    "Use /help para ver todos os comandos e estudar cada um deles.",
    "Errar faz parte: leia a mensagem de erro com calma, ela costuma dizer o problema.",
    "Pratique um pouco todos os dias. Constância vale mais que intensidade.",
    "Toda a documentação está na pasta education/ do repositório.",
)


def greeting_for_hour(hour: int) -> str:
    """Retorna "Bom dia", "Boa tarde" ou "Boa noite" para uma hora de 0 a 23."""
    if not 0 <= hour <= 23:
        raise ValueError("A hora deve estar entre 0 e 23.")
    if 5 <= hour < 12:
        return "Bom dia"
    if 12 <= hour < 18:
        return "Boa tarde"
    return "Boa noite"


class Hello(commands.Cog):
    """Cog que contém o /hello."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="hello", description="Receba um cumprimento do ProgramaBot.")
    @app_commands.describe(nome="Como você quer ser chamado (opcional).")
    async def hello(
        self,
        interaction: discord.Interaction,
        nome: app_commands.Range[str, 1, 50] | None = None,
    ) -> None:
        # Se o usuário não informar um nome, usamos o nome de exibição dele.
        name = nome or interaction.user.display_name
        greeting = greeting_for_hour(datetime.now().hour)
        tip = random.choice(STUDY_TIPS)
        await interaction.response.send_message(
            f"{greeting}, **{name}**! 👋\n💡 Dica: {tip}",
            allowed_mentions=discord.AllowedMentions.none(),
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Hello(bot))
