"""Testes que carregam todas as extensões do bot sem conectar ao Discord."""

import importlib
from pathlib import Path

import discord
import pytest

from bot.main import ProgramaBot, build_intents, discover_extensions
from bot.views.help_menu import HELP_CATEGORIES, HELP_SELECT_CUSTOM_ID, HelpView, build_category_embed

EXPECTED_SLASH_COMMANDS = {
    "ping", "help", "about", "hello", "calculator",
    "avatar", "userinfo", "serverinfo", "servericon",
    "embed", "poll", "say", "remind",
    "clear", "kick", "ban", "timeout", "unban",
    "dice", "fact",
}
EXPECTED_PREFIX_COMMANDS = {"ping", "hello", "soma"}
MODERATION_PERMISSIONS = {
    "clear": "manage_messages",
    "say": "manage_messages",
    "kick": "kick_members",
    "ban": "ban_members",
    "unban": "ban_members",
    "timeout": "moderate_members",
}


def test_discover_extensions_finds_commands_and_events():
    extensions = discover_extensions()
    assert "bot.commands.general.ping" in extensions
    assert "bot.events.ready" in extensions
    assert not any(name.endswith("__init__") for name in extensions)


@pytest.mark.parametrize("extension", discover_extensions())
def test_every_extension_has_setup_function(extension):
    module = importlib.import_module(extension)
    assert callable(getattr(module, "setup", None)), f"{extension} não tem a função setup"


async def test_all_extensions_load(loaded_bot):
    assert set(loaded_bot.extensions) == set(discover_extensions())


async def test_expected_commands_are_registered(loaded_bot):
    slash_names = {command.name for command in loaded_bot.tree.get_commands()}
    prefix_names = {command.name for command in loaded_bot.commands}
    assert slash_names == EXPECTED_SLASH_COMMANDS
    assert prefix_names == EXPECTED_PREFIX_COMMANDS


async def test_help_catalog_matches_registered_commands(loaded_bot):
    """Garante que o /help nunca fique desatualizado em relação aos comandos reais."""
    catalog = {name for data in HELP_CATEGORIES.values() for name in data["commands"]}
    registered = {command.name for command in loaded_bot.tree.get_commands()}
    assert catalog == registered


async def test_commands_have_descriptions(loaded_bot):
    for command in loaded_bot.tree.get_commands():
        assert command.description and len(command.description) <= 100
        for parameter in command.parameters:
            assert parameter.description and parameter.description != "…", (
                f"/{command.name}: o parâmetro {parameter.name} precisa de @app_commands.describe"
            )


async def test_moderation_commands_require_permissions(loaded_bot):
    for name, permission in MODERATION_PERMISSIONS.items():
        command = loaded_bot.tree.get_command(name)
        assert command.default_permissions is not None
        assert getattr(command.default_permissions, permission) is True
        assert command.checks, f"/{name} precisa de app_commands.checks.has_permissions"


def test_build_intents(settings):
    intents = build_intents(settings)
    assert intents.members is True
    assert intents.message_content is True
    assert intents.guilds is True


def test_bot_uses_settings(settings):
    bot = ProgramaBot(settings)
    assert bot.settings is settings
    assert bot.help_command is None


async def test_help_view_is_persistent():
    view = HelpView()
    assert view.timeout is None
    assert view.is_persistent()
    assert view.children[0].custom_id == HELP_SELECT_CUSTOM_ID


@pytest.mark.parametrize(
    "module_name",
    ["examples.commands.meu_comando", "examples.events.reacao_automatica", "examples.embeds.embed_completo"],
)
async def test_example_templates_load_as_extensions(settings, module_name):
    """Os modelos da pasta examples/ precisam funcionar quando copiados para o bot."""
    bot = ProgramaBot(settings)
    async with bot:
        await bot.load_extension(module_name)
        assert module_name in bot.extensions
        await bot.unload_extension(module_name)


def test_minimal_bot_example_compiles():
    source = (Path(__file__).resolve().parent.parent / "examples" / "minimal-bot" / "bot_minimo.py").read_text(encoding="utf-8")
    compile(source, "bot_minimo.py", "exec")


def test_category_embeds():
    for key in HELP_CATEGORIES:
        embed = build_category_embed(key)
        assert isinstance(embed, discord.Embed)
        assert "/" in embed.description
