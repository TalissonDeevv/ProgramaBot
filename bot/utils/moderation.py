"""Regras de segurança compartilhadas pelos comandos de moderação.

No Discord, cada membro tem cargos (roles) organizados em uma hierarquia.
Um moderador não deveria conseguir expulsar alguém com um cargo igual ou
maior que o dele. Este módulo verifica essas regras ANTES de o bot tentar
executar a ação, para mostrar uma mensagem clara ao usuário.
"""

import discord

MAX_REASON_LENGTH = 400
DEFAULT_REASON = "Nenhum motivo informado."


def check_hierarchy(
    actor: discord.Member,
    target: discord.Member,
    bot_member: discord.Member,
    guild_owner_id: int,
) -> str | None:
    """Verifica se ``actor`` pode moderar ``target``.

    Args:
        actor: quem executou o comando.
        target: quem vai sofrer a ação.
        bot_member: o próprio bot dentro do servidor (``guild.me``).
        guild_owner_id: ID do dono do servidor.

    Returns:
        ``None`` quando a ação é permitida, ou um texto explicando o bloqueio.
    """
    if target.id == actor.id:
        return "Você não pode usar esse comando em si mesmo."
    if target.id == bot_member.id:
        return "Eu não posso aplicar essa ação em mim mesmo."
    if target.id == guild_owner_id:
        return "Ninguém pode aplicar essa ação no dono do servidor."
    if actor.id != guild_owner_id and actor.top_role <= target.top_role:
        return "Você não pode moderar alguém com cargo igual ou superior ao seu."
    if bot_member.top_role <= target.top_role:
        return (
            "Meu cargo está abaixo (ou no mesmo nível) do cargo desse membro. "
            "Mova o cargo do ProgramaBot para cima nas configurações do servidor."
        )
    return None


def build_audit_reason(reason: str | None, moderator: discord.abc.User, command_name: str) -> str:
    """Monta o texto que aparece no Registro de Auditoria do servidor."""
    text = (reason or DEFAULT_REASON).strip()[:MAX_REASON_LENGTH]
    return f"{text} | por {moderator} via /{command_name}"
