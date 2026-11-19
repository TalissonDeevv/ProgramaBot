"""Testes das funções auxiliares definidas dentro dos arquivos de comandos e eventos."""

import json
import random
from types import SimpleNamespace

import pytest
from discord import app_commands

from bot.commands.fun.dice import roll_dice
from bot.commands.fun.fact import FACTS_FILE, load_facts
from bot.commands.general.hello import STUDY_TIPS, greeting_for_hour
from bot.commands.general.ping import latency_status
from bot.commands.information.userinfo import MAX_ROLES_SHOWN, format_roles
from bot.commands.moderation.unban import parse_user_id
from bot.events.errors import describe_app_command_error, format_permissions
from bot.events.message import is_only_mention


@pytest.mark.parametrize(
    ("hour", "expected"),
    [(5, "Bom dia"), (11, "Bom dia"), (12, "Boa tarde"), (17, "Boa tarde"), (18, "Boa noite"), (0, "Boa noite"), (4, "Boa noite")],
)
def test_greeting_for_hour(hour, expected):
    assert greeting_for_hour(hour) == expected


@pytest.mark.parametrize("hour", [-1, 24])
def test_greeting_invalid_hour(hour):
    with pytest.raises(ValueError):
        greeting_for_hour(hour)


def test_study_tips_not_empty():
    assert len(STUDY_TIPS) > 0


@pytest.mark.parametrize(("latency", "word"), [(50, "Excelente"), (150, "Boa"), (400, "Alta")])
def test_latency_status(latency, word):
    assert word in latency_status(latency)


def test_roll_dice():
    random.seed(42)  # "semente" fixa: os resultados aleatórios se repetem em todo teste
    results = roll_dice(6, 100)
    assert len(results) == 100
    assert all(1 <= value <= 6 for value in results)
    with pytest.raises(ValueError):
        roll_dice(1, 1)
    with pytest.raises(ValueError):
        roll_dice(6, 0)


def test_facts_file_is_valid():
    facts = load_facts()
    assert len(facts) >= 10
    assert all(fact.strip() for fact in facts)


def test_load_facts_rejects_wrong_format(tmp_path):
    wrong = tmp_path / "facts.json"
    wrong.write_text(json.dumps({"facts": []}), encoding="utf-8")
    with pytest.raises(ValueError):
        load_facts(wrong)
    assert FACTS_FILE.name == "facts.json"


@pytest.mark.parametrize(
    ("text", "expected"),
    [("123456", 123456), (" <@123> ", 123), ("<@!123>", 123), ("abc", None), ("", None), ("12a", None)],
)
def test_parse_user_id(text, expected):
    assert parse_user_id(text) == expected


def test_is_only_mention():
    assert is_only_mention("<@42>", 42)
    assert is_only_mention(" <@!42> ", 42)
    assert not is_only_mention("<@42> oi", 42)
    assert not is_only_mention("<@43>", 42)


def test_format_roles():
    def role(name):
        return SimpleNamespace(mention=f"@{name}")

    everyone = role("everyone")
    assert format_roles(SimpleNamespace(roles=[everyone])) == "Nenhum cargo"
    member = SimpleNamespace(roles=[everyone, role("baixo"), role("alto")])
    assert format_roles(member) == "@alto, @baixo"
    many = SimpleNamespace(roles=[everyone] + [role(str(i)) for i in range(MAX_ROLES_SHOWN + 3)])
    assert format_roles(many).endswith("e mais 3")


def test_describe_app_command_error():
    assert "Expulsar membros" in describe_app_command_error(app_commands.MissingPermissions(["kick_members"]))
    assert "Eu preciso" in describe_app_command_error(app_commands.BotMissingPermissions(["ban_members"]))
    cooldown = app_commands.CommandOnCooldown(app_commands.Cooldown(1, 30.0), retry_after=12.3)
    assert "12 segundo" in describe_app_command_error(cooldown)
    assert "servidores" in describe_app_command_error(app_commands.NoPrivateMessage())
    assert describe_app_command_error(app_commands.AppCommandError("x")) is None


def test_format_permissions():
    assert format_permissions(["manage_messages", "algo_novo"]) == "Gerenciar mensagens, algo novo"
