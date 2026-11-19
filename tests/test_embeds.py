"""Testes de bot/utils/embeds.py (embeds podem ser criados sem conexão com o Discord)."""

import pytest

from bot.utils.embeds import (
    ERROR_COLOR,
    FOOTER_TEXT,
    PRIMARY_COLOR,
    SUCCESS_COLOR,
    base_embed,
    error_embed,
    info_embed,
    parse_hex_color,
    success_embed,
    warning_embed,
)


def test_base_embed_has_footer_and_timestamp():
    embed = base_embed("Título", "Descrição")
    assert embed.title == "Título"
    assert embed.description == "Descrição"
    assert embed.footer.text == FOOTER_TEXT
    assert embed.timestamp is not None
    assert embed.color.value == PRIMARY_COLOR


def test_helpers_use_expected_colors():
    assert success_embed("ok").color.value == SUCCESS_COLOR
    assert error_embed("erro").color.value == ERROR_COLOR
    assert warning_embed("cuidado").title.startswith("⚠️")
    assert info_embed("info", title="Custom").title == "Custom"


@pytest.mark.parametrize(
    ("text", "expected"),
    [("#FF0000", 0xFF0000), ("00ff00", 0x00FF00), ("  #5865f2 ", 0x5865F2), ("", PRIMARY_COLOR)],
)
def test_parse_hex_color(text, expected):
    assert parse_hex_color(text) == expected


@pytest.mark.parametrize("text", ["#FFF", "vermelho", "#GGGGGG", "1234567"])
def test_parse_hex_color_invalid(text):
    with pytest.raises(ValueError):
        parse_hex_color(text)
