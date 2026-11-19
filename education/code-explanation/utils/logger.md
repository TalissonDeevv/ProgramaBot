# `bot/utils/logger.py`: logs do bot

## 1. Nome e localização

- **Arquivo:** `bot/utils/logger.py`
- **Arquivo gerado:** `logs/programabot.log` (ignorado pelo Git)

## 2. Finalidade

Configura o sistema de **logs**: as mensagens que o bot escreve para contar o que está fazendo. Elas aparecem no terminal e também ficam salvas em arquivo.

```
19/11/2026 14:02:11 | INFO     | bot.main | Extensão carregada: bot.commands.general.ping
19/11/2026 14:02:13 | INFO     | bot.events.ready | Conectado como ProgramaBot#1234 (ID: 1234...)
```

## 3. Por que foi criado

Usar `print()` funciona, mas o `logging` oferece mais recursos:

- **níveis** (DEBUG, INFO, WARNING, ERROR, CRITICAL), para filtrar o que aparece;
- **data, hora e origem** em cada linha;
- **arquivo de histórico**, útil para descobrir o que aconteceu quando você não estava olhando;
- **tracebacks completos** com `logger.exception(...)`.

## 4. Como se conecta ao restante do bot

- [`main.py`](../main.md) chama `setup_logging(settings.log_level, PROJECT_ROOT / "logs")` logo no início.
- Os outros arquivos só criam `logger = logging.getLogger(__name__)` e escrevem mensagens. A configuração feita aqui vale para todos eles.

## 5. Bibliotecas utilizadas

- [`logging`](../../libraries/logging.md) (nativa), incluindo o submódulo `logging.handlers`.
- [`pathlib`](../../libraries/pathlib.md) (nativa).

## 6. Importações

```python
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
```

`RotatingFileHandler` fica em um submódulo (`logging.handlers`), por isso tem um import separado.

## 7. Conceitos de Python utilizados

- Constantes em maiúsculas.
- Parâmetros com valor padrão e `None` como "desativado".
- Separador de milhar em números: `1_000_000` é o mesmo que `1000000`, só que mais legível.
- Objetos e métodos: criar um *handler*, configurá-lo e adicioná-lo ao *logger*.

## 8. Variáveis e constantes

| Constante | Significado |
|---|---|
| `LOG_FORMAT` | Modelo de cada linha. `%(asctime)s` = data/hora, `%(levelname)-8s` = nível alinhado em 8 colunas, `%(name)s` = módulo de origem, `%(message)s` = a mensagem. |
| `DATE_FORMAT` | `%d/%m/%Y %H:%M:%S`, o formato brasileiro de data. |
| `LOG_FILE_NAME` | `programabot.log` |
| `MAX_LOG_BYTES` | Tamanho máximo de cada arquivo (1 MB). |
| `BACKUP_COUNT` | Quantos arquivos antigos manter (`.log.1`, `.log.2`, `.log.3`). |

## 9. Funções

**`setup_logging(level="INFO", log_dir=None)`** configura o *logger raiz*, o "pai" de todos os loggers do programa.

## 10. Parâmetros

- `level`: nível mínimo. Com `"INFO"`, mensagens `DEBUG` são ignoradas.
- `log_dir`: pasta do arquivo de log. Com `None`, o log aparece só no terminal.

## 11. Métodos utilizados

| Método | Explicação |
|---|---|
| `logging.Formatter(fmt, datefmt)` | Define a aparência das linhas. |
| `logging.getLogger()` | Sem argumento, devolve o logger raiz. |
| `logger.setLevel(level)` | Define o nível mínimo. Aceita o texto `"INFO"` ou a constante `logging.INFO`. |
| `logger.handlers.clear()` | Remove os *handlers* antigos, o que evita linhas duplicadas. |
| `logging.StreamHandler()` | *Handler* que escreve no terminal. |
| `RotatingFileHandler(...)` | *Handler* que escreve em arquivo e "gira" quando o arquivo enche. |
| `handler.setFormatter(f)` | Aplica o formato ao handler. |
| `logger.addHandler(h)` | Conecta o handler ao logger. |
| `Path.mkdir(parents=True, exist_ok=True)` | Cria a pasta (e as pastas-mãe); não dá erro se ela já existir. |

## 12. Funcionamento do código

O `logging` funciona como uma linha de produção:

```
logger.info("msg") → Logger (filtra por nível) → Handler(s) → Formatter → terminal / arquivo
```

```python
root_logger = logging.getLogger()
root_logger.setLevel(level)
root_logger.handlers.clear()
```

Configurar o logger raiz faz com que **todos** os loggers do programa herdem essa configuração, inclusive os do discord.py (`discord.gateway`, `discord.client`...).

```python
file_handler = RotatingFileHandler(
    log_dir / LOG_FILE_NAME,
    maxBytes=MAX_LOG_BYTES,
    backupCount=BACKUP_COUNT,
    encoding="utf-8",
)
```

Quando `programabot.log` passa de 1 MB, ele é renomeado para `programabot.log.1` e um arquivo novo começa. `encoding="utf-8"` garante que acentos e emojis sejam salvos corretamente no Windows.

```python
logging.getLogger("discord.http").setLevel(logging.WARNING)
```

O discord.py registra cada requisição HTTP. Aqui limitamos esse logger específico a avisos e erros, para o terminal não ficar poluído.

## 13. Fluxo de execução

```
main.run_bot()
 └─ setup_logging("INFO", .../logs)
     ├─ cria o Formatter
     ├─ limpa os handlers do logger raiz
     ├─ adiciona o StreamHandler (terminal)
     ├─ cria a pasta logs/ e adiciona o RotatingFileHandler
     └─ silencia discord.http abaixo de WARNING
```

## 14. Exemplos práticos

```python
import logging
from bot.utils.logger import setup_logging

setup_logging("DEBUG")
log = logging.getLogger("meu_teste")
log.debug("Detalhe técnico")
log.info("Tudo certo")
log.warning("Cuidado")
log.error("Algo falhou")
```

## 15. Erros comuns

- **Mensagens duplicadas:** acontece quando um handler é adicionado duas vezes. O `handlers.clear()` existe para evitar isso.
- **Usar f-string no log:** prefira `logger.info("Olá %s", nome)` a `logger.info(f"Olá {nome}")`. Com `%s`, o texto só é montado se a mensagem for realmente exibida.
- **Não encontro o arquivo de log:** ele fica em `logs/programabot.log`, na raiz do projeto, e só é criado quando o bot roda.

## 16. Como testar

Rode o bot com `LOG_LEVEL=DEBUG` no `.env` e compare com `INFO`. Depois, abra `logs/programabot.log` no VS Code.

## 17. Como modificar

- Para mudar o formato, edite `LOG_FORMAT`. Por exemplo, adicione `%(lineno)d` para mostrar o número da linha.
- Para guardar mais histórico, aumente `BACKUP_COUNT`.

## 18. Desafio

Crie um segundo arquivo, `logs/erros.log`, que receba **apenas** mensagens de nível `ERROR` ou superior. Dica: crie outro `RotatingFileHandler` e chame `handler.setLevel(logging.ERROR)` nele.
