# `bot/commands/moderation/timeout.py`: o comando /timeout

## 1. Nome e localização

- **Arquivo:** `bot/commands/moderation/timeout.py`
- **Comando:** `/timeout membro:<@membro> duracao:<10m|remover> [motivo]` (requer "Castigar membros")

## 2. Finalidade

Aplicar (ou remover) o **castigo** nativo do Discord (*timeout*): durante o tempo definido, o membro não pode enviar mensagens, reagir nem falar em canais de voz.

## 3. Por que foi criado

Para mostrar como reutilizar o [`time_parser`](../../utils/time_parser.md) e como um mesmo parâmetro pode ter **dois significados** (uma duração ou a palavra "remover").

## 4. Como se conecta ao restante do bot

```
parse_duration, format_duration → utils/time_parser.py
check_hierarchy, build_audit_reason → utils/moderation.py
```

## 5. Bibliotecas utilizadas

- [`discord.py`](../../../libraries/discord-py.md).
- [`datetime`](../../../libraries/datetime.md): `timedelta`.

## 6. Importações

```python
from datetime import timedelta

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import error_embed, success_embed
from bot.utils.moderation import MAX_REASON_LENGTH, build_audit_reason, check_hierarchy
from bot.utils.time_parser import TimeParseError, format_duration, parse_duration
```

## 7. Conceitos de Python utilizados

- Uma variável que pode ser `timedelta` **ou** `None` (`delta`).
- `in` com tupla para comparar com várias palavras.
- `if/else` para escolher a mensagem final.

## 8. Variáveis e constantes

- `MAX_TIMEOUT = timedelta(days=28)`: limite imposto pelo Discord.
- `REMOVE_WORDS = ("0", "remover", "nenhum")`.
- `delta`: a duração, ou `None` para remover.

## 9. Funções

- `Timeout.timeout(interaction, membro, duracao, motivo=None)` e `setup(bot)`.

## 10. Parâmetros

- `membro: discord.Member`.
- `duracao: str`: `10m`, `1h`, `2d`... ou `remover`.
- `motivo`: opcional.

## 11. Métodos utilizados

| Método | Explicação |
|---|---|
| `member.timeout(until, *, reason=)` | `until` pode ser um `timedelta` (duração a partir de agora), um `datetime` (até quando) ou `None` (remove). |

## 12. Funcionamento do código

```python
if duracao.strip().lower() in REMOVE_WORDS:
    delta = None
else:
    try:
        delta = parse_duration(duracao)
    except TimeParseError as error:
        ...
    if delta > MAX_TIMEOUT:
        ...
```

```python
await membro.timeout(delta, reason=audit_reason)
```

Uma única chamada cobre os dois casos: aplicar (`timedelta`) e remover (`None`).

Diferente do `/kick` e do `/ban`, este comando **não pede confirmação**: o castigo é temporário e fácil de desfazer.

## 13. Fluxo de execução

```
/timeout membro:@João duracao:15m
 ├─ check_hierarchy ✔
 ├─ parse_duration("15m") → 15 min ≤ 28 dias ✔
 ├─ membro.timeout(15 min)
 └─ "🔇 João foi silenciado(a) por 15 minutos."

/timeout membro:@João duracao:remover
 └─ membro.timeout(None) → "🔊 O castigo de João foi removido."
```

## 14. Exemplos práticos

Castigo até um horário específico:

```python
from datetime import datetime, timezone
await membro.timeout(datetime(2026, 12, 1, tzinfo=timezone.utc), reason="...")
```

## 15. Erros comuns

- **"O Discord não permitiu a ação"** com administradores: o Discord **não permite** aplicar castigo em membros com a permissão de Administrador.
- **Mais de 28 dias**: é recusado pelo bot antes de chegar ao Discord.

## 16. Como testar

Aplique `30s` em uma conta secundária e tente enviar uma mensagem com ela. Depois, teste `remover`.

## 17. Como modificar

Envie uma DM ao membro informando a duração e o motivo do castigo.

## 18. Desafio

Mostre na resposta **até quando** o castigo vale, com `discord.utils.format_dt(discord.utils.utcnow() + delta, "f")`.
