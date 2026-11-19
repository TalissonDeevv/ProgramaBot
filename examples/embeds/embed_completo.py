"""MODELO: um embed usando todos os recursos principais.

Copie para bot/commands/<categoria>/ para testar no Discord com /embed-exemplo.
Também é possível só montar o embed e inspecioná-lo no terminal:

    python -c "from examples.embeds.embed_completo import criar_embed_completo; print(criar_embed_completo('Ana').to_dict())"
"""

from datetime import datetime, timezone

import discord
from discord import app_commands
from discord.ext import commands


def criar_embed_completo(nome_autor: str) -> discord.Embed:
    embed = discord.Embed(
        title="Título do embed (até 256 caracteres)",
        description="Descrição com **negrito**, *itálico*, `código` e [links](https://discord.com).",
        color=0x5865F2,
        url="https://github.com/TalissonDeevv/ProgramaBot",  # deixa o título clicável
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_author(name=nome_autor)
    embed.add_field(name="Campo em linha 1", value="Lado a lado", inline=True)
    embed.add_field(name="Campo em linha 2", value="Lado a lado", inline=True)
    embed.add_field(name="Campo em bloco", value="Ocupa a linha inteira", inline=False)
    embed.set_footer(text="Rodapé (até 2048 caracteres)")
    # Imagens precisam de URLs públicas:
    # embed.set_thumbnail(url="https://...")  imagem pequena no canto
    # embed.set_image(url="https://...")      imagem grande embaixo
    return embed


class EmbedExemplo(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="embed-exemplo", description="Mostra um embed com todos os recursos.")
    async def embed_exemplo(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(embed=criar_embed_completo(interaction.user.display_name))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(EmbedExemplo(bot))
