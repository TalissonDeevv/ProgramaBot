"""Testes de bot/config.py."""

from pathlib import Path

import pytest

from bot.config import (
    DEFAULT_DATABASE_PATH,
    PROJECT_ROOT,
    TOKEN_PLACEHOLDER,
    ConfigError,
    load_settings,
    parse_bool,
    parse_optional_id,
)

ENV_VARS = (
    "DISCORD_TOKEN",
    "GUILD_ID",
    "BOT_PREFIX",
    "WELCOME_CHANNEL_ID",
    "LOG_LEVEL",
    "DATABASE_PATH",
    "ENABLE_MEMBERS_INTENT",
    "ENABLE_MESSAGE_CONTENT_INTENT",
    "SYNC_COMMANDS",
)


@pytest.fixture
def clean_env(monkeypatch, tmp_path):
    """Remove as variáveis do ambiente e aponta para um .env inexistente."""
    for name in ENV_VARS:
        monkeypatch.delenv(name, raising=False)
    return tmp_path / "nao-existe.env"


def test_missing_token_raises(clean_env):
    with pytest.raises(ConfigError, match="token"):
        load_settings(clean_env)


def test_placeholder_token_raises(clean_env, monkeypatch):
    monkeypatch.setenv("DISCORD_TOKEN", TOKEN_PLACEHOLDER)
    with pytest.raises(ConfigError):
        load_settings(clean_env)


def test_defaults(clean_env, monkeypatch):
    monkeypatch.setenv("DISCORD_TOKEN", "abc")
    settings = load_settings(clean_env)
    assert settings.token == "abc"
    assert settings.prefix == "!"
    assert settings.guild_id is None
    assert settings.log_level == "INFO"
    assert settings.database_path == DEFAULT_DATABASE_PATH
    assert settings.enable_members_intent is True
    assert settings.sync_commands is True


def test_custom_values(clean_env, monkeypatch):
    monkeypatch.setenv("DISCORD_TOKEN", "abc")
    monkeypatch.setenv("GUILD_ID", "123456789")
    monkeypatch.setenv("BOT_PREFIX", "?")
    monkeypatch.setenv("LOG_LEVEL", "debug")
    monkeypatch.setenv("DATABASE_PATH", "outra/pasta.db")
    monkeypatch.setenv("ENABLE_MESSAGE_CONTENT_INTENT", "false")
    settings = load_settings(clean_env)
    assert settings.guild_id == 123456789
    assert settings.prefix == "?"
    assert settings.log_level == "DEBUG"
    assert settings.database_path == PROJECT_ROOT / "outra" / "pasta.db"
    assert settings.enable_message_content_intent is False


def test_env_file_is_read(clean_env, tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("DISCORD_TOKEN=do-arquivo\nBOT_PREFIX=$\n", encoding="utf-8")
    settings = load_settings(env_file)
    assert settings.token == "do-arquivo"
    assert settings.prefix == "$"


@pytest.mark.parametrize(
    ("name", "value"),
    [("LOG_LEVEL", "barulhento"), ("BOT_PREFIX", "um prefixo"), ("GUILD_ID", "abc")],
)
def test_invalid_values_raise(clean_env, monkeypatch, name, value):
    monkeypatch.setenv("DISCORD_TOKEN", "abc")
    monkeypatch.setenv(name, value)
    with pytest.raises(ConfigError):
        load_settings(clean_env)


def test_parse_optional_id():
    assert parse_optional_id("X", None) is None
    assert parse_optional_id("X", "  ") is None
    assert parse_optional_id("X", " 42 ") == 42
    with pytest.raises(ConfigError):
        parse_optional_id("X", "-5")


@pytest.mark.parametrize("text", ["true", "SIM", "1", "on"])
def test_parse_bool_true(text):
    assert parse_bool("X", text, default=False) is True


@pytest.mark.parametrize("text", ["false", "não", "0", "off"])
def test_parse_bool_false(text):
    assert parse_bool("X", text, default=True) is False


def test_parse_bool_default_and_invalid():
    assert parse_bool("X", None, default=True) is True
    with pytest.raises(ConfigError):
        parse_bool("X", "talvez", default=True)


def test_project_root_points_to_repository():
    assert (PROJECT_ROOT / "bot" / "config.py").is_file()
    assert isinstance(PROJECT_ROOT, Path)
