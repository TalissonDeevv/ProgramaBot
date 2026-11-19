"""Funções que criam embeds padronizados.

Um *embed* é aquela caixinha colorida que os bots enviam no Discord, com título,
descrição, campos e imagem. Centralizar a criação aqui garante que todas as
respostas do bot tenham a mesma aparência.
"""

from datetime import datetime, timezone

import discord

# Cores em hexadecimal (o mesmo formato usado em sites: #5865F2).
PRIMARY_COLOR = 0x5865F2  # azul do Discord
SUCCESS_COLOR = 0x57F287  # verde
WARNING_COLOR = 0xFEE75C  # amarelo
ERROR_COLOR = 0xED4245  # vermelho
INFO_COLOR = 0x3498DB  # azul claro

FOOTER_TEXT = "ProgramaBot • aprenda programando"
HEX_DIGITS = "0123456789abcdefABCDEF"


def base_embed(
    title: str,
    description: str | None = None,
    color: int = PRIMARY_COLOR,
) -> discord.Embed:
    """Cria um embed com o rodapé e o horário padrão do ProgramaBot."""
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_footer(text=FOOTER_TEXT)
    return embed


def success_embed(description: str, title: str = "✅ Tudo certo!") -> discord.Embed:
    """Embed verde, usado quando uma ação deu certo."""
    return base_embed(title, description, SUCCESS_COLOR)


def error_embed(description: str, title: str = "❌ Algo deu errado") -> discord.Embed:
    """Embed vermelho, usado para explicar erros ao usuário."""
    return base_embed(title, description, ERROR_COLOR)


def warning_embed(description: str, title: str = "⚠️ Atenção") -> discord.Embed:
    """Embed amarelo, usado para confirmações e avisos."""
    return base_embed(title, description, WARNING_COLOR)


def info_embed(description: str, title: str = "ℹ️ Informação") -> discord.Embed:
    """Embed azul, usado para respostas informativas."""
    return base_embed(title, description, INFO_COLOR)


def parse_hex_color(value: str, default: int = PRIMARY_COLOR) -> int:
    """Converte um texto como ``#FF0000`` em um número de cor.

    Raises:
        ValueError: se o texto não for uma cor hexadecimal de 6 dígitos.
    """
    cleaned = value.strip().removeprefix("#")
    if cleaned == "":
        return default
    if len(cleaned) != 6 or any(character not in HEX_DIGITS for character in cleaned):
        raise ValueError(
            "Cor inválida. Use 6 dígitos hexadecimais, por exemplo: #5865F2 ou FF0000."
        )
    return int(cleaned, 16)
