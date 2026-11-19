"""Comando /calculator: calcula expressões matemáticas sem usar eval().

Toda a lógica matemática fica em ``bot/utils/calculator.py``. Separar a lógica
do comando permite testá-la sem precisar do Discord (veja tests/test_calculator.py).
"""

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.calculator import MAX_EXPRESSION_LENGTH, CalculatorError, calculate, format_result
from bot.utils.embeds import error_embed, success_embed


class Calculator(commands.Cog):
    """Cog que contém o /calculator."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="calculator", description="Calcula uma expressão matemática.")
    @app_commands.describe(expressao="Exemplo: 2 + 3 * (4 - 1). Operadores: + - * / // % **")
    async def calculator(
        self,
        interaction: discord.Interaction,
        expressao: app_commands.Range[str, 1, MAX_EXPRESSION_LENGTH],
    ) -> None:
        try:
            result = calculate(expressao)
        except CalculatorError as error:
            await interaction.response.send_message(embed=error_embed(str(error)), ephemeral=True)
            return

        embed = success_embed(
            f"```\n{expressao}\n= {format_result(result)}\n```",
            title="🧮 Calculadora",
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Calculator(bot))
