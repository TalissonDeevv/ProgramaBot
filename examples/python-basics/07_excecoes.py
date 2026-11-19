"""Aula 08: exceções (try, except, else, finally e raise)."""


class SaldoInsuficiente(Exception):
    """Exceção personalizada, como ConfigError e CalculatorError no ProgramaBot."""


def sacar(saldo: float, valor: float) -> float:
    if valor <= 0:
        raise ValueError("O valor do saque deve ser positivo.")
    if valor > saldo:
        raise SaldoInsuficiente(f"Saldo de R$ {saldo:.2f} é menor que R$ {valor:.2f}.")
    return saldo - valor


def converter(texto: str) -> int | None:
    try:
        numero = int(texto)
    except ValueError:
        print(f"  '{texto}' não é um número inteiro.")
        return None
    else:
        print(f"  '{texto}' convertido com sucesso.")
        return numero
    finally:
        print("  (finally sempre executa)")


for entrada in ("42", "abc"):
    print(f"Convertendo {entrada!r}:")
    converter(entrada)

for valor in (30, 500, -1):
    try:
        novo_saldo = sacar(100, valor)
        print(f"Saque de {valor}: novo saldo {novo_saldo}")
    except SaldoInsuficiente as erro:  # a mais específica primeiro
        print("Saldo insuficiente:", erro)
    except ValueError as erro:
        print("Valor inválido:", erro)

try:
    10 / 0
except ZeroDivisionError as erro:
    print("Erro capturado:", type(erro).__name__, "-", erro)
