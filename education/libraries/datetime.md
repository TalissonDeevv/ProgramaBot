# datetime

## O que é?

O módulo de **datas, horas e durações** do Python.

## Para que serve? Que problema resolve?

Trabalhar com tempo é mais difícil do que parece: meses com tamanhos diferentes, anos bissextos e **fusos horários**. O `datetime` cuida da matemática de datas para você.

## Como funciona?

As três classes usadas no ProgramaBot:

| Classe | Representa | Exemplo |
|---|---|---|
| `datetime` | Um momento (data + hora) | 19/11/2026 14:30 |
| `timedelta` | Uma duração | 1 hora e 30 minutos |
| `timezone` | Um fuso horário | `timezone.utc` |

Operações entre elas:

```
datetime + timedelta = datetime        (agora + 10 min = daqui a 10 min)
datetime - datetime  = timedelta       (hoje - nascimento = idade)
timedelta comparado com timedelta      (duração > 7 dias?)
```

### Datas "ingênuas" e "conscientes"

- **Ingênua** (*naive*): sem fuso. `datetime.now()` devolve o horário local do computador, sem dizer qual é o fuso.
- **Consciente** (*aware*): com fuso. `datetime.now(timezone.utc)` sabe que está em UTC.

O Discord trabalha com horários em **UTC**. Por isso, em quase todo o bot usamos datas conscientes. A exceção é o `/hello`, que quer de propósito a hora local do computador.

## Nativa ou externa?

**Nativa.**

## Como importar

```python
from datetime import datetime, timedelta, timezone
```

Atenção: o módulo e a classe têm o mesmo nome (`datetime.datetime`). Com o `from ... import`, usamos a classe diretamente.

## Funções e métodos utilizados no ProgramaBot

| Item | Onde | Explicação |
|---|---|---|
| `datetime.now()` | `hello.py` | Agora, no horário local (ingênuo). |
| `datetime.now(timezone.utc)` | `embeds.py`, `poll.py`, `remind.py`, `reminders.py` | Agora, em UTC (consciente). |
| `.hour` | `hello.py` | A hora (0 a 23). |
| `.timestamp()` | `reminders.py` | Segundos desde 01/01/1970 UTC (*Unix time*). |
| `datetime.fromtimestamp(ts, tz=timezone.utc)` | `reminders.py` | O caminho inverso. |
| `timedelta(seconds=, minutes=, days=)` | `time_parser.py`, `poll.py`, `remind.py`, `timeout.py` | Cria durações. |
| `.total_seconds()` | `time_parser.py`, `poll.py` | Duração em segundos (`float`). |

O discord.py complementa o módulo com `discord.utils.utcnow()` e `discord.utils.format_dt()`.

## Exemplo independente do ProgramaBot

```python
from datetime import datetime, timedelta, timezone

agora = datetime.now(timezone.utc)
prova = agora + timedelta(days=7, hours=2)
falta = prova - agora

print("Agora (UTC):", agora.strftime("%d/%m/%Y %H:%M"))
print("Prova em:", prova.strftime("%d/%m/%Y %H:%M"))
print("Faltam", falta.days, "dias")
print("Em segundos:", int(falta.total_seconds()))
```

`strftime` formata a data como texto: `%d` = dia, `%m` = mês, `%Y` = ano, `%H` = hora, `%M` = minuto.

## Documentação oficial

- <https://docs.python.org/pt-br/3/library/datetime.html>
