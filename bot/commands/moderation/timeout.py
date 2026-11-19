"""Comando /timeout: silencia um membro por um tempo (recurso nativo do Discord).

Durante o castigo, o membro não pode enviar mensagens, reagir ou falar em canais de voz.
Use ``duracao:remover`` para tirar o castigo antes do tempo.
"""

from datetime import timedelta

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import error_embed, success_embed
from bot.utils.moderation import MAX_REASON_LENGTH, build_audit_reason, check_hierarchy
from bot.utils.time_parser import TimeParseError, format_duration, parse_duration

# Limite definido pelo próprio Discord.
MAX_TIMEOUT = timedelta(days=28)
REMOVE_WORDS = ("0", "remover", "nenhum")


class Timeout(commands.Cog):
    """Cog que contém o /timeout."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="timeout", description="Silencia um membro temporariamente.")
    @app_commands.describe(
        membro="Quem será silenciado.",
        duracao="Por quanto tempo. Ex.: 10m, 1h, 2d (máx. 28d). Use 'remover' para tirar o castigo.",
        motivo="Motivo (aparece no registro de auditoria).",
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(moderate_members=True)
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.checks.bot_has_permissions(moderate_members=True)
    async def timeout(
        self,
        interaction: discord.Interaction,
        membro: discord.Member,
        duracao: str,
        motivo: app_commands.Range[str, 1, MAX_REASON_LENGTH] | None = None,
    ) -> None:
        guild = interaction.guild
        if guild is None or not isinstance(interaction.user, discord.Member):
            return

        problem = check_hierarchy(interaction.user, membro, guild.me, guild.owner_id)
        if problem:
            await interaction.response.send_message(embed=error_embed(problem), ephemeral=True)
            return

        audit_reason = build_audit_reason(motivo, interaction.user, "timeout")

        if duracao.strip().lower() in REMOVE_WORDS:
            delta = None  # None remove o castigo.
        else:
            try:
                delta = parse_duration(duracao)
            except TimeParseError as error:
                await interaction.response.send_message(embed=error_embed(str(error)), ephemeral=True)
                return
            if delta > MAX_TIMEOUT:
                await interaction.response.send_message(
                    embed=error_embed("O Discord permite no máximo 28 dias de castigo."), ephemeral=True
                )
                return

        try:
            await membro.timeout(delta, reason=audit_reason)
        except discord.HTTPException:
            await interaction.response.send_message(
                embed=error_embed(
                    "O Discord não permitiu a ação. Administradores não podem receber castigo, "
                    "e meu cargo precisa estar acima do cargo do membro."
                ),
                ephemeral=True,
            )
            return

        if delta is None:
            message = f"🔊 O castigo de {membro.mention} foi removido."
        else:
            message = f"🔇 {membro.mention} foi silenciado(a) por **{format_duration(delta)}**."
        await interaction.response.send_message(
            embed=success_embed(f"{message}\nMotivo: {motivo or 'não informado'}"),
            allowed_mentions=discord.AllowedMentions.none(),
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Timeout(bot))
