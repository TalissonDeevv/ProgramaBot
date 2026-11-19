# logging

## O que é?

O sistema oficial de **registros** (*logs*) do Python: mensagens que o programa escreve sobre o que está fazendo, com data, nível de importância e origem.

## Para que serve? Que problema resolve?

`print()` serve para mostrar algo rapidamente, mas não informa **quando** a mensagem foi escrita, **de onde** veio nem **quão importante** é, e não grava em arquivo sozinho. Em um bot que fica ligado por dias, o log é como a caixa-preta de um avião: quando algo dá errado, é nele que você descobre o motivo.

## Como funciona?

Quatro peças trabalham juntas:

| Peça | Função | No ProgramaBot |
|---|---|---|
| **Logger** | Recebe as mensagens. Cada módulo tem o seu. | `logger = logging.getLogger(__name__)` |
| **Nível** | Filtra por importância. | `LOG_LEVEL` no `.env` |
| **Handler** | Decide **para onde** a mensagem vai. | terminal + arquivo |
| **Formatter** | Decide **como** a linha fica. | `LOG_FORMAT` |

Os níveis, do menos ao mais grave: `DEBUG` < `INFO` < `WARNING` < `ERROR` < `CRITICAL`. Com o nível `INFO`, `DEBUG` é ignorado e o resto aparece.

Os loggers formam uma hierarquia pelos nomes: `bot.commands.utility.remind` é "filho" de `bot`, que é filho do logger **raiz**. Ao configurar o logger raiz, todos herdam a configuração.

## Nativa ou externa?

**Nativa.**

## Como importar

```python
import logging
from logging.handlers import RotatingFileHandler
```

## Funções e classes utilizadas no ProgramaBot

| Item | Onde | Explicação |
|---|---|---|
| `logging.getLogger(__name__)` | quase todos os arquivos | Logger com o nome do módulo. |
| `logging.getLogger()` | `logger.py` | Logger raiz. |
| `logger.debug/info/warning/error(msg, *args)` | vários | Registra uma mensagem. Os `%s` são preenchidos com `args`. |
| `logger.exception(msg)` | `main.py`, `remind.py`, `embed_modal.py` | Como `error`, mas inclui o traceback. Use dentro de `except`. |
| `logger.error(msg, exc_info=erro)` | `errors.py` | Registra o traceback de uma exceção recebida como argumento. |
| `logging.Formatter(fmt, datefmt)` | `logger.py` | Formato das linhas. |
| `logging.StreamHandler()` | `logger.py` | Envia para o terminal. |
| `RotatingFileHandler(arquivo, maxBytes, backupCount, encoding)` | `logger.py` | Grava em arquivo e cria arquivos novos quando o atual enche. |
| `logger.setLevel(nivel)` | `logger.py` | Nível mínimo. |
| `logger.addHandler(h)` / `logger.handlers.clear()` | `logger.py` | Adiciona / remove handlers. |

## Exemplo independente do ProgramaBot

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("loja")

log.info("Loja aberta")
log.debug("Isto não aparece, porque o nível é INFO")
try:
    1 / 0
except ZeroDivisionError:
    log.exception("Erro ao calcular o desconto")
```

`logging.basicConfig` é o jeito mais rápido de configurar logs em scripts pequenos. O ProgramaBot configura manualmente para ter também o arquivo rotativo.

## Por que `logger.info("Olá %s", nome)` e não uma f-string?

Com `%s`, o texto só é montado se a mensagem for exibida. Com f-string, é montado sempre. Em mensagens `DEBUG` frequentes, isso economiza processamento. Além disso, ferramentas de análise de logs conseguem agrupar mensagens com o mesmo modelo.

## Documentação oficial

- Referência: <https://docs.python.org/pt-br/3/library/logging.html>
- Tutorial (recomendado): <https://docs.python.org/pt-br/3/howto/logging.html>
