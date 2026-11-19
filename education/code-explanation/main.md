# `bot/main.py`: o ponto de entrada do bot

## 1. Nome e localização

- **Arquivo:** `bot/main.py`
- **Como executar:** `python -m bot.main` (na pasta raiz do projeto, com o ambiente virtual ativado)

## 2. Finalidade

É o arquivo que **liga o bot**. Ele:

1. lê as configurações do `.env`;
2. prepara os logs;
3. cria o objeto do bot com as *intents* certas;
4. encontra e carrega todos os comandos e eventos;
5. registra os slash commands no Discord;
6. conecta ao Discord e fica rodando até você apertar `Ctrl+C`.

## 3. Por que foi criado

Todo programa precisa de um começo. Em vez de espalhar a inicialização por vários arquivos, concentramos tudo aqui. Os comandos ficam em arquivos separados, e o `main.py` só os "monta" no lugar. Assim, adicionar um comando novo **não exige editar o `main.py`**.

## 4. Como se conecta ao restante do bot

```
bot/main.py
 ├── bot/config.py          → load_settings(), Settings, ConfigError
 ├── bot/utils/logger.py    → setup_logging()
 ├── bot/views/help_menu.py → HelpView (view persistente)
 ├── bot/commands/**.py     → carregados automaticamente (discover_extensions)
 └── bot/events/*.py        → carregados automaticamente
```

Os Cogs acessam as configurações por meio de `self.bot.settings`, um atributo criado aqui. É o caso do [`remind.py`](commands/utility/remind.md) e do [`member_join.py`](events/member_join.md).

## 5. Bibliotecas utilizadas

| Biblioteca | Tipo | Para quê |
|---|---|---|
| [`asyncio`](../libraries/asyncio.md) | nativa | rodar o código assíncrono com `asyncio.run` |
| [`logging`](../libraries/logging.md) | nativa | registrar mensagens no terminal e em arquivo |
| [`pathlib`](../libraries/pathlib.md) | nativa | encontrar os arquivos de comandos |
| [`discord.py`](../libraries/discord-py.md) | externa | criar o bot e falar com o Discord |

## 6. Importações

```python
import asyncio
import logging
from pathlib import Path

import discord
from discord.ext import commands

from bot import __version__
from bot.config import PROJECT_ROOT, ConfigError, Settings, load_settings
from bot.utils.logger import setup_logging
from bot.views.help_menu import HelpView
```

Os imports seguem a convenção da [PEP 8](https://peps.python.org/pep-0008/#imports), em três blocos separados por linha em branco:

1. **Biblioteca padrão** (vem com o Python): `asyncio`, `logging`, `pathlib`.
2. **Bibliotecas de terceiros** (instaladas com `pip`): `discord`.
3. **Código do próprio projeto**: tudo que começa com `bot.`.

`from discord.ext import commands` importa a *extensão de comandos* do discord.py, que oferece `commands.Bot`, `commands.Cog` e os comandos de prefixo.

## 7. Conceitos de Python utilizados

- **Classes e herança**: `class ProgramaBot(commands.Bot)` cria uma classe nova que herda tudo de `commands.Bot`. Veja [Classes e objetos](../python/09-classes-e-objetos.md).
- **`super()`**: chama o `__init__` da classe-mãe.
- **`async def` / `await`**: funções assíncronas. Veja [Programação assíncrona](../python/13-programacao-assincrona.md).
- **Tratamento de exceções**: `try` / `except`. Veja [Exceções](../python/08-excecoes.md).
- **Gerenciador de contexto assíncrono**: `async with bot:`. Veja [Context managers](../python/12-context-managers.md).
- **Type hints**: `-> list[str]`, `settings: Settings`. Servem como documentação e ajudam o editor; o Python não as obriga.
- **`if __name__ == "__main__":`**: só executa `main()` quando o arquivo é rodado diretamente, e não quando é importado (por exemplo, pelos testes).

## 8. Variáveis e constantes

```python
logger = logging.getLogger(__name__)
BOT_PACKAGE_DIR = Path(__file__).resolve().parent
EXTENSION_FOLDERS = ("commands", "events")
```

- `logger`: o "registrador" deste arquivo. `__name__` vale `"bot.main"`, e esse nome aparece em cada linha do log.
- `BOT_PACKAGE_DIR`: caminho absoluto da pasta `bot/`. `__file__` é o caminho do próprio `main.py`; `.resolve()` o transforma em caminho absoluto; `.parent` sobe uma pasta.
- `EXTENSION_FOLDERS`: uma **tupla** (lista que não pode ser alterada) com as pastas que contêm extensões.

## 9. Funções

| Função | O que faz |
|---|---|
| `discover_extensions(base_dir)` | Encontra os arquivos de comandos/eventos e devolve os nomes de módulo. |
| `build_intents(settings)` | Monta o objeto `discord.Intents` de acordo com o `.env`. |
| `run_bot()` | Função assíncrona que cria o bot e o mantém conectado. |
| `main()` | Executa `run_bot()` e converte erros técnicos em mensagens amigáveis. |

E os métodos da classe `ProgramaBot`:

| Método | O que faz |
|---|---|
| `__init__(settings)` | Configura prefixo, intents, atividade e guarda `settings`. |
| `setup_hook()` | Roda **uma vez** antes de conectar: carrega extensões e registra views. |
| `sync_application_commands()` | Envia a lista de slash commands ao Discord. |

## 10. Parâmetros

- `discover_extensions(base_dir: Path = BOT_PACKAGE_DIR)`: o parâmetro tem **valor padrão**. No bot, chamamos sem argumentos; nos testes, poderíamos passar outra pasta.
- `build_intents(settings: Settings)`: recebe as configurações para saber quais intents ativar.
- `ProgramaBot(settings: Settings)`: o bot inteiro depende das configurações.

## 11. Métodos de bibliotecas utilizados

| Método | Explicação |
|---|---|
| `Path.rglob("*.py")` | Procura arquivos `.py` em todas as subpastas (o "r" é de *recursivo*). |
| `Path.relative_to(outro)` | Corta o começo do caminho: `C:/.../ProgramaBot/bot/commands/ping.py` → `bot/commands/ping.py`. |
| `Path.with_suffix("")` | Remove a extensão `.py`. |
| `Path.parts` | Separa o caminho em partes: `("bot", "commands", "general", "ping")`. |
| `discord.Intents.default()` | Intents padrão (sem as privilegiadas). |
| `commands.when_mentioned_or("!")` | Aceita como prefixo o `!` **ou** uma menção ao bot. |
| `discord.Game(name=...)` | Status "Jogando ..." do bot. |
| `bot.load_extension(nome)` | Importa o módulo e chama a função `setup(bot)` dele. |
| `bot.add_view(HelpView())` | Registra uma view persistente. |
| `bot.tree.copy_global_to(guild=...)` | Copia os comandos globais para um servidor específico. |
| `bot.tree.sync(guild=...)` | Envia os comandos ao Discord. Retorna a lista sincronizada. |
| `bot.start(token)` | Faz login e conecta. Só termina quando o bot desliga. |
| `asyncio.run(coro)` | Cria o *event loop*, executa a corrotina e fecha o loop no final. |

## 12. Funcionamento do código

### Descobrindo extensões automaticamente

```python
for folder in EXTENSION_FOLDERS:
    for file in sorted((base_dir / folder).rglob("*.py")):
        if file.name.startswith("_"):
            continue
        relative_path = file.relative_to(base_dir.parent).with_suffix("")
        extensions.append(".".join(relative_path.parts))
```

Dois `for` aninhados: para cada pasta (`commands`, `events`), percorremos todos os `.py`. O operador `/` junta caminhos (`base_dir / "commands"`). `sorted` garante uma ordem previsível. `continue` pula para o próximo arquivo sem executar o resto do bloco. No final, `".".join(...)` cola as partes com ponto: `bot.commands.general.ping`.

### As intents

```python
intents = discord.Intents.default()
intents.members = settings.enable_members_intent
intents.message_content = settings.enable_message_content_intent
```

*Intents* dizem ao Discord quais eventos o bot quer receber. `members` e `message_content` são **privilegiadas**: precisam ser ligadas também no Developer Portal. Mais detalhes em [Intents](../discord-development/02-intents.md).

### A classe do bot

```python
class ProgramaBot(commands.Bot):
    def __init__(self, settings: Settings) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or(settings.prefix),
            intents=build_intents(settings),
            help_command=None,
            activity=discord.Game(name="/help | aprendendo Python"),
        )
        self.settings = settings
```

`help_command=None` desativa o `!help` automático do discord.py, porque temos o nosso `/help`. `self.settings = settings` cria um **atributo**: qualquer Cog com acesso ao bot pode ler `bot.settings`.

### setup_hook

```python
async def setup_hook(self) -> None:
    for extension in discover_extensions():
        try:
            await self.load_extension(extension)
        except commands.ExtensionError:
            logger.exception("Falha ao carregar a extensão %s", extension)
    self.add_view(HelpView())
    if self.settings.sync_commands:
        await self.sync_application_commands()
```

O discord.py chama `setup_hook` automaticamente depois do login e antes de conectar ao *gateway*. É o lugar certo para preparar tudo **uma vez**. O `try/except` faz com que um arquivo com erro gere um log, mas não derrube o bot. `logger.exception` também registra o *traceback* (o caminho do erro).

### Sincronização dos comandos

Slash commands precisam ser registrados no Discord. Com `GUILD_ID`, registramos só no seu servidor de testes, o que é **instantâneo**. Sem ele, o registro é global e pode demorar alguns minutos para aparecer.

### run_bot e main

```python
async def run_bot() -> None:
    settings = load_settings()
    setup_logging(settings.log_level, PROJECT_ROOT / "logs")
    bot = ProgramaBot(settings)
    async with bot:
        await bot.start(settings.token)
```

`async with bot:` garante que o bot seja fechado corretamente quando o programa terminar, mesmo que dê erro.

```python
def main() -> None:
    try:
        asyncio.run(run_bot())
    except ConfigError as error:
        print(f"[Erro de configuração] {error}")
        raise SystemExit(1) from None
    except discord.LoginFailure: ...
    except discord.PrivilegedIntentsRequired: ...
    except KeyboardInterrupt: ...
```

Cada `except` trata um problema comum e explica a solução. `raise SystemExit(1)` encerra o programa com **código de saída 1**, a convenção para "terminou com erro". `from None` esconde o traceback original, que só confundiria quem está começando. Para `ConfigError` usamos `print`, porque os logs ainda não foram configurados nesse momento.

## 13. Fluxo de execução

```
python -m bot.main
 └─ main()
     └─ asyncio.run(run_bot())
         ├─ load_settings()             → lê .env (pode lançar ConfigError)
         ├─ setup_logging()             → terminal + logs/programabot.log
         ├─ ProgramaBot(settings)       → __init__
         └─ bot.start(token)
             ├─ login                   → pode lançar LoginFailure
             ├─ setup_hook()
             │   ├─ load_extension(...) x26
             │   ├─ add_view(HelpView())
             │   └─ tree.sync()
             ├─ conecta ao gateway       → pode lançar PrivilegedIntentsRequired
             └─ evento on_ready          → events/ready.py
```

## 14. Exemplos práticos

Listar as extensões encontradas:

```bash
python -c "from bot.main import discover_extensions; print(*discover_extensions(), sep='\n')"
```

Executar o bot com logs detalhados (temporariamente, no PowerShell):

```powershell
$env:LOG_LEVEL="DEBUG"; python -m bot.main
```

## 15. Erros comuns

| Mensagem | Causa | Solução |
|---|---|---|
| `[Erro de configuração] O token do bot não foi configurado` | `.env` ausente ou com o texto de exemplo | [Configurando o .env](../getting-started/07-configurando-o-env.md) |
| `O Discord recusou o token` | Token errado ou regenerado | Gere outro em *Bot > Reset Token* |
| `As intents privilegiadas não estão ativadas` | Intents desligadas no Portal | Ative-as ou use `false` no `.env` |
| `Falha ao carregar a extensão ...` | Erro de código em um arquivo de comando | Leia o traceback logo abaixo no log |
| `ModuleNotFoundError: No module named 'bot'` | Usou `python bot/main.py` | Use `python -m bot.main` |

## 16. Como testar

```bash
python -m pytest tests/test_extensions.py -v
```

Esses testes criam um `ProgramaBot` **sem conectar ao Discord**, carregam todas as extensões e conferem se os comandos esperados foram registrados.

## 17. Como modificar

- **Mudar o status do bot:** altere `discord.Game(name=...)`. Também existe `discord.Activity(type=discord.ActivityType.listening, name="...")` para o status "Ouvindo".
- **Criar uma nova pasta de extensões:** adicione o nome em `EXTENSION_FOLDERS`.
- **Desligar a sincronização automática:** use `SYNC_COMMANDS=false` no `.env` depois que os comandos já estiverem registrados. Assim você evita chamadas desnecessárias à API.

## 18. Desafio

Faça o bot mostrar, no log, **quanto tempo** levou para carregar todas as extensões. Dica: use `time.perf_counter()` antes e depois do `for` dentro do `setup_hook` e registre a diferença com `logger.info`.
