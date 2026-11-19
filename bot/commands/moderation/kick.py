"""Comando /kick: expulsa um membro do servidor, com confirmação por botão.

Expulsar não é banir: a pessoa expulsa pode voltar com um novo convite.
"""

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import error_embed, info_embed, success_embed, warning_embed
from bot.utils.moderation import MAX_REASON_LENGTH, build_audit_reason, check_hierarchy
from bot.views.confirm import ConfirmView


class Kick(commands.Cog):
    """Cog que contém o /kick."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="kick", description="Expulsa um membro do servidor.")
    @app_commands.describe(membro="Quem será expulso.", motivo="Motivo (aparece no registro de auditoria).")
    @app_commands.guild_only()
    @app_commands.default_permissions(kick_members=True)
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.checks.bot_has_permissions(kick_members=True)
    async def kick(
        self,
        interaction: discord.Interaction,
        membro: discord.Member,
        motivo: app_commands.Range[str, 1, MAX_REASON_LENGTH] | None = None,
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
            embed=warning_embed(f"Tem certeza que deseja **expulsar** {membro.mention}?"),
            view=view,
            ephemeral=True,
        )
        await view.wait()  # Espera um clique ou o tempo acabar.

        if view.confirmed is None:
            await interaction.edit_original_response(embed=info_embed("Tempo esgotado. Nada foi feito."), view=None)
            return
        if not view.confirmed:
            await interaction.edit_original_response(embed=info_embed("Ação cancelada."), view=None)
            return

        try:
            await membro.kick(reason=build_audit_reason(motivo, interaction.user, "kick"))
        except discord.HTTPException:
            await interaction.edit_original_response(
                embed=error_embed("O Discord não permitiu a expulsão. Verifique minhas permissões e meu cargo."),
                view=None,
            )
            return

        await interaction.edit_original_response(
            embed=success_embed(f"👢 **{membro}** foi expulso(a).\nMotivo: {motivo or 'não informado'}"),
            view=None,
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Kick(bot))
