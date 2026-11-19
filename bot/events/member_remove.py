"""Evento on_member_remove: avisa quando alguém sai do servidor.

Esse evento também é disparado quando um membro é expulso ou banido.
Assim como o on_member_join, requer a intent SERVER MEMBERS.
"""

import logging

import discord
from discord.ext import commands

from bot.events.member_join import get_welcome_channel
from bot.utils.embeds import WARNING_COLOR, base_embed

logger = logging.getLogger(__name__)


class MemberRemove(commands.Cog):
    """Cog que escuta o evento on_member_remove."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        # Reaproveitamos a mesma regra de escolha de canal das boas-vindas.
        channel = get_welcome_channel(member.guild, self.bot.settings.welcome_channel_id)
        if channel is None:
            return

        embed = base_embed(
            "👋 Até logo!",
            f"**{member}** saiu do servidor. Agora somos **{member.guild.member_count}** membros.",
            WARNING_COLOR,
        )
        try:
            await channel.send(embed=embed)
        except discord.HTTPException:
            logger.warning("Não consegui enviar a mensagem de saída em #%s.", channel.name)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MemberRemove(bot))
