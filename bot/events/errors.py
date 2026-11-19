"""Tratamento central de erros dos comandos.

Quando um comando falha (falta de permissão, cooldown, erro no código...),
o discord.py chama um *error handler*. Aqui transformamos esses erros em
mensagens amigáveis para o usuário e registramos os erros inesperados no log.
"""

import logging

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import error_embed

logger = logging.getLogger(__name__)

# Tradução dos nomes de permissão que aparecem nos nossos comandos.
PERMISSION_NAMES = {
    "ban_members": "Banir membros",
    "kick_members": "Expulsar membros",
    "manage_messages": "Gerenciar mensagens",
    "moderate_members": "Castigar membros",
    "read_message_history": "Ver histórico de mensagens",
    "send_messages": "Enviar mensagens",
}

UNEXPECTED_ERROR_MESSAGE = "Ocorreu um erro inesperado. O problema foi registrado no log do bot."


def format_permissions(permissions: list[str]) -> str:
    """Converte ``["kick_members"]`` em ``"Expulsar membros"``."""
    return ", ".join(PERMISSION_NAMES.get(name, name.replace("_", " ")) for name in permissions)


def describe_app_command_error(error: app_commands.AppCommandError) -> str | None:
    """Retorna uma mensagem amigável para erros conhecidos, ou ``None`` para os inesperados.

    A ordem dos ``if`` importa: MissingPermissions, BotMissingPermissions e
    NoPrivateMessage são tipos especiais de CheckFailure, então vêm antes dele.
    """
    if isinstance(error, app_commands.MissingPermissions):
        return f"Você precisa da permissão: **{format_permissions(error.missing_permissions)}**."
    if isinstance(error, app_commands.BotMissingPermissions):
        return f"Eu preciso da permissão: **{format_permissions(error.missing_permissions)}**."
    if isinstance(error, app_commands.CommandOnCooldown):
        return f"Calma! Você poderá usar este comando de novo em {error.retry_after:.0f} segundo(s)."
    if isinstance(error, app_commands.NoPrivateMessage):
        return "Este comando só funciona dentro de servidores."
    if isinstance(error, app_commands.CheckFailure):
        return "Você não pode usar este comando aqui."
    return None


class ErrorHandler(commands.Cog):
    """Cog que registra os tratadores de erro de slash commands e de comandos de prefixo."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._previous_tree_error = bot.tree.on_error

    async def cog_load(self) -> None:
        # Substituímos o tratador padrão da árvore de slash commands pelo nosso.
        self.bot.tree.on_error = self.on_app_command_error

    async def cog_unload(self) -> None:
        self.bot.tree.on_error = self._previous_tree_error

    async def on_app_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ) -> None:
        """Chamado quando um slash command gera um erro."""
        message = describe_app_command_error(error)
        if message is None:
            command_name = interaction.command.name if interaction.command else "desconhecido"
            logger.error("Erro inesperado no comando /%s", command_name, exc_info=error)
            message = UNEXPECTED_ERROR_MESSAGE

        embed = error_embed(message)
        try:
            # Se o comando já respondeu (ou usou defer), precisamos usar followup.
            if interaction.response.is_done():
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.HTTPException:
            logger.warning("Não foi possível avisar o usuário sobre o erro.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        """Chamado quando um comando de PREFIXO gera um erro."""
        # Se o comando tem tratador próprio (como o !soma), deixamos ele cuidar.
        if ctx.command is not None and ctx.command.has_error_handler():
            return
        if isinstance(error, commands.CommandNotFound):
            return  # Ignora mensagens como "!algo" que não são comandos nossos.
        if isinstance(error, commands.UserInputError):
            await ctx.send(f"Uso incorreto do comando. Verifique os parâmetros. ({error})")
            return
        logger.error("Erro inesperado no comando de prefixo %s", ctx.command, exc_info=error)
        await ctx.send(UNEXPECTED_ERROR_MESSAGE)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ErrorHandler(bot))
