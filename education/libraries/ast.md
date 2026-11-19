# ast

## O que é?

O módulo `ast` (*Abstract Syntax Tree*, árvore de sintaxe abstrata) transforma código Python, em forma de texto, em uma **árvore de objetos** que representa a estrutura do código, **sem executá-lo**.

## Para que serve? Que problema resolve?

Ferramentas que analisam código (formatadores, verificadores de erros, IDEs) usam árvores de sintaxe. No ProgramaBot, o `ast` resolve um problema de **segurança**: permite que a calculadora entenda uma expressão matemática digitada pelo usuário sem usar `eval()`, que executaria qualquer código.

## Como funciona?

Quando o Python lê seu código, ele primeiro transforma o texto em uma árvore e só depois executa. O `ast` nos dá acesso a essa etapa intermediária:

```python
>>> import ast
>>> print(ast.dump(ast.parse("2 + 3 * 4", mode="eval"), indent=2))
Expression(
  body=BinOp(
    left=Constant(value=2),
    op=Add(),
    right=BinOp(
      left=Constant(value=3),
      op=Mult(),
      right=Constant(value=4))))
```

Repare que a árvore já respeita a precedência dos operadores: a multiplicação fica "mais funda" e é calculada primeiro.

## Nativa ou externa?

**Nativa.**

## Como importar

```python
import ast
```

## Classes e funções utilizadas no ProgramaBot

| Item | Explicação |
|---|---|
| `ast.parse(texto, mode="eval")` | Analisa o texto como **uma expressão**. Lança `SyntaxError` se o texto for inválido. |
| `ast.Expression.body` | O nó principal. |
| `ast.Constant` | Um valor literal (`2`, `3.5`, `"texto"`, `True`). |
| `ast.BinOp` | Operação com dois lados: `.left`, `.op` e `.right`. |
| `ast.UnaryOp` | Operação com um lado (`-5`): `.op` e `.operand`. |
| `ast.Add`, `ast.Sub`, `ast.Mult`, `ast.Div`, `ast.FloorDiv`, `ast.Mod`, `ast.Pow` | Os operadores `+ - * / // % **`. |
| `ast.UAdd`, `ast.USub` | `+x` e `-x`. |

Tudo isso está em [`bot/utils/calculator.py`](../code-explanation/utils/calculator.md).

## Por que isso é seguro?

O `ast.parse` **só analisa**, não executa. Depois, nosso código percorre a árvore e só aceita os tipos de nó da tabela acima. Uma chamada de função como `open("arquivo")` vira um nó `ast.Call`, que não está na lista, e é recusada.

> Existe também `ast.literal_eval`, que avalia com segurança literais como `"[1, 2, 3]"`. Ele não serve para a calculadora porque não aceita a maioria dos operadores matemáticos.

## Exemplo independente do ProgramaBot

Contar quantas funções existem em um arquivo Python:

```python
import ast
from pathlib import Path

codigo = Path(__file__).read_text(encoding="utf-8")
arvore = ast.parse(codigo)

for no in ast.walk(arvore):
    if isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef)):
        print("Função encontrada:", no.name, "na linha", no.lineno)
```

## Documentação oficial

- <https://docs.python.org/pt-br/3/library/ast.html>
