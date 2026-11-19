# `bot/commands/general/hello.py`: o comando /hello

## 1. Nome e localização

- **Arquivo:** `bot/commands/general/hello.py`
- **Comando:** `/hello [nome]`

## 2. Finalidade

Cumprimentar o usuário com "Bom dia", "Boa tarde" ou "Boa noite", de acordo com o horário, e sortear uma dica de estudo.

## 3. Por que foi criado

Ele reúne, em poucas linhas, três fundamentos de programação:

- **condicionais** (escolher a saudação);
- **parâmetros opcionais** (o nome pode ou não ser informado);
- **aleatoriedade** (sortear uma dica).

É também o arquivo ideal para a sua **primeira modificação**.

## 4. Como se conecta ao restante do bot

É independente: não importa nada do projeto. Tem uma versão de prefixo (`!hello`) em [`prefix_examples.py`](prefix_examples.md), para comparação.

## 5. Bibliotecas utilizadas

- [`random`](../../../libraries/random.md) (nativa): `random.choice`.
- [`datetime`](../../../libraries/datetime.md) (nativa): `datetime.now().hour`.
- [`discord.py`](../../../libraries/discord-py.md).

## 6. Importações

```python
import random
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands
```

## 7. Conceitos de Python utilizados

- **Tupla** de textos (`STUDY_TIPS`).
- **`if` com comparação encadeada**: `5 <= hour < 12` é o mesmo que `5 <= hour and hour < 12`.
- **Lançar exceção** para entrada inválida (`raise ValueError`).
- **Operador `or`** como valor padrão: `nome or interaction.user.display_name`.
- **Parâmetro opcional** com `= None`.

## 8. Variáveis e constantes

- `STUDY_TIPS`: tupla com dicas.
- `name`: o nome que será usado (o informado ou o do perfil).
- `greeting`: a saudação.
- `tip`: a dica sorteada.

## 9. Funções

**`greeting_for_hour(hour) -> str`**:

| Hora | Resultado |
|---|---|
| 5 a 11 | Bom dia |
| 12 a 17 | Boa tarde |
| 18 a 4 | Boa noite |

Fica fora da classe para ser testada sem o Discord.

## 10. Parâmetros

- `hour`: número de 0 a 23.
- `nome: app_commands.Range[str, 1, 50] | None = None`:
  - `Range[str, 1, 50]` faz o **próprio Discord** exigir de 1 a 50 caracteres;
  - `| None = None` torna o parâmetro **opcional** no Discord.

## 11. Métodos utilizados

| Método | Explicação |
|---|---|
| `datetime.now().hour` | Hora atual **do computador onde o bot roda**. |
| `random.choice(sequencia)` | Escolhe um item aleatório. |
| `@app_commands.describe(nome=...)` | Texto de ajuda que aparece embaixo do parâmetro no Discord. |
| `interaction.user.display_name` | Apelido no servidor, ou nome global. |
| `discord.AllowedMentions.none()` | Se alguém digitar `@everyone` como nome, ninguém é marcado. |

## 12. Funcionamento do código

```python
def greeting_for_hour(hour: int) -> str:
    if not 0 <= hour <= 23:
        raise ValueError("A hora deve estar entre 0 e 23.")
    if 5 <= hour < 12:
        return "Bom dia"
    if 12 <= hour < 18:
        return "Boa tarde"
    return "Boa noite"
```

Como cada `if` termina com `return`, não precisamos de `elif`: se o primeiro `if` for verdadeiro, a função já terminou. O último `return` cobre todos os casos restantes (18 a 23 e 0 a 4).

```python
name = nome or interaction.user.display_name
```

Se `nome` for `None`, o `or` usa o nome do perfil.

## 13. Fluxo de execução

```
/hello nome:Ana
 ├─ name = "Ana"
 ├─ greeting_for_hour(14) → "Boa tarde"
 ├─ random.choice(STUDY_TIPS)
 └─ "Boa tarde, **Ana**! 👋\n💡 Dica: ..."
```

## 14. Exemplos práticos

```python
from bot.commands.general.hello import greeting_for_hour
for hora in (3, 9, 15, 21):
    print(hora, greeting_for_hour(hora))
```

## 15. Erros comuns

- **"Boa noite" às 10h da manhã**: o bot usa o relógio do computador onde está rodando. Se ele estiver hospedado em outro país, o fuso será outro.
- **Parâmetro sem descrição**: o teste `test_commands_have_descriptions` falha se faltar o `@app_commands.describe`.

## 16. Como testar

```bash
python -m pytest tests/test_command_helpers.py -k greeting -v
```

## 17. Como modificar

- Adicione suas próprias dicas em `STUDY_TIPS`.
- Crie uma faixa nova: "Boa madrugada" entre 0h e 4h.

## 18. Desafio

Resolva o [exercício 7](../../../exercises/02-basico.md#exercício-7--criar-o-comando-hello-do-zero): recrie este comando do zero, em um arquivo novo, sem olhar o original.
