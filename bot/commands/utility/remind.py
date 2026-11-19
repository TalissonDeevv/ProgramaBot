"""Comando /remind: cria lembretes que sobrevivem a reinicializações do bot.

Como funciona:

1. O usuário usa ``/remind tempo:10m mensagem:Estudar Python``.
2. O lembrete é salvo no SQLite (``bot/database/reminders.py``).
3. Uma tarefa em segundo plano (``tasks.loop``) verifica o banco a cada 30 segundos.
4. Quando chega a hora, o bot envia a mensagem no canal e apaga o lembrete.
"""

import logging
from datetime import datetime, timedelta, timezone

import discord
from discord import app_commands
from discord.ext import commands, tasks

from bot.database.reminders import Reminder, ReminderRepository
from bot.utils.embeds import error_embed, info_embed, success_embed
from bot.utils.time_parser import TimeParseError, format_duration, parse_duration

logger = logging.getLogger(__name__)

MAX_DURATION = timedelta(days=7)
MAX_REMINDERS_PER_USER = 10
CHECK_INTERVAL_SECONDS = 30


class Remind(commands.Cog):
    """Cog com o /remind e a tarefa que entrega os lembretes."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.repository = ReminderRepository(bot.settings.database_path)

    async def cog_load(self) -> None:
        """Chamado automaticamente quando o Cog é carregado."""
        self.repository.setup()
        self.check_reminders.start()

    async def cog_unload(self) -> None:
        """Chamado quando o Cog é descarregado: para a tarefa em segundo plano."""
        self.check_reminders.cancel()

    @app_commands.command(name="remind", description="Cria um lembrete para você.")
    @app_commands.describe(
        tempo="Daqui a quanto tempo. Exemplos: 30s, 10m, 2h, 1d12h (máximo 7 dias).",
        mensagem="Do que você quer ser lembrado.",
    )
    @app_commands.guild_only()
    async def remind(
        self,
        interaction: discord.Interaction,
        tempo: str,
        mensagem: app_commands.Range[str, 1, 300],
    ) -> None:
        try:
            delay = parse_duration(tempo)
        except TimeParseError as error:
            await interaction.response.send_message(embed=error_embed(str(error)), ephemeral=True)
            return

        if delay > MAX_DURATION:
            await interaction.response.send_message(
                embed=error_embed("O tempo máximo para um lembrete é de 7 dias."), ephemeral=True
            )
            return

        if self.repository.count_for_user(interaction.user.id) >= MAX_REMINDERS_PER_USER:
            await interaction.response.send_message(
                embed=error_embed(f"Você já tem {MAX_REMINDERS_PER_USER} lembretes pendentes."),
                ephemeral=True,
            )
            return

        remind_at = datetime.now(timezone.utc) + delay
        reminder_id = self.repository.add(
            user_id=interaction.user.id,
            channel_id=interaction.channel_id,
            message=mensagem,
            remind_at=remind_at,
        )
        await interaction.response.send_message(
            embed=success_embed(
                f"Lembrete **#{reminder_id}** criado! Vou te avisar neste canal "
                f"{discord.utils.format_dt(remind_at, 'R')} (daqui a {format_duration(delay)})."
            ),
            ephemeral=True,
        )

    @tasks.loop(seconds=CHECK_INTERVAL_SECONDS)
    async def check_reminders(self) -> None:
        """Roda a cada 30 segundos procurando lembretes vencidos."""
        for reminder in self.repository.get_due():
            try:
                await self._deliver(reminder)
            except Exception:
                # Um erro em um lembrete não pode parar a tarefa inteira.
                logger.exception("Erro ao entregar o lembrete #%s", reminder.id)
            finally:
                self.repository.delete(reminder.id)

    @check_reminders.before_loop
    async def before_check_reminders(self) -> None:
        """Espera o bot conectar antes de começar a verificar."""
        await self.bot.wait_until_ready()

    async def _deliver(self, reminder: Reminder) -> None:
        """Envia o lembrete no canal onde ele foi criado."""
        channel = self.bot.get_channel(reminder.channel_id)
        if channel is None:
            try:
                channel = await self.bot.fetch_channel(reminder.channel_id)
            except discord.HTTPException:
                logger.warning("Canal %s do lembrete #%s não está acessível.", reminder.channel_id, reminder.id)
                return

        if not isinstance(channel, discord.abc.Messageable):
            return

        await channel.send(
            content=f"<@{reminder.user_id}>",
            embed=info_embed(reminder.message, title="⏰ Lembrete"),
            # Só a pessoa que criou o lembrete é marcada; @everyone e cargos ficam bloqueados.
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True),
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Remind(bot))
