# 05. Repetições

## Explicação

### `for`: para cada item

```python
for linguagem in ["Python", "JavaScript"]:
    print(linguagem)

for numero in range(5):        # 0, 1, 2, 3, 4
    print(numero)

for numero in range(2, 11, 2): # 2, 4, 6, 8, 10 (início, fim exclusivo, passo)
    print(numero)

for letra in "abc":            # strings também são percorridas
    print(letra)
```

### `while`: enquanto

```python
saldo = 100
while saldo > 0:
    saldo -= 30
    print("Saldo:", saldo)
```

### Controles

```python
for numero in range(10):
    if numero == 3:
        continue   # pula o 3
    if numero == 6:
        break      # para tudo no 6
    print(numero)  # 0 1 2 4 5
```

### Acumuladores e contadores

```python
total = 0
for preco in [10, 20, 30]:
    total += preco
print(total)  # 60
```

## Exemplo simples

```python
for i in range(1, 4):
    print(f"{i}º lugar")
```

## Código executável

[`examples/python-basics/05_repeticoes.py`](../../examples/python-basics/05_repeticoes.py)

## Aplicação no ProgramaBot

- [`main.py`](../code-explanation/main.md): `for` aninhado para descobrir extensões, com `continue` para pular os `__init__.py`.
- [`time_parser.py`](../code-explanation/utils/time_parser.md): acumulador `total_seconds += ...`.
- [`remind.py`](../code-explanation/commands/utility/remind.md): `for reminder in self.repository.get_due()`.
- [`confirm.py`](../code-explanation/views/confirm.md): `for item in self.children: item.disabled = True`.

## Exercício

1. Mostre a tabuada de um número escolhido pelo usuário.
2. Peça números ao usuário até ele digitar `0` e mostre a soma de todos (use `while`).
3. Percorra `"programabot"` e conte quantas vezes a letra `o` aparece.
