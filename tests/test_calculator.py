"""Testes da calculadora segura (bot/utils/calculator.py)."""

import pytest

from bot.utils.calculator import CalculatorError, calculate, format_result


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("2 + 3", 5),
        ("2 + 3 * 4", 14),
        ("(2 + 3) * 4", 20),
        ("10 / 4", 2.5),
        ("10 // 4", 2),
        ("10 % 4", 2),
        ("2 ** 10", 1024),
        ("2 ^ 3", 8),
        ("-5 + 2", -3),
        ("+7", 7),
        ("3 × 3", 9),
        ("9 ÷ 3", 3),
        ("1,5 + 1", 2.5),
    ],
)
def test_valid_expressions(expression, expected):
    assert calculate(expression) == expected


@pytest.mark.parametrize(
    "expression",
    [
        "__import__('os').system('dir')",
        "open('arquivo.txt')",
        "print(1)",
        "x + 1",
        "'texto' * 3",
        "[1, 2, 3]",
        "True + 1",
        "lambda: 1",
        "2 if 1 else 3",
        "1 < 2",
    ],
)
def test_dangerous_or_unsupported_expressions_are_rejected(expression):
    with pytest.raises(CalculatorError):
        calculate(expression)


@pytest.mark.parametrize("expression", ["1 / 0", "5 // 0", "5 % 0"])
def test_division_by_zero(expression):
    with pytest.raises(CalculatorError, match="zero"):
        calculate(expression)


def test_empty_and_invalid_syntax():
    with pytest.raises(CalculatorError):
        calculate("   ")
    with pytest.raises(CalculatorError):
        calculate("2 +")


def test_limits():
    with pytest.raises(CalculatorError):
        calculate("1+" * 60 + "1")  # longa demais
    with pytest.raises(CalculatorError):
        calculate("2 ** 1000")  # expoente alto demais
    with pytest.raises(CalculatorError):
        calculate("10 ** 100 * 10")  # resultado grande demais
    with pytest.raises(CalculatorError):
        calculate("0 ** -1")
    with pytest.raises(CalculatorError):
        calculate("(-8) ** 0.5")  # resultado complexo


@pytest.mark.parametrize(
    ("value", "expected"),
    [(4.0, "4"), (0.1 + 0.2, "0.3"), (2.5, "2.5"), (7, "7"), (-3.0, "-3")],
)
def test_format_result(value, expected):
    assert format_result(value) == expected
