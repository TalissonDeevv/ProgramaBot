"""Testes das regras de hierarquia (bot/utils/moderation.py).

Em vez de membros reais do Discord, usamos objetos simples (SimpleNamespace)
com os mesmos atributos que a função usa: ``id`` e ``top_role``. Como a função
só compara cargos com ``<=``, números servem para representar a posição do cargo.
"""

from types import SimpleNamespace

import pytest

from bot.utils.moderation import DEFAULT_REASON, MAX_REASON_LENGTH, build_audit_reason, check_hierarchy

OWNER_ID = 1


def member(member_id: int, role_position: int) -> SimpleNamespace:
    return SimpleNamespace(id=member_id, top_role=role_position)


@pytest.fixture
def bot_member():
    return member(99, 50)


def test_allowed(bot_member):
    assert check_hierarchy(member(2, 30), member(3, 10), bot_member, OWNER_ID) is None


def test_cannot_target_self(bot_member):
    actor = member(2, 30)
    assert "si mesmo" in check_hierarchy(actor, actor, bot_member, OWNER_ID)


def test_cannot_target_bot(bot_member):
    assert "mim mesmo" in check_hierarchy(member(2, 30), bot_member, bot_member, OWNER_ID)


def test_cannot_target_owner(bot_member):
    assert "dono" in check_hierarchy(member(2, 30), member(OWNER_ID, 1), bot_member, OWNER_ID)


def test_actor_role_must_be_higher(bot_member):
    assert "igual ou superior" in check_hierarchy(member(2, 10), member(3, 10), bot_member, OWNER_ID)


def test_owner_can_moderate_higher_roles(bot_member):
    assert check_hierarchy(member(OWNER_ID, 1), member(3, 40), bot_member, OWNER_ID) is None


def test_bot_role_must_be_higher(bot_member):
    assert "Meu cargo" in check_hierarchy(member(OWNER_ID, 100), member(3, 60), bot_member, OWNER_ID)


def test_build_audit_reason():
    assert build_audit_reason(None, "Moderador#0001", "kick") == f"{DEFAULT_REASON} | por Moderador#0001 via /kick"
    long_reason = "a" * 1000
    assert build_audit_reason(long_reason, "Mod", "ban").startswith("a" * MAX_REASON_LENGTH + " |")
