"""Calculadora segura usada pelo comando ``/calculator``.

Por que não usar ``eval()``? Porque ``eval`` executa QUALQUER código Python.
Um usuário mal-intencionado poderia digitar algo como
``__import__('os').remove('arquivo')`` e o bot executaria. Aqui fazemos
diferente: usamos o módulo ``ast`` para transformar o texto em uma "árvore"
e só calculamos os nós que representam números e operações matemáticas.
Qualquer outra coisa é recusada.
"""

import ast

MAX_EXPRESSION_LENGTH = 100
MAX_EXPONENT = 100
MAX_ABSOLUTE_RESULT = 10**100

# Símbolos que as pessoas costumam digitar e o equivalente em Python.
REPLACEMENTS = {"×": "*", "÷": "/", "^": "**", ",": "."}


class CalculatorError(Exception):
    """Erro com uma mensagem amigável para mostrar ao usuário."""


def calculate(expression: str) -> int | float:
    """Calcula uma expressão matemática simples, como ``2 + 3 * (4 - 1)``.

    Operadores aceitos: ``+ - * / // % **`` e parênteses.

    Raises:
        CalculatorError: se a expressão estiver vazia, for inválida ou perigosa.
    """
    cleaned = expression.strip()
    for symbol, python_symbol in REPLACEMENTS.items():
        cleaned = cleaned.replace(symbol, python_symbol)

    if not cleaned:
        raise CalculatorError("Digite uma expressão, por exemplo: 2 + 3 * 4")
    if len(cleaned) > MAX_EXPRESSION_LENGTH:
        raise CalculatorError(
            f"A expressão é longa demais (máximo de {MAX_EXPRESSION_LENGTH} caracteres)."
        )

    try:
        tree = ast.parse(cleaned, mode="eval")
    except SyntaxError:
        raise CalculatorError(
            "Expressão inválida. Use números, os operadores + - * / // % ** e parênteses."
        ) from None

    return _evaluate(tree.body)


def _evaluate(node: ast.AST) -> int | float:
    """Calcula um nó da árvore de forma recursiva (a função chama a si mesma)."""
    if isinstance(node, ast.Constant):
        # bool é um tipo de int em Python, então precisamos excluí-lo explicitamente.
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise CalculatorError("Apenas números são permitidos.")
        return _check_size(node.value)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        if isinstance(node.op, ast.UAdd):
            return operand
        if isinstance(node.op, ast.USub):
            return -operand
        raise CalculatorError("Operador não permitido.")

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        return _check_size(_apply_operator(node.op, left, right))

    raise CalculatorError(
        "Esse tipo de expressão não é permitido. Use apenas números e operadores matemáticos."
    )


def _apply_operator(operator: ast.operator, left: int | float, right: int | float) -> int | float:
    """Aplica um operador matemático a dois números."""
    if isinstance(operator, ast.Add):
        return left + right
    if isinstance(operator, ast.Sub):
        return left - right
    if isinstance(operator, ast.Mult):
        return left * right
    if isinstance(operator, (ast.Div, ast.FloorDiv, ast.Mod)) and right == 0:
        raise CalculatorError("Não é possível dividir por zero.")
    if isinstance(operator, ast.Div):
        return left / right
    if isinstance(operator, ast.FloorDiv):
        return left // right
    if isinstance(operator, ast.Mod):
        return left % right
    if isinstance(operator, ast.Pow):
        if abs(right) > MAX_EXPONENT:
            raise CalculatorError(f"O expoente máximo permitido é {MAX_EXPONENT}.")
        if left == 0 and right < 0:
            raise CalculatorError("Não é possível elevar zero a um expoente negativo.")
        try:
            return left**right
        except OverflowError:
            raise CalculatorError("O resultado é grande demais para ser calculado.") from None
    raise CalculatorError("Operador não permitido.")


def _check_size(value: int | float) -> int | float:
    """Impede números gigantes, que deixariam o bot lento."""
    if isinstance(value, complex):
        raise CalculatorError("O resultado não é um número real.")
    if abs(value) > MAX_ABSOLUTE_RESULT:
        raise CalculatorError("O resultado é grande demais para ser exibido.")
    return value


def format_result(value: int | float) -> str:
    """Formata o resultado: ``4.0`` vira ``4`` e ``0.1 + 0.2`` vira ``0.3``."""
    if isinstance(value, float):
        rounded = round(value, 10)
        if rounded.is_integer():
            return str(int(rounded))
        return str(rounded)
    return str(value)
