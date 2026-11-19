# `bot/events/errors.py`: tratamento central de erros

## 1. Nome e localização

- **Arquivo:** `bot/events/errors.py`
- **Trata:** erros de slash commands (`tree.on_error`) e de comandos de prefixo (`on_command_error`)

## 2. Finalidade

Transformar erros de comandos em mensagens amigáveis para o usuário e registrar no log os erros **inesperados** (bugs), com o *traceback* completo.

## 3. Por que foi criado

Sem um tratador, quando um comando falha:

- o usuário vê "O aplicativo não respondeu" e não entende nada;
- o erro aparece no terminal sem contexto.

Centralizar o tratamento evita repetir `try/except` de permissão e cooldown em cada comando.

## 4. Como se conecta ao restante do bot

- Todos os comandos com `checks.has_permissions`, `bot_has_permissions`, `cooldown` ou `guild_only` dependem deste arquivo para explicar o erro.
- O `!soma` ([`prefix_examples.py`](../commands/general/prefix_examples.md)) tem tratador próprio; este arquivo respeita isso.

## 5. Bibliotecas utilizadas

- [`discord.py`](../../libraries/discord-py.md): exceções de `app_commands` e de `commands`.
- [`logging`](../../libraries/logging.md).

## 6. Importações

```python
import logging

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import error_embed
```

## 7. Conceitos de Python utilizados

- **Hierarquia de exceções** e a importância da **ordem** dos `isinstance`.
- **Dicionário de tradução** com `dict.get(chave, padrão)`.
- **Substituir um método de outro objeto** (`self.bot.tree.on_error = ...`) e restaurar o original depois.
- **`exc_info=error`** no log para registrar o traceback.

## 8. Variáveis e constantes

- `PERMISSION_NAMES`: tradução dos nomes técnicos das permissões.
- `UNEXPECTED_ERROR_MESSAGE`: mensagem genérica para bugs.
- `self._previous_tree_error`: o tratador original, guardado para ser restaurado no `cog_unload`.

## 9. Funções

| Função | O que faz |
|---|---|
| `format_permissions(permissions)` | `["kick_members"]` → `"Expulsar membros"` |
| `describe_app_command_error(error)` | Mensagem amigável ou `None` para erros inesperados |
| `ErrorHandler.cog_load()` / `cog_unload()` | Instala / remove o tratador |
| `ErrorHandler.on_app_command_error(interaction, error)` | Trata erros de slash commands |
| `ErrorHandler.on_command_error(ctx, error)` | Trata erros de comandos de prefixo |

## 10. Parâmetros

- `error`: a exceção. Em slash commands, é uma subclasse de `app_commands.AppCommandError`. Erros do seu código chegam embrulhados em `CommandInvokeError`.
- `interaction` / `ctx`: onde responder.

## 11. Exceções tratadas

| Exceção | Quando acontece | Mensagem |
|---|---|---|
| `MissingPermissions` | O usuário não tem a permissão | "Você precisa da permissão: ..." |
| `BotMissingPermissions` | O bot não tem a permissão | "Eu preciso da permissão: ..." |
| `CommandOnCooldown` | Usou rápido demais | "Calma! ... em X segundo(s)" |
| `NoPrivateMessage` | `guild_only` usado em DM | "Só funciona dentro de servidores" |
| `CheckFailure` | Qualquer outra verificação falhou | "Você não pode usar este comando aqui" |
| (outras) | Bug no código | log + mensagem genérica |

## 12. Funcionamento do código

### A ordem importa

```python
if isinstance(error, app_commands.MissingPermissions): ...
if isinstance(error, app_commands.BotMissingPermissions): ...
if isinstance(error, app_commands.CommandOnCooldown): ...
if isinstance(error, app_commands.NoPrivateMessage): ...
if isinstance(error, app_commands.CheckFailure): ...
```

Todas as quatro primeiras são **subclasses** de `CheckFailure`. Se `CheckFailure` viesse primeiro, `isinstance` seria verdadeiro para todas, e as mensagens específicas nunca apareceriam.

### Instalando o tratador

```python
async def cog_load(self) -> None:
    self.bot.tree.on_error = self.on_app_command_error
```

A `CommandTree` (`bot.tree`) chama `on_error` sempre que um slash command falha. Trocamos o método padrão (que só imprime o erro) pelo nosso.

### Responder sem causar outro erro

```python
if interaction.response.is_done():
    await interaction.followup.send(embed=embed, ephemeral=True)
else:
    await interaction.response.send_message(embed=embed, ephemeral=True)
```

Se o comando já tinha respondido (ou usado `defer`), usar `response` de novo lançaria `InteractionResponded`.

### Comandos de prefixo

```python
if ctx.command is not None and ctx.command.has_error_handler():
    return
if isinstance(error, commands.CommandNotFound):
    return
```

Ignoramos `CommandNotFound` para o bot não reclamar de toda mensagem que começa com `!`.

## 13. Fluxo de execução

```
/kick (sem permissão)
 → checks.has_permissions falha → MissingPermissions
 → tree.on_error → on_app_command_error
     → describe → "Você precisa da permissão: **Expulsar membros**."
     → send_message(ephemeral)

/calculator com um bug (ex.: ZeroDivisionError não tratado)
 → CommandInvokeError → describe → None
 → logger.error(..., exc_info=error)  ← traceback no log
 → "Ocorreu um erro inesperado..."
```

## 14. Exemplos práticos

Tratar um erro personalizado:

```python
class NotStudentError(app_commands.CheckFailure):
    pass

# em describe_app_command_error, ANTES do CheckFailure:
if isinstance(error, NotStudentError):
    return "Este comando é exclusivo para estudantes."
```

## 15. Erros comuns

- **Mensagens genéricas para tudo**: provavelmente `CheckFailure` foi colocado antes das subclasses.
- **Esquecer o `exc_info`**: o log fica sem traceback e o bug fica difícil de encontrar.

## 16. Como testar

```bash
python -m pytest tests/test_command_helpers.py -k "describe or format_permissions" -v
```

As exceções do discord.py podem ser criadas diretamente nos testes, sem Discord.

## 17. Como modificar

Ao criar um comando com uma permissão nova, adicione a tradução em `PERMISSION_NAMES` (ex.: `"manage_roles": "Gerenciar cargos"`).

## 18. Desafio

Crie um *check* personalizado `is_owner()` que só deixa o dono do bot usar um comando (dica: `app_commands.check(predicate)`), lance um erro próprio e traduza-o aqui.
