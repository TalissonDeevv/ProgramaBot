# pathlib

## O que é?

Um módulo que representa **caminhos de arquivos e pastas** como objetos (`Path`), em vez de textos soltos.

## Para que serve? Que problema resolve?

Caminhos mudam de sistema para sistema: o Windows usa `C:\Users\...` e o Linux usa `/home/...`. Montá-los "colando" textos gera erros. O `pathlib` resolve isso:

```python
pasta = Path("data")
arquivo = pasta / "programabot.db"   # o operador / junta caminhos, em qualquer sistema
```

## Como funciona?

`Path` é uma classe. Cada objeto guarda um caminho e oferece métodos para consultar e manipular esse caminho e o arquivo que ele representa.

## Nativa ou externa?

**Nativa.**

## Como importar

```python
from pathlib import Path
```

## Métodos e atributos utilizados no ProgramaBot

| Item | Onde | Explicação |
|---|---|---|
| `Path(__file__)` | `config.py`, `main.py`, `fact.py` | Caminho do arquivo atual. |
| `.resolve()` | idem | Converte em caminho absoluto, sem `..`. |
| `.parent` / `.parents[n]` | idem | Pasta-mãe / n níveis acima. |
| `caminho / "nome"` | vários | Junta caminhos. |
| `.rglob("*.py")` | `main.py` | Procura arquivos em todas as subpastas. |
| `.relative_to(base)` | `main.py` | Caminho relativo a outra pasta. |
| `.with_suffix("")` | `main.py` | Troca (ou remove) a extensão. |
| `.parts` | `main.py` | Tupla com as partes do caminho. |
| `.name` | `main.py`, `fact.py` | Nome do arquivo (`ping.py`). |
| `.is_absolute()` | `config.py` | O caminho é absoluto? |
| `.mkdir(parents=True, exist_ok=True)` | `logger.py`, `reminders.py` | Cria a pasta, inclusive as intermediárias. |
| `.open(encoding="utf-8")` | `fact.py` | Abre o arquivo. |

## Exemplo independente do ProgramaBot

```python
from pathlib import Path

aqui = Path(__file__).resolve().parent
notas = aqui / "notas"
notas.mkdir(exist_ok=True)

arquivo = notas / "lembrete.txt"
arquivo.write_text("Estudar pathlib", encoding="utf-8")
print(arquivo.read_text(encoding="utf-8"))

for item in aqui.glob("*.py"):
    print("Script encontrado:", item.name)
```

## Por que usar `Path(__file__)` em vez de caminhos como `"data/arquivo.db"`?

Caminhos relativos dependem da **pasta em que o terminal está aberto**. Se você rodar o bot de outra pasta, `"data/arquivo.db"` apontaria para o lugar errado. Com `Path(__file__).resolve().parent`, o caminho é calculado a partir do próprio arquivo de código e funciona de qualquer lugar.

## Documentação oficial

- <https://docs.python.org/pt-br/3/library/pathlib.html>
