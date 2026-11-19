"""Comando /dice: rola um ou mais dados.

Bom para estudar o módulo ``random``, listas, ``sum()`` e compreensão de listas.
"""

import random

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import base_embed


def roll_dice(sides: int, amount: int) -> list[int]:
    """Rola ``amount`` dados de ``sides`` lados e devolve a lista de resultados."""
    if sides < 2:
        raise ValueError("Um dado precisa ter pelo menos 2 lados.")
    if amount < 1:
        raise ValueError("É preciso rolar pelo menos 1 dado.")
    # Compreensão de lista: repete random.randint "amount" vezes.
    return [random.randint(1, sides) for _ in range(amount)]


class Dice(commands.Cog):
    """Cog que contém o /dice."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="dice", description="Rola um ou mais dados.")
    @app_commands.describe(lados="Quantos lados cada dado tem (2 a 1000).", quantidade="Quantos dados rolar (1 a 10).")
    async def dice(
        self,
        interaction: discord.Interaction,
        lados: app_commands.Range[int, 2, 1000] = 6,
        quantidade: app_commands.Range[int, 1, 10] = 1,
    ) -> None:
        results = roll_dice(lados, quantidade)
        embed = base_embed(f"🎲 {quantidade}d{lados}", f"Resultados: **{', '.join(map(str, results))}**")
        if quantidade > 1:
            embed.add_field(name="Soma", value=str(sum(results)))
            embed.add_field(name="Maior", value=str(max(results)))
            embed.add_field(name="Menor", value=str(min(results)))
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Dice(bot))
