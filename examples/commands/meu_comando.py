"""MODELO de comando para o ProgramaBot.

Como usar:
    1. Copie este arquivo para uma pasta de comandos, por exemplo:
       bot/commands/fun/meu_comando.py
    2. Troque os nomes marcados com "TROQUE".
    3. Reinicie o bot: ele é carregado automaticamente (bot/main.py -> discover_extensions).
    4. Siga o checklist de education/discord-development/10-criando-um-novo-comando.md
       (documentação, catálogo do /help e testes).
"""

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import error_embed, success_embed


def processar_texto(texto: str) -> str:
    """Coloque a lógica em funções separadas: assim dá para testar sem o Discord."""
    return texto[::-1]  # TROQUE: aqui o texto é invertido ("abc" -> "cba")


class MeuComando(commands.Cog):  # TROQUE o nome da classe
    """Descreva aqui o que este Cog faz."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="inverter", description="Inverte um texto.")  # TROQUE nome e descrição
    @app_commands.describe(texto="O texto que será invertido.")
    async def inverter(
        self,
        interaction: discord.Interaction,
        texto: app_commands.Range[str, 1, 200],
    ) -> None:
        resultado = processar_texto(texto)
        if not resultado.strip():
            await interaction.response.send_message(embed=error_embed("Texto vazio."), ephemeral=True)
            return
        await interaction.response.send_message(
            embed=success_embed(resultado, title="🔁 Texto invertido"),
            allowed_mentions=discord.AllowedMentions.none(),
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MeuComando(bot))
