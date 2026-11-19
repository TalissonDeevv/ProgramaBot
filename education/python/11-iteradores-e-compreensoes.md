# 11. Iteradores e compreensões de lista

## Explicação

### Iteráveis e iteradores

Um **iterável** é qualquer coisa que pode ser percorrida com `for`: listas, tuplas, strings, dicionários, `range`, arquivos. Por baixo dos panos, o `for` pede ao iterável um **iterador** (`iter()`) e chama `next()` até acabar:

```python
numeros = [10, 20]
it = iter(numeros)
next(it)  # 10
next(it)  # 20
next(it)  # StopIteration → é assim que o for sabe que acabou
```

### Funções úteis

```python
for indice, nome in enumerate(["Ana", "Bruno"]):   # índice + valor
    print(indice, nome)                           # 0 Ana / 1 Bruno

for nome, nota in zip(["Ana", "Bruno"], [9, 7]):   # percorre duas listas juntas
    print(nome, nota)

for item in reversed([1, 2, 3]): ...              # de trás para frente
sorted(["c", "a", "b"])                           # ["a", "b", "c"]
any(n > 5 for n in [1, 7])                        # True: algum maior que 5?
all(n > 0 for n in [1, 7])                        # True: todos positivos?
sum(n for n in range(4))                          # 6
```

### Compreensão de lista

Uma forma curta de criar uma lista a partir de outra:

```python
quadrados = [n * n for n in range(5)]             # [0, 1, 4, 9, 16]
pares = [n for n in range(10) if n % 2 == 0]      # com filtro
nomes = [nome.title() for nome in ["ana", "bia"]] # ["Ana", "Bia"]
```

O equivalente "longo":

```python
quadrados = []
for n in range(5):
    quadrados.append(n * n)
```

Também existem compreensões de **dicionário** e **set**:

```python
{nome: len(nome) for nome in ["Ana", "Bruno"]}    # {"Ana": 3, "Bruno": 5}
{letra for letra in "banana"}                     # {"b", "a", "n"}
```

E **expressões geradoras** (com parênteses), que produzem os valores um a um, sem criar a lista inteira na memória.

> Use compreensões quando ficarem **curtas e legíveis**. Se precisar de várias condições, um `for` normal é mais claro.

## Exemplo simples

```python
precos = [10.0, 25.5, 8.0]
com_desconto = [p * 0.9 for p in precos]
print(com_desconto)
```

## Código executável

[`examples/python-basics/03_colecoes.py`](../../examples/python-basics/03_colecoes.py) (parte final)

## Aplicação no ProgramaBot

| Recurso | Onde |
|---|---|
| Compreensão de lista | `roll_dice` em [`dice.py`](../code-explanation/commands/fun/dice.md); opções do menu em [`help_menu.py`](../code-explanation/views/help_menu.md) |
| `enumerate` | botões da enquete em [`views/poll.py`](../code-explanation/views/poll.md) |
| `zip` | `result_lines` em `views/poll.py` |
| `reversed` | cargos em [`userinfo.py`](../code-explanation/commands/information/userinfo.md) |
| `any` | validação de cor em [`embeds.py`](../code-explanation/utils/embeds.md) |
| `all` | validação do JSON em [`fact.py`](../code-explanation/commands/fun/fact.md) |
| `sorted` + `rglob` | descoberta de extensões em [`main.py`](../code-explanation/main.md) |

## Exercício

1. Com compreensão de lista, gere os múltiplos de 7 entre 1 e 100.
2. Dada `palavras = ["python", "é", "muito", "legal"]`, crie uma lista só com as palavras de mais de 3 letras, em maiúsculas.
3. Use `zip` para criar o dicionário `{"Ana": 9, "Bruno": 7}` a partir de duas listas.
