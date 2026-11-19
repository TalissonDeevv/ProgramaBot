# `bot/events/ready.py`: o evento on_ready

## 1. Nome e localização

- **Arquivo:** `bot/events/ready.py`
- **Evento:** `on_ready`

## 2. Finalidade

Avisar no terminal (e no arquivo de log) que o bot se conectou: nome, ID, número de servidores e latência.

## 3. Por que foi criado

É a confirmação de que tudo deu certo. Também é o exemplo mais simples de **evento**: uma função que o discord.py chama sozinho quando algo acontece, sem que ninguém precise usar um comando.

## 4. Como se conecta ao restante do bot

Carregado automaticamente por [`main.py`](../main.md) (pasta `events/`). O [`remind.py`](../commands/utility/remind.md) espera por este momento com `wait_until_ready()`.

## 5. Bibliotecas utilizadas

- [`discord.py`](../../libraries/discord-py.md): `commands.Cog.listener`.
- [`logging`](../../libraries/logging.md).

## 6. Importações

```python
import logging

from discord.ext import commands
```

## 7. Conceitos de Python utilizados

- Decorators.
- Formatação de log com `%s` (texto), `%d` (inteiro) e `%.0f` (número sem casas decimais).

## 8. Variáveis

- `user`: o usuário do bot (`self.bot.user`).

## 9. Funções

- `Ready.on_ready()` e `setup(bot)`.

## 10. Parâmetros

`on_ready` não recebe parâmetros além de `self`.

## 11. Métodos utilizados

| Item | Explicação |
|---|---|
| `@commands.Cog.listener()` | Registra o método como ouvinte de um evento. O nome do método (`on_ready`) define qual evento é ouvido. |
| `self.bot.user` | O usuário do bot (`None` antes do login). |
| `self.bot.guilds` | Servidores conectados. |
| `self.bot.latency` | Latência em segundos. |

## 12. Funcionamento do código

```python
@commands.Cog.listener()
async def on_ready(self) -> None:
    user = self.bot.user
    if user is None:
        return
    logger.info("Conectado como %s (ID: %s)", user, user.id)
```

### Cuidado: o on_ready pode acontecer várias vezes

Se a conexão cair e o bot se reconectar, o Discord pode disparar `on_ready` de novo. Por isso, **não** coloque aqui ações que só podem acontecer uma vez, como carregar extensões ou sincronizar comandos. Para isso existe o `setup_hook`, no `main.py`.

## 13. Fluxo de execução

```
bot.start(token) → login → setup_hook → conexão ao gateway → cache preenchido → on_ready
```

## 14. Exemplos práticos

Listar os servidores no log:

```python
for guild in self.bot.guilds:
    logger.info("- %s (%s membros)", guild.name, guild.member_count)
```

## 15. Erros comuns

- **`on_ready` nunca é chamado**: o bot não chegou a conectar. Veja os erros acima no terminal (token, intents).
- **Usar `@bot.event` dentro de um Cog**: em Cogs, use `@commands.Cog.listener()`.

## 16. Como testar

Execute `python -m bot.main` e procure "ProgramaBot pronto!" no terminal.

## 17. Como modificar

Mude o status do bot quando ele ficar pronto:

```python
import discord
await self.bot.change_presence(activity=discord.Game(name=f"em {len(self.bot.guilds)} servidores"))
```

## 18. Desafio

Crie o evento `on_guild_join(self, guild)` em um arquivo novo (`bot/events/guild_join.py`), que registra no log quando o bot é adicionado a um servidor. Lembre-se de criar também `education/code-explanation/events/guild_join.md`.
