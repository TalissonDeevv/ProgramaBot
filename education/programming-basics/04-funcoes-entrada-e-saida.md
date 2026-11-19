# 04. Funções, entrada e saída

## Funções

### Explicação

Uma **função** é um bloco de código com nome, que executa uma tarefa e pode ser **reutilizado**. É como uma receita que você escreve uma vez e prepara quantas vezes quiser.

```python
def saudar(nome):
    print(f"Olá, {nome}!")

saudar("Ana")
saudar("Bruno")
```

- `def` define a função.
- `nome` é um **parâmetro**: uma "entrada" da função.
- `"Ana"` é o **argumento**: o valor real enviado ao chamar a função.

Funções podem **devolver** um resultado com `return`:

```python
def dobro(numero):
    return numero * 2

resultado = dobro(21)   # 42
```

Por que usar funções? Para **evitar repetição**, **dar nome** a uma ideia e **dividir** um problema grande em partes pequenas.

## Entrada e saída

### Explicação

- **Saída** é o que o programa mostra: `print(...)`.
- **Entrada** é o que o programa recebe do usuário: `input(...)`.

```python
nome = input("Qual é o seu nome? ")
print("Prazer,", nome)
```

`input` **sempre** devolve texto. Para fazer contas, converta o valor:

```python
idade = int(input("Sua idade: "))     # int → número inteiro
altura = float(input("Sua altura: ")) # float → número com casas decimais
```

## Código executável

```python
def calcular_media(nota1, nota2):
    return (nota1 + nota2) / 2


def situacao(media):
    if media >= 7:
        return "Aprovado"
    return "Reprovado"


nome = input("Nome do aluno: ")
n1 = float(input("Primeira nota: "))
n2 = float(input("Segunda nota: "))

media = calcular_media(n1, n2)
print(f"{nome}: média {media:.1f} — {situacao(media)}")
```

`:.1f` dentro da f-string mostra o número com uma casa decimal.

## Aplicação prática no ProgramaBot

Em um bot, a **entrada** não vem do `input()`, e sim do Discord: o parâmetro de um slash command. A **saída** não é o `print()`, e sim `interaction.response.send_message(...)`.

| Programa de terminal | ProgramaBot |
|---|---|
| `nome = input("Nome: ")` | `/hello nome:Ana` → parâmetro `nome` |
| `print("Olá")` | `await interaction.response.send_message("Olá")` |

Funções pequenas e reutilizáveis estão em toda parte, por exemplo `greeting_for_hour(hour)` em [`hello.py`](../code-explanation/commands/general/hello.md) e `success_embed(...)` em [`embeds.py`](../code-explanation/utils/embeds.md).

## Exercício

1. Crie uma função `area_retangulo(base, altura)` que **retorne** a área. Mostre a área de um retângulo 5 × 3.
2. Crie uma função `e_par(numero)` que retorne `True` ou `False`.
3. Peça ao usuário dois números com `input` e mostre a soma. O que acontece se você esquecer de converter com `int()`? (Dica: `"2" + "3"` dá `"23"`.)
