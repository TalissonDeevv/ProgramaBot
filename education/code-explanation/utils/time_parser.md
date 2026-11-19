# `bot/utils/time_parser.py`: interpretando durações de tempo

## 1. Nome e localização

- **Arquivo:** `bot/utils/time_parser.py`
- **Usado por:** [`/remind`](../commands/utility/remind.md) e [`/timeout`](../commands/moderation/timeout.md)

## 2. Finalidade

Converter textos curtos, como `10m`, `2h` e `1d12h`, em objetos `timedelta` (uma duração que o Python entende), e fazer o caminho inverso: escrever uma duração por extenso (`1 hora e 30 minutos`).

## 3. Por que foi criado

O Discord não tem um campo de "duração" nos slash commands. O usuário digita um texto, e alguém precisa interpretá-lo. Como dois comandos precisam disso, a lógica fica em um módulo compartilhado.

## 4. Como se conecta ao restante do bot

```
/remind tempo:"10m"   → parse_duration → timedelta(minutes=10) → banco de dados
/timeout duracao:"1h" → parse_duration → member.timeout(timedelta(hours=1))
mensagem de resposta  → format_duration → "10 minutos"
```

## 5. Bibliotecas utilizadas

- [`re`](../../libraries/re.md) (nativa): expressões regulares.
- [`datetime`](../../libraries/datetime.md) (nativa): a classe `timedelta`.

## 6. Importações

```python
import re
from datetime import timedelta
```

## 7. Conceitos de Python utilizados

- Expressões regulares (padrões de texto).
- Dicionários para mapear unidade → segundos.
- Tupla de tuplas (`UNIT_NAMES`) e **desempacotamento** no `for`.
- `divmod()`, que devolve quociente e resto de uma vez.
- Expressão condicional: `singular if amount == 1 else plural`.
- Fatiamento de listas: `parts[:-1]` (todos menos o último) e `parts[-1]` (o último).
- Herança de exceções: `TimeParseError(ValueError)`.

## 8. Variáveis e constantes

```python
FULL_PATTERN = re.compile(r"(?:\d+[dhms])+")
PART_PATTERN = re.compile(r"(\d+)([dhms])")
UNIT_SECONDS = {"d": 86_400, "h": 3_600, "m": 60, "s": 1}
```

- `FULL_PATTERN`: o texto **inteiro** precisa ser uma ou mais combinações de número + unidade.
  - `\d+` = um ou mais dígitos;
  - `[dhms]` = uma das letras d, h, m ou s;
  - `(?: ... )+` = grupo que se repete uma ou mais vezes, sem "capturar" o conteúdo.
- `PART_PATTERN`: encontra cada combinação e **captura** o número (grupo 1) e a unidade (grupo 2).
- `UNIT_SECONDS`: quantos segundos cada unidade vale.
- `UNIT_NAMES`: nomes no singular e no plural, do maior para o menor.

O `r` antes das aspas cria uma *raw string*, em que `\d` não é tratado como caractere especial do Python.

## 9. Funções

- **`parse_duration(text) -> timedelta`**: valida e converte. Lança `TimeParseError` se o texto for inválido.
- **`format_duration(duration) -> str`**: escreve a duração em português.

## 10. Parâmetros

- `text`: o que o usuário digitou (`"1h 30m"`, `"2H"`).
- `duration`: um `timedelta`.

## 11. Métodos utilizados

| Método | Explicação |
|---|---|
| `re.compile(padrão)` | Prepara o padrão uma vez para reutilizá-lo várias vezes. |
| `padrão.fullmatch(texto)` | Só combina se o texto **inteiro** seguir o padrão. Retorna `None` se não seguir. |
| `padrão.findall(texto)` | Lista com todos os grupos encontrados: `[("1", "h"), ("30", "m")]`. |
| `timedelta(seconds=n)` | Cria uma duração. |
| `timedelta.total_seconds()` | Converte a duração em segundos (`float`). |
| `divmod(a, b)` | Retorna `(a // b, a % b)`. |
| `", ".join(lista)` | Junta textos com vírgula. |

## 12. Funcionamento do código

```python
cleaned = text.strip().lower().replace(" ", "")
if not FULL_PATTERN.fullmatch(cleaned):
    raise TimeParseError("Formato de tempo inválido. ...")
```

Primeiro normalizamos: removemos espaços e passamos para minúsculas. `"1H 30M"` vira `"1h30m"`. Depois validamos o formato completo. Sem o `fullmatch`, um texto como `"abc10m"` passaria, porque `findall` acharia o `10m` e ignoraria o resto.

```python
total_seconds = 0
for amount, unit in PART_PATTERN.findall(cleaned):
    total_seconds += int(amount) * UNIT_SECONDS[unit]
```

Cada par `("1", "h")` é desempacotado em `amount="1"` e `unit="h"`. Ele vale `1 * 3600` segundos.

```python
for seconds_per_unit, singular, plural in UNIT_NAMES:
    amount, remaining = divmod(remaining, seconds_per_unit)
    if amount:
        parts.append(f"{amount} {singular if amount == 1 else plural}")
```

Para 5400 segundos: `divmod(5400, 86400)` = `(0, 5400)`, então não há dias; `divmod(5400, 3600)` = `(1, 1800)`, então "1 hora"; `divmod(1800, 60)` = `(30, 0)`, então "30 minutos". Resultado: `"1 hora e 30 minutos"`.

## 13. Fluxo de execução

```
parse_duration(" 1H 30m ")
 ├─ limpeza         → "1h30m"
 ├─ fullmatch       → ok
 ├─ findall         → [("1","h"), ("30","m")]
 ├─ soma            → 3600 + 1800 = 5400
 └─ timedelta(seconds=5400)
```

## 14. Exemplos práticos

```python
from bot.utils.time_parser import parse_duration, format_duration

d = parse_duration("1d2h")
print(d)                    # 1 day, 2:00:00
print(format_duration(d))   # 1 dia e 2 horas
```

## 15. Erros comuns

- **`10`** (sem unidade) é recusado de propósito: não dá para saber se são minutos ou segundos.
- **`1,5h`** não é aceito. Use `1h30m`.
- **`0m`** é recusado, porque a duração precisa ser maior que zero.

## 16. Como testar

```bash
python -m pytest tests/test_time_parser.py -v
```

## 17. Como modificar

Para aceitar semanas (`1w`), adicione `w` ao padrão (`[dhmsw]`) nas duas expressões, inclua `"w": 604_800` em `UNIT_SECONDS` e `(604_800, "semana", "semanas")` no início de `UNIT_NAMES`.

## 18. Desafio

Faça `parse_duration` aceitar palavras em português, como `10 minutos` ou `2 horas`. Dica: antes de validar, use um dicionário para substituir `"minutos"` por `"m"`, `"horas"` por `"h"` etc. Cuidado com a ordem das substituições (`"minuto"` está dentro de `"minutos"`).
