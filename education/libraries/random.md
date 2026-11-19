# random

## O que é?

O módulo de **números e escolhas aleatórias** do Python.

## Para que serve? Que problema resolve?

Jogos, sorteios, dicas variadas e testes com dados diferentes precisam de aleatoriedade. O `random` gera números *pseudoaleatórios*: parecem aleatórios, mas são calculados por um algoritmo a partir de uma **semente** (*seed*).

## Como funciona?

O algoritmo (*Mersenne Twister*) parte de uma semente e produz uma sequência que parece imprevisível. Com a mesma semente, a sequência se repete. Isso é ótimo para testes:

```python
random.seed(42)
print(random.randint(1, 6))  # sempre o mesmo número com a semente 42
```

> ⚠️ O `random` **não** é seguro para criptografia (senhas, tokens). Para isso existe o módulo `secrets`.

## Nativa ou externa?

**Nativa.**

## Como importar

```python
import random
```

## Funções utilizadas no ProgramaBot

| Função | Onde | Explicação |
|---|---|---|
| `random.choice(sequencia)` | `hello.py`, `fact.py` | Um item aleatório de uma lista ou tupla. |
| `random.randint(a, b)` | `dice.py` | Inteiro entre `a` e `b`, **incluindo os dois**. |
| `random.seed(valor)` | `tests/test_command_helpers.py` | Fixa a semente para resultados reproduzíveis. |

## Exemplo independente do ProgramaBot

```python
import random

nomes = ["Ana", "Bruno", "Carla", "Diego"]

print("Sorteado:", random.choice(nomes))
print("Dado:", random.randint(1, 6))
print("Três sem repetir:", random.sample(nomes, 3))

random.shuffle(nomes)   # embaralha a própria lista
print("Embaralhados:", nomes)

print("Entre 0 e 1:", random.random())
```

## Documentação oficial

- <https://docs.python.org/pt-br/3/library/random.html>
