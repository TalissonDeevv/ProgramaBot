# 06. Funções: parâmetros, argumentos e retornos

## Explicação

```python
def nome_da_funcao(parametro1, parametro2="padrão"):
    """Docstring: explica o que a função faz."""
    resultado = ...
    return resultado
```

- **Parâmetro**: a variável na definição (`parametro1`).
- **Argumento**: o valor passado na chamada.
- **`return`**: devolve um valor e **encerra** a função. Sem `return`, a função devolve `None`.

### Formas de passar argumentos

```python
def apresentar(nome, idade, cidade="não informada"):
    print(f"{nome}, {idade} anos, {cidade}")

apresentar("Ana", 20)                     # posicionais
apresentar("Ana", 20, "Natal")            # sobrescreve o padrão
apresentar(idade=20, nome="Ana")          # nomeados (a ordem não importa)
```

### Parâmetros especiais

```python
def somar(*numeros):          # quantidade variável → tupla
    return sum(numeros)

somar(1, 2, 3)                # 6

def configurar(*, cor, tamanho):   # tudo depois de * deve ser passado com nome
    ...

configurar(cor="azul", tamanho=3)
```

### Type hints (dicas de tipo)

```python
def dobro(numero: int) -> int:
    return numero * 2
```

Elas não mudam o funcionamento, mas documentam a função e ajudam o editor a apontar erros.

### Escopo

Variáveis criadas dentro de uma função só existem dentro dela.

## Exemplo simples

```python
def celsius_para_fahrenheit(celsius: float) -> float:
    return celsius * 9 / 5 + 32

print(celsius_para_fahrenheit(25))  # 77.0
```

## Código executável

[`examples/python-basics/06_funcoes.py`](../../examples/python-basics/06_funcoes.py)

## Aplicação no ProgramaBot

- **Valor padrão**: `base_embed(title, description=None, color=PRIMARY_COLOR)` em [`embeds.py`](../code-explanation/utils/embeds.md).
- **Argumentos nomeados**: `self.repository.add(user_id=..., channel_id=..., message=..., remind_at=...)` em [`remind.py`](../code-explanation/commands/utility/remind.md).
- **`*` (somente nomeados)**: `async def hello_prefix(self, ctx, *, nome=None)` em [`prefix_examples.py`](../code-explanation/commands/general/prefix_examples.md).
- **Retornar `None` como "sem problema"**: `check_hierarchy` em [`moderation.py`](../code-explanation/utils/moderation.md).
- **Parâmetros de comando** viram campos no Discord: `/dice lados:20 quantidade:3`.

## Exercício

1. Crie `calcular_desconto(preco, porcentagem=10)` que retorne o preço com desconto.
2. Crie `maior(*numeros)` sem usar `max()`.
3. Crie `formatar_nome(nome, sobrenome, *, maiusculas=False)` e chame-a com e sem `maiusculas=True`.
