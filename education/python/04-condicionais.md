# 04. Condicionais

## Explicação

```python
if condição:
    ...            # executa se a condição for verdadeira
elif outra_condição:
    ...            # se a primeira for falsa e esta for verdadeira
else:
    ...            # se nenhuma for verdadeira
```

Recursos que o ProgramaBot usa bastante:

```python
# Comparação encadeada
if 5 <= hora < 12: ...

# Verificar None (use "is", não "==")
if membro is None: ...

# Verificar se uma coleção ou texto está vazio
if not opcoes: ...

# Pertencimento
if texto in ("sim", "s", "yes"): ...

# Expressão condicional (if em uma linha)
palavra = "voto" if quantidade == 1 else "votos"

# "Cláusula de guarda": sair cedo da função
def dividir(a, b):
    if b == 0:
        return None
    return a / b
```

### Valores "verdadeiros" e "falsos"

Em um `if`, estes valores contam como falso: `False`, `None`, `0`, `0.0`, `""`, `[]`, `{}`, `()`, `set()`. Todo o resto conta como verdadeiro.

## Exemplo simples

```python
temperatura = 31
if temperatura >= 30:
    print("Calor!")
elif temperatura >= 18:
    print("Agradável")
else:
    print("Frio")
```

## Código executável

[`examples/python-basics/04_condicionais.py`](../../examples/python-basics/04_condicionais.py)

## Aplicação no ProgramaBot

- [`hello.py`](../code-explanation/commands/general/hello.md): `greeting_for_hour` com comparações encadeadas.
- [`moderation.py`](../code-explanation/utils/moderation.md): uma sequência de cláusulas de guarda.
- [`kick.py`](../code-explanation/commands/moderation/kick.md): `if view.confirmed is None` antes de `if not view.confirmed`, um exemplo de como a ordem importa.

## Exercício

1. Escreva `classificar_imc(imc)` que retorne "abaixo do peso" (< 18,5), "normal" (< 25), "sobrepeso" (< 30) ou "obesidade".
2. Escreva `ano_bissexto(ano)`: divisível por 4 e não por 100, **ou** divisível por 400.
3. Por que `if view.confirmed is None` precisa vir antes de `if not view.confirmed`? Teste com os três valores possíveis.
