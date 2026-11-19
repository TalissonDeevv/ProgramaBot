"""Comando /poll: cria uma enquete com botões e encerra depois de um tempo.

A lógica e os botões estão em ``bot/views/poll.py``. Este comando valida os
dados, envia a enquete e espera o tempo escolhido usando ``asyncio.sleep``.
"""

import asyncio
from datetime import timedelta

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import error_embed
from bot.views.poll import PollError, PollState, PollView, parse_poll_options


class Poll(commands.Cog):
    """Cog que contém o /poll."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="poll", description="Cria uma enquete com botões.")
    @app_commands.describe(
        pergunta="A pergunta da enquete.",
        opcoes="De 2 a 5 opções separadas por ponto e vírgula. Ex.: Python; JavaScript; Java",
        duracao_minutos="Por quantos minutos a enquete fica aberta (1 a 1440).",
    )
    @app_commands.guild_only()
    async def poll(
        self,
        interaction: discord.Interaction,
        pergunta: app_commands.Range[str, 1, 200],
        opcoes: str,
        duracao_minutos: app_commands.Range[int, 1, 1440] = 10,
    ) -> None:
        try:
            options = parse_poll_options(opcoes)
        except PollError as error:
            await interaction.response.send_message(embed=error_embed(str(error)), ephemeral=True)
            return

        duration = timedelta(minutes=duracao_minutos)
        view = PollView(PollState(pergunta, options), interaction.user.display_name, duration)
        await interaction.response.send_message(
            embed=view.build_embed(), view=view, allowed_mentions=discord.AllowedMentions.none()
        )

        # Guardamos uma referência "parcial" à mensagem. Editar por ela usa o token do bot,
        # que não expira (o token da interação expira em 15 minutos).
        sent_message = await interaction.original_response()
        view.message = sent_message.channel.get_partial_message(sent_message.id)

        # await asyncio.sleep NÃO trava o bot: outros comandos continuam funcionando.
        await asyncio.sleep(duration.total_seconds())
        await view.finish()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Poll(bot))
