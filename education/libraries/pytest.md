# pytest (e pytest-asyncio)

## O que é?

O **pytest** é a ferramenta de testes automatizados mais popular do Python. O **pytest-asyncio** é um *plugin* que permite testar funções `async def`.

## Para que serve? Que problema resolve?

Testar à mão (abrir o Discord e usar cada comando) é lento, e é fácil esquecer algum caso. Um teste automatizado é um pequeno programa que verifica se outro programa funciona. Com `python -m pytest`, os mais de 200 testes do ProgramaBot rodam em poucos segundos.

Os testes também protegem contra **regressões**: quando você muda algo e, sem perceber, quebra outra parte.

## Como funciona?

1. O pytest procura arquivos `test_*.py` na pasta `tests/`.
2. Dentro deles, executa as funções que começam com `test_`.
3. Cada `assert` verifica uma condição. Se ela for falsa, o teste falha e o pytest mostra os valores envolvidos.

## Nativa ou externa?

**Externa.** É uma dependência de **desenvolvimento**: o bot não precisa dela para rodar.

## Como instalar

```bash
pip install -r requirements-dev.txt
```

## Como importar

```python
import pytest
```

Para escrever testes simples, nem é preciso importar: o `assert` é do próprio Python.

## Recursos utilizados no ProgramaBot

| Recurso | Onde | Explicação |
|---|---|---|
| `assert condição` | todos os testes | Verificação. |
| `pytest.raises(Erro, match="texto")` | vários | Confirma que um erro **é** lançado. |
| `@pytest.mark.parametrize("a, b", [...])` | vários | Roda o mesmo teste com vários valores. |
| `@pytest.fixture` | `conftest.py`, `test_config.py`, `test_reminders.py` | Prepara dados ou objetos reutilizáveis. |
| `tmp_path` (fixture nativa) | vários | Pasta temporária, apagada depois. |
| `monkeypatch` (fixture nativa) | `test_config.py` | Altera variáveis de ambiente só durante o teste. |
| `conftest.py` | `tests/` | Fixtures compartilhadas por todos os arquivos. |
| `pytest.ini` | raiz | Configurações (pasta dos testes, modo async). |
| `async def test_...` | `test_extensions.py`, `test_poll.py` | Testes assíncronos (pytest-asyncio com `asyncio_mode = auto`). |

## Exemplo independente do ProgramaBot

```python
# arquivo: test_matematica.py
import pytest


def dobro(numero: int) -> int:
    return numero * 2


def test_dobro():
    assert dobro(3) == 6


@pytest.mark.parametrize(("entrada", "esperado"), [(0, 0), (-2, -4), (10, 20)])
def test_dobro_varios(entrada, esperado):
    assert dobro(entrada) == esperado


def test_divisao_por_zero():
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

```bash
python -m pytest test_matematica.py -v
```

## Comandos úteis

```bash
python -m pytest                          # todos os testes
python -m pytest -v                       # mostra o nome de cada teste
python -m pytest tests/test_calculator.py # um arquivo
python -m pytest -k dice                  # testes cujo nome contém "dice"
python -m pytest -x                       # para no primeiro erro
```

Use `python -m pytest` (e não só `pytest`) para garantir o uso do Python do ambiente virtual.

## Documentação oficial

- pytest: <https://docs.pytest.org/>
- pytest-asyncio: <https://pytest-asyncio.readthedocs.io/>

Veja também: [Boas práticas: testes](../best-practices/04-testes.md).
