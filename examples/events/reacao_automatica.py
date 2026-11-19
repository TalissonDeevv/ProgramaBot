"""MODELO de evento: reage com 👋 a mensagens que contêm "bom dia".

Requer a intent MESSAGE CONTENT (o bot precisa ler o texto das mensagens).

Como usar:
    1. Copie para bot/events/reacao_automatica.py
    2. Crie education/code-explanation/events/reacao_automatica.md (o teste exige!)
    3. Reinicie o bot.
"""

import discord
from discord.ext import commands

PALAVRAS_GATILHO = ("bom dia", "boa tarde", "boa noite")


def deve_reagir(conteudo: str) -> bool:
    """Lógica separada, fácil de testar."""
    texto = conteudo.lower()
    return any(palavra in texto for palavra in PALAVRAS_GATILHO)


class ReacaoAutomatica(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:  # nunca reagir a bots
            return
        if deve_reagir(message.content):
            try:
                await message.add_reaction("👋")
            except discord.HTTPException:
                pass  # sem permissão para reagir neste canal


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ReacaoAutomatica(bot))
