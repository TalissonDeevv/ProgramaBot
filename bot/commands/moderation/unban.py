"""Comando /unban: remove o banimento de um usuário usando o ID dele.

Como a pessoa banida não está mais no servidor, não dá para escolhê-la na
lista de membros. Por isso pedimos o ID (ative o Modo Desenvolvedor do Discord
e clique com o botão direito no usuário > Copiar ID).
"""

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import error_embed, success_embed
from bot.utils.moderation import MAX_REASON_LENGTH, build_audit_reason


def parse_user_id(text: str) -> int | None:
    """Converte o texto em ID. Aceita ``123`` ou uma menção como ``<@123>``."""
    cleaned = text.strip().removeprefix("<@").removeprefix("!").removesuffix(">")
    if not cleaned.isdigit():
        return None
    return int(cleaned)


class Unban(commands.Cog):
    """Cog que contém o /unban."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="unban", description="Remove o banimento de um usuário.")
    @app_commands.describe(usuario_id="ID do usuário banido.", motivo="Motivo (aparece no registro de auditoria).")
    @app_commands.guild_only()
    @app_commands.default_permissions(ban_members=True)
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
    async def unban(
        self,
        interaction: discord.Interaction,
        usuario_id: str,
        motivo: app_commands.Range[str, 1, MAX_REASON_LENGTH] | None = None,
    ) -> None:
        guild = interaction.guild
        if guild is None:
            return

        user_id = parse_user_id(usuario_id)
        if user_id is None:
            await interaction.response.send_message(
                embed=error_embed("ID inválido. Ele deve conter apenas números, como 123456789012345678."),
                ephemeral=True,
            )
            return

        try:
            # discord.Object representa "algo com este ID", sem precisar buscar o usuário.
            await guild.unban(discord.Object(id=user_id), reason=build_audit_reason(motivo, interaction.user, "unban"))
        except discord.NotFound:
            await interaction.response.send_message(
                embed=error_embed("Esse usuário não está banido (ou o ID não existe)."), ephemeral=True
            )
            return
        except discord.HTTPException:
            await interaction.response.send_message(
                embed=error_embed("O Discord não permitiu a ação. Verifique minhas permissões."), ephemeral=True
            )
            return

        await interaction.response.send_message(
            embed=success_embed(f"✅ O banimento de <@{user_id}> foi removido."),
            allowed_mentions=discord.AllowedMentions.none(),
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Unban(bot))
