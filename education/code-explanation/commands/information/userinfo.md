# `bot/commands/information/userinfo.py`: o comando /userinfo

## 1. Nome e localização

- **Arquivo:** `bot/commands/information/userinfo.py`
- **Comando:** `/userinfo [membro]` (só em servidores)

## 2. Finalidade

Exibir informações de um membro: nome, ID, se é bot, data de criação da conta, data de entrada no servidor e cargos.

## 3. Por que foi criado

Para estudar o objeto `discord.Member` e duas técnicas úteis:

- **datas que se adaptam ao fuso de quem lê**, com `discord.utils.format_dt`;
- **manipulação de listas** (inverter, fatiar e limitar quantidade).

## 4. Como se conecta ao restante do bot

Usa `base_embed`. A função `format_roles` é testada em `tests/test_command_helpers.py`.

## 5. Bibliotecas utilizadas

- [`discord.py`](../../../libraries/discord-py.md).

## 6. Importações

```python
import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import base_embed
```

## 7. Conceitos de Python utilizados

- **Fatiamento de listas**: `roles[1:]` (do segundo em diante) e `roles[:10]` (os dez primeiros).
- **`reversed()`** e **`list()`**.
- **Compreensão de lista**: `[role.mention for role in roles[:MAX_ROLES_SHOWN]]`.
- **`isinstance`** para garantir o tipo.
- **Expressão condicional**: `"Sim" if target.bot else "Não"`.

## 8. Variáveis e constantes

- `MAX_ROLES_SHOWN = 10`: o valor de um campo de embed tem limite de 1024 caracteres. Mostrar todos os cargos de um servidor grande ultrapassaria esse limite.
- `target`: o membro consultado.
- `roles`, `mentions`, `hidden`: usados em `format_roles`.

## 9. Funções

- **`format_roles(member) -> str`**: lista os cargos do mais alto para o mais baixo, sem `@everyone`, com no máximo 10 e o texto "e mais X" para o restante.
- `UserInfo.userinfo(interaction, membro=None)` e `setup(bot)`.

## 10. Parâmetros

- `membro: discord.Member | None = None`: o tipo `Member` só faz sentido em servidores, por isso o comando usa `@app_commands.guild_only()`.

## 11. Métodos e atributos utilizados

| Atributo | Explicação |
|---|---|
| `member.roles` | Lista de cargos, do **mais baixo** para o **mais alto**. O primeiro é sempre `@everyone`. |
| `role.mention` | Texto como `<@&123>`, que o Discord exibe como o nome do cargo. |
| `member.top_role` | Cargo mais alto. |
| `member.color` | Cor do cargo mais alto que tem cor (`.value` = número; 0 se não houver). |
| `member.created_at` | Quando a conta foi criada (`datetime` em UTC). |
| `member.joined_at` | Quando entrou no servidor (pode ser `None` em casos raros). |
| `member.bot` | `True` se for um bot. |
| `discord.utils.format_dt(dt, "D")` | Data longa, como "19 de novembro de 2026". |
| `discord.utils.format_dt(dt, "R")` | Tempo relativo, como "há 3 anos". |
| `@app_commands.guild_only()` | Esconde o comando em mensagens diretas. |

## 12. Funcionamento do código

```python
def format_roles(member: discord.Member) -> str:
    roles = list(reversed(member.roles[1:]))
    if not roles:
        return "Nenhum cargo"
    mentions = [role.mention for role in roles[:MAX_ROLES_SHOWN]]
    hidden = len(roles) - MAX_ROLES_SHOWN
    if hidden > 0:
        mentions.append(f"e mais {hidden}")
    return ", ".join(mentions)
```

1. `[1:]` remove o `@everyone`.
2. `reversed` coloca o cargo mais alto primeiro.
3. `[:10]` pega até 10 cargos.

```python
embed = base_embed(f"👤 {target.display_name}", color=target.color.value or 0x5865F2)
```

Se o membro não tiver cargo colorido, `color.value` é `0` (preto), e `or` troca pelo azul padrão.

`format_dt` gera textos como `<t:1700000000:R>`. **O próprio Discord** converte isso para o idioma e o fuso horário de quem lê. Por isso, o bot não precisa saber onde cada pessoa mora.

`allowed_mentions=discord.AllowedMentions.none()` evita que as menções de cargos no embed notifiquem alguém.

## 13. Fluxo de execução

```
/userinfo membro:@Ana
 ├─ target = Ana (Member)
 ├─ embed com thumbnail (avatar)
 ├─ campos: usuário, ID, bot?, criada, entrou, cargo mais alto, cargos
 └─ send_message(embed, sem notificar menções)
```

## 14. Exemplos práticos

Os testes usam objetos falsos:

```python
from types import SimpleNamespace
from bot.commands.information.userinfo import format_roles

def cargo(nome):
    return SimpleNamespace(mention=f"@{nome}")

membro = SimpleNamespace(roles=[cargo("everyone"), cargo("Aluno"), cargo("Monitor")])
print(format_roles(membro))  # @Monitor, @Aluno
```

## 15. Erros comuns

- **Comando não aparece em mensagens diretas**: é proposital (`guild_only`).
- **Campo com mais de 1024 caracteres** gera erro. Por isso existe o limite de cargos.

## 16. Como testar

```bash
python -m pytest tests/test_command_helpers.py -k format_roles -v
```

## 17. Como modificar

Adicione um campo com as **permissões principais** do membro: `target.guild_permissions.administrator`, `.manage_messages` etc.

## 18. Desafio

Mostre há quantos **dias** a pessoa está no servidor. Dica: `(discord.utils.utcnow() - target.joined_at).days`. Pense: por que é preciso usar um horário com fuso (`utcnow()`) em vez de `datetime.now()`?
