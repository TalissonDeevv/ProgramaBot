# 📦 Bibliotecas usadas no ProgramaBot

Esta pasta explica **cada biblioteca e módulo** importado pelo código do bot. Quando encontrar um `import` que você não conhece, procure aqui.

## Antes de tudo: módulo, pacote, biblioteca e framework

Essas palavras aparecem o tempo todo e costumam ser confundidas.

| Termo | O que é | Exemplo no ProgramaBot |
|---|---|---|
| **Módulo** | Um único arquivo `.py` com código reutilizável. | `bot/utils/embeds.py` é um módulo; `random` também. |
| **Pacote** | Uma pasta que agrupa módulos (normalmente com um `__init__.py`). | `bot/utils/` é um pacote; `discord` também. |
| **Biblioteca** | Um conjunto de código pronto para você **chamar** quando precisar. Pode ser um módulo ou vários pacotes. | `python-dotenv`: você chama `load_dotenv()` quando quiser. |
| **Framework** | Uma estrutura que **chama o seu código**. Você preenche as partes, e ele decide quando executá-las. | `discord.ext.commands`: você escreve `async def ping(...)`, e é o framework que decide chamá-lo quando alguém usa `/ping`. |

A diferença entre biblioteca e framework costuma ser resumida assim: **você chama a biblioteca; o framework chama você**. O discord.py é, ao mesmo tempo, uma biblioteca (classes como `discord.Embed`) e um framework (o sistema de comandos e eventos).

## Nativa ou externa?

- **Biblioteca padrão (nativa):** já vem com o Python. Basta importar.
- **Externa (de terceiros):** precisa ser instalada com `pip`. Fica listada no `requirements.txt`.

## Índice

### Externas (instaladas com `pip install -r requirements.txt`)

| Biblioteca | Para quê | Página |
|---|---|---|
| discord.py | Criar o bot e falar com o Discord | [discord-py.md](discord-py.md) |
| python-dotenv | Ler o arquivo `.env` | [python-dotenv.md](python-dotenv.md) |
| pytest (desenvolvimento) | Testes automatizados | [pytest.md](pytest.md) |

### Nativas (biblioteca padrão do Python)

| Módulo | Para quê | Página |
|---|---|---|
| asyncio | Programação assíncrona | [asyncio.md](asyncio.md) |
| os | Variáveis de ambiente | [os.md](os.md) |
| pathlib | Caminhos de arquivos | [pathlib.md](pathlib.md) |
| logging | Registros (logs) | [logging.md](logging.md) |
| datetime | Datas, horas e durações | [datetime.md](datetime.md) |
| random | Números e escolhas aleatórias | [random.md](random.md) |
| json | Ler arquivos JSON | [json.md](json.md) |
| sqlite3 | Banco de dados | [sqlite3.md](sqlite3.md) |
| ast | Calculadora segura | [ast.md](ast.md) |
| re | Expressões regulares | [re.md](re.md) |
| dataclasses | Classes de dados | [dataclasses.md](dataclasses.md) |

## Onde cada uma aparece

| Arquivo | Bibliotecas |
|---|---|
| `bot/main.py` | asyncio, logging, pathlib, discord.py |
| `bot/config.py` | os, dataclasses, pathlib, python-dotenv |
| `bot/utils/logger.py` | logging, pathlib |
| `bot/utils/embeds.py` | datetime, discord.py |
| `bot/utils/calculator.py` | ast |
| `bot/utils/time_parser.py` | re, datetime |
| `bot/database/reminders.py` | sqlite3, dataclasses, datetime, pathlib |
| `bot/views/poll.py` | dataclasses, datetime, logging, discord.py |
| `bot/commands/general/hello.py` | random, datetime, discord.py |
| `bot/commands/utility/poll.py` | asyncio, datetime, discord.py |
| `bot/commands/utility/remind.py` | logging, datetime, discord.py |
| `bot/commands/fun/dice.py` | random, discord.py |
| `bot/commands/fun/fact.py` | json, random, pathlib, discord.py |
| `tests/*.py` | pytest |

## Como ler a documentação oficial

Toda página termina com o link da documentação oficial. No começo ela pode parecer difícil. Algumas dicas:

1. Procure a seção **Quickstart** ou **Tutorial** antes da referência completa (*API Reference*).
2. Use `Ctrl+F` para achar o nome exato da função.
3. Leia a **assinatura** (os parâmetros entre parênteses) e os exemplos.
4. A documentação do Python tem versão em português: <https://docs.python.org/pt-br/3/>.
