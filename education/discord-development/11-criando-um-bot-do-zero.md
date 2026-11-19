# 11. Criando um bot do zero (independente do ProgramaBot)

O objetivo do ProgramaBot é que você consiga criar **seus próprios** bots. Este roteiro mostra como começar um projeto novo do zero.

## 1. Crie a pasta e o ambiente

```bash
mkdir meu-bot
cd meu-bot
python -m venv .venv
```

Ative o ambiente ([como ativar](../getting-started/05-ambiente-virtual-e-dependencias.md)) e instale:

```bash
pip install discord.py python-dotenv
pip freeze > requirements.txt
```

## 2. Crie a aplicação no Discord

Siga [Criando o bot no Discord](../getting-started/06-criando-o-bot-no-discord.md). Isso inclui criar a aplicação, copiar o token e convidar o bot.

## 3. Proteja o token

Crie `.env`:

```ini
DISCORD_TOKEN=seu_token
```

Crie `.gitignore` **antes** do primeiro commit:

```
.env
.venv/
__pycache__/
```

## 4. Versão 1: um único arquivo

Comece pelo [`examples/minimal-bot/bot_minimo.py`](../../examples/minimal-bot/bot_minimo.py). Copie-o como `bot.py` e execute:

```bash
python bot.py
```

## 5. Versão 2: organize quando crescer

Quando o arquivo passar de umas 150 linhas, divida-o:

```
meu-bot/
├── bot/
│   ├── __init__.py
│   ├── main.py          # cria o Bot e carrega as extensões
│   └── commands/
│       ├── __init__.py
│       └── ping.py      # um Cog + setup()
├── tests/
├── .env
├── .gitignore
└── requirements.txt
```

`bot/main.py` mínimo:

```python
import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

EXTENSIONS = ("bot.commands.ping",)


class MeuBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=discord.Intents.default())

    async def setup_hook(self) -> None:
        for extension in EXTENSIONS:
            await self.load_extension(extension)
        await self.tree.sync()


async def main() -> None:
    load_dotenv()
    async with MeuBot() as bot:
        await bot.start(os.environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
```

Execute com `python -m bot.main`.

## 6. Cresça aos poucos

Pegue ideias do ProgramaBot conforme precisar:

| Necessidade | Veja |
|---|---|
| Configurações validadas | [`config.py`](../code-explanation/config.md) |
| Logs em arquivo | [`utils/logger.py`](../code-explanation/utils/logger.md) |
| Carregamento automático de extensões | [`main.py`](../code-explanation/main.md) |
| Tratamento de erros | [`events/errors.py`](../code-explanation/events/errors.md) |
| Banco de dados | [`database/reminders.py`](../code-explanation/database/reminders.md) |
| Testes | [`tests/`](../../tests) e [Boas práticas: testes](../best-practices/04-testes.md) |

## 7. Ideias de projetos

- Bot de **estudos**: pomodoro, metas diárias, ranking de horas estudadas.
- Bot de **quiz**: perguntas de múltipla escolha com botões e pontuação em SQLite.
- Bot de **eventos**: agenda com lembretes para o servidor.
- Bot de **cargos por botão**: membros escolhem os próprios cargos (com view persistente).

## 8. Hospedagem

Para o bot ficar online 24 horas, ele precisa rodar em um computador sempre ligado (um servidor, um VPS ou um Raspberry Pi). Antes de escolher um serviço de hospedagem, leia os termos e verifique custos e limites, que mudam com frequência. Nunca envie o token por canais inseguros: configure-o como variável de ambiente no serviço escolhido.
