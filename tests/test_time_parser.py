"""Testes de bot/utils/time_parser.py."""

from datetime import timedelta

import pytest

from bot.utils.time_parser import TimeParseError, format_duration, parse_duration


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("30s", timedelta(seconds=30)),
        ("10m", timedelta(minutes=10)),
        ("2h", timedelta(hours=2)),
        ("1d", timedelta(days=1)),
        ("1h30m", timedelta(hours=1, minutes=30)),
        ("1d 12h", timedelta(days=1, hours=12)),
        ("2H", timedelta(hours=2)),
    ],
)
def test_parse_duration(text, expected):
    assert parse_duration(text) == expected


@pytest.mark.parametrize("text", ["", "abc", "10", "m10", "10x", "1h-30m", "0m", "-5m"])
def test_invalid_durations(text):
    with pytest.raises(TimeParseError):
        parse_duration(text)


@pytest.mark.parametrize(
    ("duration", "expected"),
    [
        (timedelta(seconds=1), "1 segundo"),
        (timedelta(minutes=10), "10 minutos"),
        (timedelta(hours=1, minutes=30), "1 hora e 30 minutos"),
        (timedelta(days=2, hours=1, minutes=5), "2 dias, 1 hora e 5 minutos"),
        (timedelta(0), "0 segundos"),
    ],
)
def test_format_duration(duration, expected):
    assert format_duration(duration) == expected
