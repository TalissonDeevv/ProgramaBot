# `bot/utils/calculator.py`: a calculadora segura

## 1. Nome e localização

- **Arquivo:** `bot/utils/calculator.py`
- **Usado por:** [`commands/general/calculator.py`](../commands/general/calculator.md) e [`commands/general/prefix_examples.py`](../commands/general/prefix_examples.md)

## 2. Finalidade

Calcular expressões como `2 + 3 * (4 - 1)` digitadas por usuários do Discord, **sem nunca executar código arbitrário**.

## 3. Por que foi criado

A forma "fácil" de fazer uma calculadora em Python seria:

```python
resultado = eval(texto_do_usuario)  # ❌ NUNCA faça isso em um bot
```

`eval` executa **qualquer** código Python. Se alguém digitar `__import__('os').system('...')`, o comando seria executado no computador onde o bot roda. Isso é uma falha grave de segurança, chamada *execução remota de código*.

A solução segura é **analisar** a expressão antes de calculá-la e aceitar apenas números e operações matemáticas. Para isso usamos o módulo `ast`.

## 4. Como se conecta ao restante do bot

- `/calculator` chama `calculate()` e mostra `format_result()`.
- `!soma` usa `format_result()` para exibir números bonitos.
- `MAX_EXPRESSION_LENGTH` também é usado no comando para limitar o tamanho do texto no próprio Discord.

## 5. Bibliotecas utilizadas

- [`ast`](../../libraries/ast.md) (nativa): transforma texto em uma árvore de sintaxe.

## 6. Importações

```python
import ast
```

## 7. Conceitos de Python utilizados

- **Recursão**: `_evaluate` chama a si mesma para calcular partes da expressão.
- **`isinstance`**: verifica o tipo de um objeto.
- **Exceções personalizadas** (`CalculatorError`).
- **Dicionários** (`REPLACEMENTS`) e laço `for` em `.items()`.
- **Funções "privadas"**: o `_` no início de `_evaluate` indica que a função é de uso interno do módulo. É uma convenção; o Python não bloqueia o acesso.
- **Operadores aritméticos**: `+ - * / // % **`.

## 8. Variáveis e constantes

| Constante | Valor | Por quê |
|---|---|---|
| `MAX_EXPRESSION_LENGTH` | `100` | Expressões gigantes não fazem sentido em um chat. |
| `MAX_EXPONENT` | `100` | `2 ** 99999999` travaria o bot. |
| `MAX_ABSOLUTE_RESULT` | `10**100` | Limita o tamanho do resultado. |
| `REPLACEMENTS` | `{"×": "*", "÷": "/", "^": "**", ",": "."}` | Aceita símbolos que as pessoas costumam digitar. |

## 9. Funções

| Função | O que faz |
|---|---|
| `calculate(expression)` | Limpa, valida, analisa e calcula. É a única função pública. |
| `_evaluate(node)` | Calcula um nó da árvore (recursiva). |
| `_apply_operator(operator, left, right)` | Aplica `+`, `-`, `*`... a dois números. |
| `_check_size(value)` | Rejeita números complexos ou grandes demais. |
| `format_result(value)` | Transforma `4.0` em `"4"` e `0.30000000000000004` em `"0.3"`. |

## 10. Parâmetros

- `expression`: o texto digitado.
- `node`: um nó da árvore (`ast.Constant`, `ast.BinOp`...).
- `operator`: um objeto como `ast.Add()` ou `ast.Mult()`.
- `left` / `right`: os números à esquerda e à direita do operador.

## 11. Métodos utilizados

| Método | Explicação |
|---|---|
| `ast.parse(texto, mode="eval")` | Analisa o texto como **uma expressão** (não como um programa inteiro). Lança `SyntaxError` se o texto não for Python válido. |
| `tree.body` | O nó principal da expressão. |
| `str.replace(a, b)` | Troca todas as ocorrências de `a` por `b`. |
| `round(valor, 10)` | Arredonda para 10 casas decimais. |
| `float.is_integer()` | `True` se o float não tem parte decimal (`4.0`). |

## 12. Funcionamento do código

### A árvore de sintaxe

Para o Python, `2 + 3 * 4` vira esta árvore:

```
        BinOp(+)
       /        \
 Constant(2)   BinOp(*)
              /        \
        Constant(3)   Constant(4)
```

Você pode ver isso no terminal:

```python
import ast
print(ast.dump(ast.parse("2 + 3 * 4", mode="eval"), indent=2))
```

### Avaliando nó por nó

```python
def _evaluate(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise CalculatorError("Apenas números são permitidos.")
        return _check_size(node.value)

    if isinstance(node, ast.UnaryOp):   # -5, +7
        ...

    if isinstance(node, ast.BinOp):     # a + b, a * b...
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        return _check_size(_apply_operator(node.op, left, right))

    raise CalculatorError("Esse tipo de expressão não é permitido. ...")
```

Esse é o coração da segurança: funcionamos como uma **lista de permissões** (*allowlist*). Só três tipos de nó são aceitos. Uma chamada de função (`ast.Call`), um nome de variável (`ast.Name`) ou um acesso a atributo (`ast.Attribute`) caem no `raise` do final. Por isso `__import__('os')` é recusado.

O `bool` é excluído porque, em Python, `True` é um tipo de `int` (`True + True == 2`).

### Divisão por zero e limites

```python
if isinstance(operator, (ast.Div, ast.FloorDiv, ast.Mod)) and right == 0:
    raise CalculatorError("Não é possível dividir por zero.")
```

Verificamos antes de calcular para mostrar uma mensagem amigável, em vez de um `ZeroDivisionError`.

## 13. Fluxo de execução

```
calculate("2 ^ 3 + 1")
 ├─ troca "^" por "**"           → "2 ** 3 + 1"
 ├─ valida tamanho
 ├─ ast.parse(...)               → BinOp(BinOp(2 ** 3) + 1)
 └─ _evaluate(BinOp +)
     ├─ _evaluate(BinOp **) → _evaluate(2)=2, _evaluate(3)=3 → 8
     ├─ _evaluate(1) → 1
     └─ 8 + 1 = 9
```

## 14. Exemplos práticos

```python
from bot.utils.calculator import calculate, format_result, CalculatorError

print(calculate("(10 + 5) / 2"))       # 7.5
print(format_result(calculate("0.1 + 0.2")))  # 0.3

try:
    calculate("open('senha.txt')")
except CalculatorError as erro:
    print("Bloqueado:", erro)
```

## 15. Erros comuns

- **"Por que `0.1 + 0.2` dá `0.30000000000000004`?"** Computadores guardam números decimais em binário, e alguns valores não têm representação exata. Por isso existe o `format_result`, que arredonda o resultado para exibição.
- **Vírgula como separador de milhar:** `1,000` vira `1.000` (um), porque a vírgula é tratada como separador decimal, como no Brasil.
- **`2(3)`** gera erro, porque Python não entende multiplicação implícita. Use `2*(3)`.

## 16. Como testar

```bash
python -m pytest tests/test_calculator.py -v
```

Os testes incluem tentativas de ataque (`__import__`, `open`, `lambda`) para garantir que continuam bloqueadas.

## 17. Como modificar

Para aceitar a função `sqrt` (raiz quadrada), seria preciso permitir `ast.Call` **apenas** quando o nome da função for `"sqrt"`. Faça isso com cuidado: cada novo tipo de nó aceito é um ponto que precisa ser verificado.

## 18. Desafio

Adicione suporte a **porcentagem**: `50%` deveria valer `0.5`. Dica: antes do `ast.parse`, use o módulo `re` para trocar `número%` por `(número/100)`. Atenção para não confundir com o operador de resto `10 % 3`. Escreva testes para os dois casos.
