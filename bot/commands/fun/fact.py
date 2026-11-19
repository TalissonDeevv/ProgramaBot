"""Comando /fact: mostra uma curiosidade sobre programação.

As curiosidades ficam no arquivo ``bot/data/facts.json``. Guardar dados em um
arquivo separado permite adicionar novas curiosidades sem mexer no código.
"""

import json
import random
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import info_embed

# parents[2] sobe duas pastas: fun/ -> commands/ -> bot/
FACTS_FILE = Path(__file__).resolve().parents[2] / "data" / "facts.json"


def load_facts(path: Path = FACTS_FILE) -> list[str]:
    """Lê o arquivo JSON e devolve a lista de curiosidades.

    Raises:
        ValueError: se o arquivo não tiver uma lista de textos.
    """
    with path.open(encoding="utf-8") as file:
        data = json.load(file)

    facts = data.get("facts") if isinstance(data, dict) else None
    if not isinstance(facts, list) or not facts or not all(isinstance(fact, str) for fact in facts):
        raise ValueError(f"O arquivo {path.name} deve conter {{\"facts\": [\"texto\", ...]}}.")
    return facts


class Fact(commands.Cog):
    """Cog que contém o /fact."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        # Lemos o arquivo uma única vez, quando o Cog é criado.
        self.facts = load_facts()

    @app_commands.command(name="fact", description="Mostra uma curiosidade sobre programação.")
    async def fact(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(embed=info_embed(random.choice(self.facts), title="💡 Você sabia?"))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fact(bot))
