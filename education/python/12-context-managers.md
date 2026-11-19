# 12. Context managers (`with`)

## Explicação

Alguns recursos precisam ser **liberados** depois do uso: arquivos abertos, conexões com banco de dados, conexões de rede. Se você esquecer de fechá-los, ou se acontecer um erro no meio, eles ficam presos.

Um **context manager** garante a preparação e a limpeza automática, com a instrução `with`:

```python
with open("notas.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write("Estudar Python")
# aqui o arquivo JÁ foi fechado, mesmo que tenha ocorrido um erro
```

É o equivalente seguro de:

```python
arquivo = open("notas.txt", "w", encoding="utf-8")
try:
    arquivo.write("Estudar Python")
finally:
    arquivo.close()
```

### Como funciona por dentro

Um objeto é um context manager se tiver os métodos `__enter__` (executado no início do `with`) e `__exit__` (executado no fim, com ou sem erro).

```python
class Cronometro:
    def __enter__(self):
        import time
        self.inicio = time.perf_counter()
        return self

    def __exit__(self, tipo_erro, erro, traceback):
        import time
        print(f"Levou {time.perf_counter() - self.inicio:.3f}s")
        return False  # False: não esconde o erro, se houver


with Cronometro():
    sum(range(1_000_000))
```

### Context managers assíncronos

Com `async with`, os métodos são `__aenter__` e `__aexit__` e podem usar `await`.

## Exemplo simples

```python
from pathlib import Path

with Path("ola.txt").open("w", encoding="utf-8") as f:
    f.write("Olá!")
```

## Código executável

[`examples/python-basics/10_decorators_e_context_managers.py`](../../examples/python-basics/10_decorators_e_context_managers.py)

## Aplicação no ProgramaBot

| Uso | Onde | O que garante |
|---|---|---|
| `with path.open(...) as file:` | [`fact.py`](../code-explanation/commands/fun/fact.md) | fecha o arquivo JSON |
| `with connection:` | [`reminders.py`](../code-explanation/database/reminders.md) | `commit` ou `rollback` da transação |
| `try/finally: connection.close()` | `reminders.py` | fecha a conexão (o `with connection` **não** fecha) |
| `async with bot:` | [`main.py`](../code-explanation/main.md) | fecha o bot e as conexões ao sair |
| `async with bot:` | `tests/conftest.py` | prepara e encerra o bot nos testes |
| `with pytest.raises(...)` | testes | verifica se um erro acontece dentro do bloco |

## Exercício

1. Escreva um programa que grave três linhas em `diario.txt` usando `with` e depois as leia de volta.
2. Crie um context manager `Mensagem` que imprima "Início" no `__enter__` e "Fim" no `__exit__`.
3. No `__exit__`, o que acontece se você retornar `True` quando houver um erro? Teste com `with Mensagem(): 1 / 0`. Por que isso é perigoso?
