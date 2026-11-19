# `bot/commands/fun/dice.py`: o comando /dice

## 1. Nome e localização

- **Arquivo:** `bot/commands/fun/dice.py`
- **Comando:** `/dice [lados:2-1000] [quantidade:1-10]` (padrão: 1 dado de 6 lados)

## 2. Finalidade

Rolar dados e mostrar os resultados. Quando há mais de um dado, mostra também a soma, o maior e o menor valor.

## 3. Por que foi criado

Para praticar **aleatoriedade**, **listas** e funções nativas como `sum`, `max`, `min` e `map`, em um contexto divertido. Jogadores de RPG reconhecem a notação `2d6` (2 dados de 6 lados).

## 4. Como se conecta ao restante do bot

Usa `base_embed`. A função `roll_dice` é testada sem o Discord.

## 5. Bibliotecas utilizadas

- [`random`](../../../libraries/random.md): `random.randint`.
- [`discord.py`](../../../libraries/discord-py.md).

## 6. Importações

```python
import random

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import base_embed
```

## 7. Conceitos de Python utilizados

- **Compreensão de lista**: `[random.randint(1, sides) for _ in range(amount)]`.
- **`_` como nome de variável**: indica que o valor não será usado.
- **`range(n)`**: sequência de 0 a n-1.
- **`map(str, lista)`**: aplica `str` em cada item.
- **`", ".join(...)`**: junta textos.
- **`sum`, `max`, `min`**.
- **Validação com `raise ValueError`**.

## 8. Variáveis

- `results`: lista de inteiros.

## 9. Funções

- **`roll_dice(sides, amount) -> list[int]`**: rola os dados.
- `Dice.dice(interaction, lados=6, quantidade=1)` e `setup(bot)`.

## 10. Parâmetros

- `sides` / `lados`: número de faces (mínimo 2).
- `amount` / `quantidade`: quantos dados (mínimo 1).

A validação existe em **dois lugares**: no Discord (`Range`) e na função (`raise ValueError`). A função pode ser usada fora do comando, por isso se protege sozinha.

## 11. Métodos utilizados

| Método | Explicação |
|---|---|
| `random.randint(a, b)` | Inteiro aleatório entre `a` e `b`, **incluindo os dois extremos**. |

## 12. Funcionamento do código

```python
return [random.randint(1, sides) for _ in range(amount)]
```

É equivalente a:

```python
results = []
for _ in range(amount):
    results.append(random.randint(1, sides))
return results
```

```python
embed = base_embed(f"🎲 {quantidade}d{lados}", f"Resultados: **{', '.join(map(str, results))}**")
```

`join` só aceita textos, por isso convertemos cada número com `map(str, ...)`.

## 13. Fluxo de execução

```
/dice lados:20 quantidade:3
 ├─ roll_dice(20, 3) → [7, 19, 2]
 └─ embed "🎲 3d20" → Resultados: 7, 19, 2 | Soma 28 | Maior 19 | Menor 2
```

## 14. Exemplos práticos

```python
import random
from bot.commands.fun.dice import roll_dice

random.seed(1)        # resultados reproduzíveis
print(roll_dice(6, 5))
```

## 15. Erros comuns

- **`random.randint(1, 6)` nunca dá 6?** Dá sim: `randint` inclui o limite superior. Não confunda com `range(1, 6)`, que vai só até 5.

## 16. Como testar

```bash
python -m pytest tests/test_command_helpers.py -k roll_dice -v
```

O teste usa `random.seed(42)` para os resultados "aleatórios" serem sempre os mesmos.

## 17. Como modificar

Adicione um bônus: `/dice lados:20 bonus:3` soma 3 ao total.

## 18. Desafio

Crie o comando `/coinflip` (cara ou coroa) em um arquivo novo, `bot/commands/fun/coinflip.py`, usando `random.choice(("Cara", "Coroa"))`. Siga o checklist de [Criando um novo comando](../../../discord-development/10-criando-um-novo-comando.md), incluindo a documentação e o teste.
