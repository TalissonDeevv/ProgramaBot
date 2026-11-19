"""Evento on_message: reage quando alguém menciona o bot.

O evento ``on_message`` é disparado para TODA mensagem que o bot consegue ver.
Usar ``@commands.Cog.listener()`` adiciona um "ouvinte" extra, sem substituir
o processamento dos comandos de prefixo que o ``commands.Bot`` já faz.
"""

import discord
from discord.ext import commands


def is_only_mention(content: str, bot_id: int) -> bool:
    """Verifica se a mensagem contém apenas a menção ao bot (ex.: ``<@123>``)."""
    return content.strip() in (f"<@{bot_id}>", f"<@!{bot_id}>")


class Message(commands.Cog):
    """Cog que escuta o evento on_message."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        # Nunca responda outros bots (nem a si mesmo): evita loops infinitos.
        if message.author.bot or self.bot.user is None:
            return

        if is_only_mention(message.content, self.bot.user.id):
            await message.reply(
                f"Olá, {message.author.display_name}! Eu sou o ProgramaBot. 🤖\n"
                f"Use `/help` para ver meus comandos ou `{self.bot.settings.prefix}ping` "
                "para testar um comando de prefixo.",
                mention_author=False,
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Message(bot))
