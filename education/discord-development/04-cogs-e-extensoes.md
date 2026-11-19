# 04. Cogs e extensões: organizando o código

## O problema

Um bot com 20 comandos em um único arquivo vira um arquivo de milhares de linhas, difícil de ler e de manter. A solução do discord.py tem duas partes.

## Cog

Um **Cog** é uma classe que agrupa comandos, eventos e estado relacionados:

```python
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="...")
    async def ping(self, interaction): ...

    @commands.Cog.listener()
    async def on_ready(self): ...
```

Métodos especiais úteis:

| Método | Quando é chamado |
|---|---|
| `async def cog_load(self)` | quando o Cog é adicionado (ideal para preparar banco de dados e iniciar tarefas) |
| `async def cog_unload(self)` | quando o Cog é removido (ideal para parar tarefas) |

## Extensão

Uma **extensão** é um módulo Python com uma função `setup`:

```python
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ping(bot))
```

O bot carrega a extensão pelo nome do módulo:

```python
await bot.load_extension("bot.commands.general.ping")
```

Também existem `bot.unload_extension(...)` e `bot.reload_extension(...)`.

## Como o ProgramaBot organiza

**Um comando por arquivo, um Cog por arquivo, uma extensão por arquivo:**

```
bot/commands/general/ping.py   →  extensão "bot.commands.general.ping"  →  Cog Ping  →  /ping
bot/events/ready.py            →  extensão "bot.events.ready"           →  Cog Ready →  on_ready
```

E o [`main.py`](../code-explanation/main.md) descobre todas as extensões automaticamente:

```python
def discover_extensions(base_dir: Path = BOT_PACKAGE_DIR) -> list[str]:
    ...  # percorre bot/commands/** e bot/events/*
```

Vantagens:

- Para criar um comando, basta **criar um arquivo**. Nenhum outro arquivo precisa ser editado para carregá-lo.
- Cada arquivo tem uma página de explicação correspondente em `code-explanation/`.
- Um erro em um arquivo não derruba os outros (o `setup_hook` registra o erro e continua).

## Por que não existe uma pasta `cogs/`?

Muitos projetos usam uma pasta `cogs/`. No ProgramaBot, **todo arquivo de `commands/` e `events/` já é um Cog**, organizado por categoria. Uma pasta `cogs/` separada seria redundante.

## Exercício

1. Abra três arquivos de `bot/commands/` e identifique em cada um: a classe Cog, o `__init__`, o comando e a função `setup`.
2. Crie um Cog com **dois** comandos relacionados (`/par` e `/impar`, que dizem se um número é par ou ímpar) em um único arquivo.

Documentação: <https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html> e <https://discordpy.readthedocs.io/en/stable/ext/commands/extensions.html>
