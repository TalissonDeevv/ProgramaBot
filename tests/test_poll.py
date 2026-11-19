"""Testes da enquete (bot/views/poll.py)."""

from datetime import timedelta

import pytest

from bot.views.poll import MAX_OPTIONS, PollError, PollState, PollView, parse_poll_options


def test_parse_poll_options_cleans_input():
    assert parse_poll_options(" Python ;JavaScript; ; python; Java ") == ["Python", "JavaScript", "Java"]


@pytest.mark.parametrize("raw", ["Apenas uma", "", ";;;", "A; a"])
def test_too_few_options(raw):
    with pytest.raises(PollError):
        parse_poll_options(raw)


def test_too_many_or_too_long_options():
    with pytest.raises(PollError):
        parse_poll_options(";".join(f"Opção {i}" for i in range(MAX_OPTIONS + 1)))
    with pytest.raises(PollError):
        parse_poll_options("A; " + "x" * 81)


def test_votes_add_change_and_remove():
    state = PollState("Linguagem favorita?", ["Python", "Java"])
    assert state.vote(user_id=1, option_index=0) == "added"
    assert state.vote(user_id=2, option_index=0) == "added"
    assert state.counts() == [2, 0]
    assert state.vote(user_id=1, option_index=1) == "changed"
    assert state.counts() == [1, 1]
    assert state.vote(user_id=1, option_index=1) == "removed"
    assert state.counts() == [1, 0]
    assert state.total_votes == 1


def test_invalid_option_index():
    state = PollState("?", ["A", "B"])
    with pytest.raises(IndexError):
        state.vote(1, 5)


def test_result_lines():
    state = PollState("?", ["A", "B"])
    state.vote(1, 0)
    lines = state.result_lines()
    assert "1 voto (100%)" in lines[0]
    assert "0 votos (0%)" in lines[1]


async def test_poll_view_creates_one_button_per_option():
    view = PollView(PollState("?", ["A", "B", "C"]), "Autor", timedelta(minutes=1))
    assert len(view.children) == 3
    embed = view.build_embed()
    assert embed.title == "📊 ?"
    await view.finish()  # sem mensagem: apenas desativa os botões
    assert view.finished
    assert all(button.disabled for button in view.children)
