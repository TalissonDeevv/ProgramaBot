"""Evento on_member_join: dá boas-vindas a quem entra no servidor.

Requer a intent privilegiada SERVER MEMBERS (``intents.members``). Sem ela,
o Discord simplesmente não envia esse evento para o bot.
"""

import logging

import discord
from discord.ext import commands

from bot.utils.embeds import SUCCESS_COLOR, base_embed

logger = logging.getLogger(__name__)


def get_welcome_channel(guild: discord.Guild, channel_id: int | None) -> discord.TextChannel | None:
    """Escolhe o canal de boas-vindas.

    1. Usa o canal configurado em WELCOME_CHANNEL_ID, se existir neste servidor.
    2. Senão, usa o "canal de mensagens do sistema" definido nas configurações do servidor.
    3. Só retorna o canal se o bot puder enviar mensagens nele.
    """
    channel = guild.get_channel(channel_id) if channel_id else None
    if not isinstance(channel, discord.TextChannel):
        channel = guild.system_channel
    if channel is None:
        return None
    if not channel.permissions_for(guild.me).send_messages:
        return None
    return channel


class MemberJoin(commands.Cog):
    """Cog que escuta o evento on_member_join."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def cog_load(self) -> None:
        if not self.bot.intents.members:
            logger.warning("Intent 'members' desativada: as boas-vindas não vão funcionar.")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        channel = get_welcome_channel(member.guild, self.bot.settings.welcome_channel_id)
        if channel is None:
            return

        embed = base_embed(
            "👋 Boas-vindas!",
            f"Olá, {member.mention}! Seja bem-vindo(a) ao **{member.guild.name}**.\n"
            f"Você é o membro número **{member.guild.member_count}**. Use `/help` para começar.",
            SUCCESS_COLOR,
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        try:
            await channel.send(embed=embed)
        except discord.HTTPException:
            logger.warning("Não consegui enviar a mensagem de boas-vindas em #%s.", channel.name)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MemberJoin(bot))
