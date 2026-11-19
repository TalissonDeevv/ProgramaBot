# `bot/commands/moderation/unban.py`: o comando /unban

## 1. Nome e localização

- **Arquivo:** `bot/commands/moderation/unban.py`
- **Comando:** `/unban usuario_id:<ID> [motivo]` (requer "Banir membros")

## 2. Finalidade

Remover o banimento de um usuário a partir do **ID** dele.

## 3. Por que foi criado

Quem está banido não aparece na lista de membros, então não dá para usar um parâmetro do tipo `discord.Member`. O comando ensina a:

- receber e **validar** um ID digitado como texto;
- usar `discord.Object` para representar "algo com este ID";
- tratar **exceções específicas** (`NotFound`) antes das genéricas (`HTTPException`).

## 4. Como se conecta ao restante do bot

Usa `build_audit_reason` e os embeds. A função `parse_user_id` é testada em `tests/test_command_helpers.py`.

## 5. Bibliotecas utilizadas

- [`discord.py`](../../../libraries/discord-py.md).

## 6. Importações

```python
import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import error_embed, success_embed
from bot.utils.moderation import MAX_REASON_LENGTH, build_audit_reason
```

## 7. Conceitos de Python utilizados

- **Encadeamento de métodos de string**: `.strip().removeprefix("<@").removeprefix("!").removesuffix(">")`.
- **`str.isdigit()`** para validar.
- **Vários `except`**, do mais específico para o mais genérico.

## 8. Variáveis

- `user_id`: o ID convertido em `int`, ou `None`.

## 9. Funções

- **`parse_user_id(text) -> int | None`**: aceita `123`, `<@123>` ou `<@!123>`.
- `Unban.unban(interaction, usuario_id, motivo=None)` e `setup(bot)`.

## 10. Parâmetros

- `usuario_id: str`: texto, porque IDs do Discord são números grandes (18 a 20 dígitos). Além disso, o campo `integer` dos slash commands tem um limite menor que o tamanho dos IDs.
- `motivo`: opcional.

## 11. Métodos utilizados

| Método | Explicação |
|---|---|
| `discord.Object(id=...)` | Objeto mínimo, que só tem um ID. Muitos métodos aceitam qualquer coisa com `.id` (o tipo *Snowflake*). |
| `guild.unban(user, reason=)` | Remove o banimento. Lança `NotFound` se a pessoa não estiver banida. |

## 12. Funcionamento do código

```python
def parse_user_id(text: str) -> int | None:
    cleaned = text.strip().removeprefix("<@").removeprefix("!").removesuffix(">")
    if not cleaned.isdigit():
        return None
    return int(cleaned)
```

```python
try:
    await guild.unban(discord.Object(id=user_id), reason=...)
except discord.NotFound:
    ...  # não está banido
except discord.HTTPException:
    ...  # outro problema
```

`NotFound` é uma subclasse de `HTTPException`. Se a ordem fosse invertida, o primeiro `except` capturaria tudo e o segundo nunca seria usado.

## 13. Fluxo de execução

```
/unban usuario_id:"123456789012345678"
 ├─ parse_user_id → 123456789012345678
 ├─ guild.unban(Object(id))
 │    ├─ ok       → "✅ O banimento de <@id> foi removido."
 │    ├─ NotFound → "Esse usuário não está banido"
 │    └─ outro    → "O Discord não permitiu a ação"
```

## 14. Exemplos práticos

Como copiar um ID: *Configurações de usuário > Avançado > Modo desenvolvedor* (ativar). Depois, clique com o botão direito no usuário > **Copiar ID do usuário**.

## 15. Erros comuns

- **"ID inválido"**: o texto tem letras ou espaços no meio.
- **Usar `int` como tipo do parâmetro**: IDs do Discord podem ultrapassar o limite numérico do campo `integer` dos slash commands, por isso usamos texto.

## 16. Como testar

```bash
python -m pytest tests/test_command_helpers.py -k parse_user_id -v
```

## 17. Como modificar

Adicione **autocompletar** com a lista de banidos: `@unban.autocomplete("usuario_id")` com uma função que percorre `guild.bans()` e devolve `app_commands.Choice(name=nome, value=str(id))`.

## 18. Desafio

Implemente o autocompletar acima, limitado a 25 opções (o máximo do Discord) e filtrado pelo texto que o usuário já digitou (`current`). Leia sobre [autocomplete](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.app_commands.Command.autocomplete) na documentação oficial.
