"""Comando /userinfo: mostra informações de um membro do servidor."""

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import base_embed

MAX_ROLES_SHOWN = 10


def format_roles(member: discord.Member) -> str:
    """Lista os cargos do membro, do mais alto para o mais baixo, sem o @everyone."""
    # member.roles vem do mais baixo para o mais alto; [1:] remove o @everyone.
    roles = list(reversed(member.roles[1:]))
    if not roles:
        return "Nenhum cargo"
    mentions = [role.mention for role in roles[:MAX_ROLES_SHOWN]]
    hidden = len(roles) - MAX_ROLES_SHOWN
    if hidden > 0:
        mentions.append(f"e mais {hidden}")
    return ", ".join(mentions)


class UserInfo(commands.Cog):
    """Cog que contém o /userinfo."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="userinfo", description="Mostra informações de um membro.")
    @app_commands.describe(membro="Membro que você quer consultar (deixe vazio para ver você).")
    @app_commands.guild_only()
    async def userinfo(
        self,
        interaction: discord.Interaction,
        membro: discord.Member | None = None,
    ) -> None:
        target = membro or interaction.user
        # Dentro de um servidor, interaction.user é um discord.Member.
        # Esta verificação protege o código e ajuda o editor a entender o tipo.
        if not isinstance(target, discord.Member):
            await interaction.response.send_message("Use este comando em um servidor.", ephemeral=True)
            return

        embed = base_embed(f"👤 {target.display_name}", color=target.color.value or 0x5865F2)
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(name="Usuário", value=str(target), inline=True)
        embed.add_field(name="ID", value=str(target.id), inline=True)
        embed.add_field(name="É um bot?", value="Sim" if target.bot else "Não", inline=True)
        # format_dt cria uma data que o Discord mostra no fuso horário de quem lê.
        embed.add_field(
            name="Conta criada",
            value=f"{discord.utils.format_dt(target.created_at, 'D')} ({discord.utils.format_dt(target.created_at, 'R')})",
            inline=False,
        )
        if target.joined_at is not None:
            embed.add_field(
                name="Entrou no servidor",
                value=f"{discord.utils.format_dt(target.joined_at, 'D')} ({discord.utils.format_dt(target.joined_at, 'R')})",
                inline=False,
            )
        embed.add_field(name="Cargo mais alto", value=target.top_role.mention, inline=False)
        embed.add_field(name=f"Cargos ({len(target.roles) - 1})", value=format_roles(target), inline=False)

        await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions.none())


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UserInfo(bot))
