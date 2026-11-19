# 03. Coleções: listas, tuplas, dicionários e sets

## Explicação

Coleções guardam **vários valores** em uma única variável.

| Tipo | Sintaxe | Ordenada? | Pode mudar? | Repetidos? | Uso típico |
|---|---|---|---|---|---|
| `list` | `[1, 2, 3]` | sim | sim | sim | itens que mudam |
| `tuple` | `(1, 2, 3)` | sim | **não** | sim | itens fixos |
| `dict` | `{"a": 1}` | sim (ordem de inserção) | sim | chaves não | associar chave → valor |
| `set` | `{1, 2, 3}` | **não** | sim | **não** | itens únicos, buscas rápidas |

### Listas

```python
alunos = ["Ana", "Bruno"]
alunos.append("Carla")   # adiciona no final
alunos[0]                # "Ana"
alunos[-1]               # "Carla" (índices negativos contam do fim)
alunos[1:]               # ["Bruno", "Carla"] (fatiamento)
len(alunos)              # 3
alunos.remove("Bruno")
"Ana" in alunos          # True
```

### Tuplas

```python
CORES = ("vermelho", "verde", "azul")
CORES[0] = "rosa"        # ❌ TypeError: tuplas não podem ser alteradas
```

### Dicionários

```python
aluno = {"nome": "Ana", "nota": 9}
aluno["nome"]            # "Ana"
aluno["idade"] = 17      # adiciona uma chave
aluno.get("cidade")      # None (não dá erro)
for chave, valor in aluno.items():
    print(chave, valor)
```

### Sets

```python
vistos = {"python", "java"}
vistos.add("python")     # nada muda: não há repetidos
"java" in vistos         # True (busca muito rápida)
```

## Exemplo simples

```python
compras = ["arroz", "feijão"]
compras.append("café")
print(f"Tenho {len(compras)} itens: {', '.join(compras)}")
```

## Código executável

[`examples/python-basics/03_colecoes.py`](../../examples/python-basics/03_colecoes.py)

## Aplicação no ProgramaBot

| Coleção | Onde | Para quê |
|---|---|---|
| `list` | `parse_poll_options` em [`views/poll.py`](../code-explanation/views/poll.md) | opções da enquete |
| `tuple` | `STUDY_TIPS` em [`hello.py`](../code-explanation/commands/general/hello.md) | dicas fixas |
| `dict` | `HELP_CATEGORIES` em [`help_menu.py`](../code-explanation/views/help_menu.md) | catálogo de comandos |
| `dict` | `PollState.votes` | `{id_do_usuario: opção}`, um voto por pessoa |
| `set` | `seen` em `parse_poll_options` | detectar opções repetidas |

## Exercício

1. Crie uma lista com 5 linguagens. Mostre a primeira, a última e as três do meio.
2. Crie um dicionário `{"ana": 9, "bruno": 7, "carla": 8}` e mostre quem tirou nota maior que 7,5.
3. Dada a lista `[1, 2, 2, 3, 3, 3]`, use `set` para mostrar os números sem repetição.
