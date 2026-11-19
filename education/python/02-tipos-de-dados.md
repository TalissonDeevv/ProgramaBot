# 02. Tipos de dados: strings, inteiros, floats e booleanos

## Explicação

| Tipo | Nome | Exemplos | Para quê |
|---|---|---|---|
| `str` | string (texto) | `"Olá"`, `'Python'` | nomes, mensagens |
| `int` | inteiro | `10`, `-3`, `0` | contagens, IDs |
| `float` | ponto flutuante | `3.14`, `0.5` | medidas, médias |
| `bool` | booleano | `True`, `False` | sim/não, condições |
| `NoneType` | nulo | `None` | "nenhum valor" |

Use `type(valor)` para descobrir o tipo.

### Strings

```python
texto = "  ProgramaBot  "
texto.strip()        # "ProgramaBot" (remove espaços das pontas)
texto.lower()        # "  programabot  "
texto.upper()        # "  PROGRAMABOT  "
"bot" in "ProgramaBot".lower()   # True
"a,b,c".split(",")   # ["a", "b", "c"]
len("Python")        # 6
"Py" + "thon"        # "Python"
"ha" * 3             # "hahaha"
"Python"[0]          # "P" (o primeiro caractere fica no índice 0)
```

### Números

```python
10 / 3     # 3.3333333333333335 (divisão sempre resulta em float)
10 // 3    # 3
round(3.14159, 2)   # 3.14
0.1 + 0.2  # 0.30000000000000004 (limitação da representação binária)
```

### Conversões

```python
int("42")      # 42
float("2.5")   # 2.5
str(10)        # "10"
bool(0)        # False (0, "", [] e None são considerados "falsos")
int("abc")     # ❌ ValueError
```

## Exemplo simples

```python
preco = 19.9
quantidade = 3
total = preco * quantidade
print(f"Total: R$ {total:.2f}")   # :.2f → duas casas decimais
```

## Código executável

[`examples/python-basics/02_tipos.py`](../../examples/python-basics/02_tipos.py)

## Aplicação no ProgramaBot

- **Strings**: [`config.py`](../code-explanation/config.md) usa `.strip()`, `.lower()` e `.upper()` para limpar o que veio do `.env`.
- **Conversões**: `int(value.strip())` transforma o ID do `.env` em número.
- **Float vs. int**: [`format_result`](../code-explanation/utils/calculator.md) transforma `4.0` em `"4"`.
- **`None`**: `guild_id: int | None = None` significa "pode não ter servidor configurado".

## Exercício

1. Peça uma palavra com `input` e mostre: quantas letras tem, a palavra em maiúsculas e a primeira letra.
2. Converta `"3.7"` para `float` e depois para `int`. Qual é o resultado? E `int("3.7")` direto, funciona?
3. Mostre `bool("")`, `bool("0")` e `bool(0)`. Por que o segundo é `True`?
