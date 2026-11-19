"""Converte textos como ``10m`` ou ``1h30m`` em durações de tempo.

Usado pelos comandos ``/remind`` (lembretes) e ``/timeout`` (castigo temporário).
"""

import re
from datetime import timedelta

# Uma ou mais combinações de "número + unidade", sem nada antes ou depois.
FULL_PATTERN = re.compile(r"(?:\d+[dhms])+")
# Cada combinação individual: o número fica no grupo 1 e a unidade no grupo 2.
PART_PATTERN = re.compile(r"(\d+)([dhms])")

UNIT_SECONDS = {"d": 86_400, "h": 3_600, "m": 60, "s": 1}

UNIT_NAMES = (
    (86_400, "dia", "dias"),
    (3_600, "hora", "horas"),
    (60, "minuto", "minutos"),
    (1, "segundo", "segundos"),
)


class TimeParseError(ValueError):
    """Erro lançado quando o texto não representa uma duração válida."""


def parse_duration(text: str) -> timedelta:
    """Converte ``"1h30m"`` em ``timedelta(hours=1, minutes=30)``.

    Unidades aceitas: ``d`` (dias), ``h`` (horas), ``m`` (minutos), ``s`` (segundos).

    Raises:
        TimeParseError: se o formato estiver errado ou a duração for zero.
    """
    cleaned = text.strip().lower().replace(" ", "")
    if not FULL_PATTERN.fullmatch(cleaned):
        raise TimeParseError(
            "Formato de tempo inválido. Use números seguidos de d, h, m ou s. "
            "Exemplos: 30s, 10m, 2h, 1d12h."
        )

    total_seconds = 0
    for amount, unit in PART_PATTERN.findall(cleaned):
        total_seconds += int(amount) * UNIT_SECONDS[unit]

    if total_seconds <= 0:
        raise TimeParseError("A duração precisa ser maior que zero.")
    return timedelta(seconds=total_seconds)


def format_duration(duration: timedelta) -> str:
    """Escreve uma duração por extenso: ``1 hora e 30 minutos``."""
    remaining = int(duration.total_seconds())
    parts: list[str] = []
    for seconds_per_unit, singular, plural in UNIT_NAMES:
        amount, remaining = divmod(remaining, seconds_per_unit)
        if amount:
            parts.append(f"{amount} {singular if amount == 1 else plural}")

    if not parts:
        return "0 segundos"
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + " e " + parts[-1]
