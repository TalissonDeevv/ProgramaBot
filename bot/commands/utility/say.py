"""Comando /say: faz o bot enviar uma mensagem no canal.

Por segurança, só quem tem a permissão "Gerenciar mensagens" pode usar,
e o bot nunca marca @everyone, @here ou cargos com esse texto.
"""

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import error_embed, success_embed


class Say(commands.Cog):
    """Cog que contém o /say."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="say", description="Faz o bot enviar uma mensagem neste canal.")
    @app_commands.describe(mensagem="O texto que o bot vai enviar.")
    @app_commands.guild_only()
    # default_permissions: esconde o comando de quem não tem a permissão (configurável pelo servidor).
    @app_commands.default_permissions(manage_messages=True)
    # checks.has_permissions: verificação real, feita pelo bot no momento do uso.
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(send_messages=True)
    async def say(
        self,
        interaction: discord.Interaction,
        mensagem: app_commands.Range[str, 1, 2000],
    ) -> None:
        channel = interaction.channel
        if not isinstance(channel, discord.abc.Messageable):
            await interaction.response.send_message(
                embed=error_embed("Não consigo enviar mensagens neste tipo de canal."), ephemeral=True
            )
            return

        await channel.send(mensagem, allowed_mentions=discord.AllowedMentions.none())
        await interaction.response.send_message(embed=success_embed("Mensagem enviada!"), ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Say(bot))
