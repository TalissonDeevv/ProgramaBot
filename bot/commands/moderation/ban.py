"""Comando /ban: bane um membro do servidor, com confirmação por botão.

Um banimento impede a pessoa de voltar até que alguém use ``/unban``.
"""

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import error_embed, info_embed, success_embed, warning_embed
from bot.utils.moderation import MAX_REASON_LENGTH, build_audit_reason, check_hierarchy
from bot.views.confirm import ConfirmView

SECONDS_PER_DAY = 86_400


class Ban(commands.Cog):
    """Cog que contém o /ban."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ban", description="Bane um membro do servidor.")
    @app_commands.describe(
        membro="Quem será banido.",
        motivo="Motivo (aparece no registro de auditoria).",
        apagar_mensagens_dias="Apagar as mensagens dos últimos X dias (0 a 7).",
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(ban_members=True)
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        membro: discord.Member,
        motivo: app_commands.Range[str, 1, MAX_REASON_LENGTH] | None = None,
        apagar_mensagens_dias: app_commands.Range[int, 0, 7] = 0,
    ) -> None:
        guild = interaction.guild
        if guild is None or not isinstance(interaction.user, discord.Member):
            return

        problem = check_hierarchy(interaction.user, membro, guild.me, guild.owner_id)
        if problem:
            await interaction.response.send_message(embed=error_embed(problem), ephemeral=True)
            return

        view = ConfirmView(author_id=interaction.user.id)
        await interaction.response.send_message(
            embed=warning_embed(f"Tem certeza que deseja **banir** {membro.mention}?"),
            view=view,
            ephemeral=True,
        )
        await view.wait()

        if view.confirmed is None:
            await interaction.edit_original_response(embed=info_embed("Tempo esgotado. Nada foi feito."), view=None)
            return
        if not view.confirmed:
            await interaction.edit_original_response(embed=info_embed("Ação cancelada."), view=None)
            return

        try:
            await guild.ban(
                membro,
                reason=build_audit_reason(motivo, interaction.user, "ban"),
                delete_message_seconds=apagar_mensagens_dias * SECONDS_PER_DAY,
            )
        except discord.HTTPException:
            await interaction.edit_original_response(
                embed=error_embed("O Discord não permitiu o banimento. Verifique minhas permissões e meu cargo."),
                view=None,
            )
            return

        await interaction.edit_original_response(
            embed=success_embed(f"🔨 **{membro}** foi banido(a).\nMotivo: {motivo or 'não informado'}"),
            view=None,
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ban(bot))
