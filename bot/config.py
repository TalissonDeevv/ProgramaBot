"""Carrega e valida as configurações do ProgramaBot.

As configurações ficam no arquivo ``.env`` (que nunca deve ir para o GitHub).
Este módulo lê esse arquivo, converte cada valor para o tipo correto e
reúne tudo em um único objeto ``Settings``.
"""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Pasta raiz do projeto (a pasta que contém bot/, education/, README.md...).
# __file__ é o caminho deste arquivo: .../ProgramaBot/bot/config.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Texto usado no .env.example. Se o token ainda for esse, o estudante
# esqueceu de colocar o token verdadeiro.
TOKEN_PLACEHOLDER = "cole_seu_token_aqui"

VALID_LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
DEFAULT_DATABASE_PATH = PROJECT_ROOT / "data" / "programabot.db"

TRUE_VALUES = ("1", "true", "sim", "yes", "on")
FALSE_VALUES = ("0", "false", "nao", "não", "no", "off")


class ConfigError(Exception):
    """Erro lançado quando uma configuração está ausente ou inválida."""


@dataclass(frozen=True)
class Settings:
    """Todas as configurações do bot, já convertidas e validadas.

    ``frozen=True`` impede que alguém altere os valores depois de criados,
    evitando que uma parte do código mude a configuração "sem querer".
    """

    token: str
    prefix: str = "!"
    guild_id: int | None = None
    welcome_channel_id: int | None = None
    log_level: str = "INFO"
    database_path: Path = DEFAULT_DATABASE_PATH
    enable_members_intent: bool = True
    enable_message_content_intent: bool = True
    sync_commands: bool = True


def parse_optional_id(name: str, value: str | None) -> int | None:
    """Converte um texto em ID do Discord (número inteiro positivo).

    Retorna ``None`` quando a variável não foi preenchida.
    """
    if value is None or value.strip() == "":
        return None
    try:
        number = int(value.strip())
    except ValueError:
        raise ConfigError(
            f"A variável {name} deve conter apenas números (um ID do Discord). "
            f"Valor recebido: {value!r}"
        ) from None
    if number <= 0:
        raise ConfigError(f"A variável {name} deve ser um número positivo.")
    return number


def parse_bool(name: str, value: str | None, default: bool) -> bool:
    """Converte textos como "true", "sim" ou "0" em ``True``/``False``."""
    if value is None or value.strip() == "":
        return default
    normalized = value.strip().lower()
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    raise ConfigError(
        f"A variável {name} deve ser true ou false. Valor recebido: {value!r}"
    )


def load_settings(env_file: Path | None = None) -> Settings:
    """Lê o arquivo ``.env`` e as variáveis de ambiente e devolve um ``Settings``.

    Variáveis já definidas no sistema têm prioridade sobre o arquivo ``.env``
    (comportamento padrão do ``load_dotenv``).
    """
    load_dotenv(env_file or PROJECT_ROOT / ".env")

    token = os.getenv("DISCORD_TOKEN", "").strip()
    if not token or token == TOKEN_PLACEHOLDER:
        raise ConfigError(
            "O token do bot não foi configurado. Copie o arquivo .env.example "
            "para .env e preencha DISCORD_TOKEN com o token do Discord "
            "Developer Portal. Veja education/getting-started/07-configurando-o-env.md"
        )

    prefix = os.getenv("BOT_PREFIX", "!").strip() or "!"
    if " " in prefix or len(prefix) > 5:
        raise ConfigError("BOT_PREFIX deve ter de 1 a 5 caracteres e não pode ter espaços.")

    log_level = os.getenv("LOG_LEVEL", "INFO").strip().upper() or "INFO"
    if log_level not in VALID_LOG_LEVELS:
        raise ConfigError(
            f"LOG_LEVEL inválido: {log_level!r}. Use um destes: {', '.join(VALID_LOG_LEVELS)}"
        )

    raw_database_path = os.getenv("DATABASE_PATH", "").strip()
    database_path = Path(raw_database_path) if raw_database_path else DEFAULT_DATABASE_PATH
    if not database_path.is_absolute():
        database_path = PROJECT_ROOT / database_path

    return Settings(
        token=token,
        prefix=prefix,
        guild_id=parse_optional_id("GUILD_ID", os.getenv("GUILD_ID")),
        welcome_channel_id=parse_optional_id("WELCOME_CHANNEL_ID", os.getenv("WELCOME_CHANNEL_ID")),
        log_level=log_level,
        database_path=database_path,
        enable_members_intent=parse_bool(
            "ENABLE_MEMBERS_INTENT", os.getenv("ENABLE_MEMBERS_INTENT"), default=True
        ),
        enable_message_content_intent=parse_bool(
            "ENABLE_MESSAGE_CONTENT_INTENT", os.getenv("ENABLE_MESSAGE_CONTENT_INTENT"), default=True
        ),
        sync_commands=parse_bool("SYNC_COMMANDS", os.getenv("SYNC_COMMANDS"), default=True),
    )
