"""Evento on_ready: avisa no terminal quando o bot está online.

Atenção: o Discord pode disparar ``on_ready`` mais de uma vez (por exemplo,
depois de uma reconexão). Por isso, não coloque aqui código que só pode rodar
uma vez, como carregar extensões. Para isso existe o ``setup_hook``.
"""

import logging

from discord.ext import commands

logger = logging.getLogger(__name__)


class Ready(commands.Cog):
    """Cog que escuta o evento on_ready."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        user = self.bot.user
        if user is None:
            return
        logger.info("Conectado como %s (ID: %s)", user, user.id)
        logger.info("Presente em %d servidor(es). Latência: %.0f ms", len(self.bot.guilds), self.bot.latency * 1000)
        logger.info("ProgramaBot pronto! Use /help no Discord.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ready(bot))
