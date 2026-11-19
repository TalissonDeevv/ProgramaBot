"""O menor bot possível com um slash command, em um único arquivo.

Use este exemplo para entender a base de qualquer bot, sem Cogs nem extensões.
Depois, compare com a estrutura organizada do ProgramaBot (bot/main.py).

Como executar (a partir da pasta raiz do ProgramaBot, com o ambiente virtual ativo):

    1. Garanta que o .env tem DISCORD_TOKEN preenchido.
    2. python examples/minimal-bot/bot_minimo.py
    3. No Discord, use /oi (pode levar alguns minutos para aparecer globalmente).
"""

import os

import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()  # lê o .env da pasta atual
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents padrão bastam para slash commands.
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)  # onde os slash commands ficam registrados


@tree.command(name="oi", description="O bot diz oi para você")
async def oi(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(f"Oi, {interaction.user.display_name}! 👋")


@tree.command(name="somar", description="Soma dois números")
@app_commands.describe(a="Primeiro número", b="Segundo número")
async def somar(interaction: discord.Interaction, a: int, b: int) -> None:
    await interaction.response.send_message(f"{a} + {b} = {a + b}")


@client.event
async def setup_hook() -> None:
    # Registra os comandos no Discord uma vez, antes de conectar.
    await tree.sync()


@client.event
async def on_ready() -> None:
    print(f"Online como {client.user}")


if __name__ == "__main__":
    if not TOKEN or TOKEN == "cole_seu_token_aqui":
        raise SystemExit("Configure DISCORD_TOKEN no arquivo .env antes de executar.")
    client.run(TOKEN)
