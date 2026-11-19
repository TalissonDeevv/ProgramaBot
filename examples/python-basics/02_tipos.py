"""Aula 02: tipos de dados (str, int, float, bool e None)."""

texto = "  ProgramaBot  "
inteiro = 42
decimal = 3.75
verdadeiro = True
nada = None

for valor in (texto, inteiro, decimal, verdadeiro, nada):
    print(repr(valor), "é do tipo", type(valor).__name__)

# Métodos de string
print(texto.strip())
print(texto.strip().upper())
print(texto.strip().lower())
print("Tamanho sem espaços:", len(texto.strip()))
print("Primeira letra:", texto.strip()[0])
print("Separando:", "python,discord,git".split(","))

# Números
print("10 / 3 =", 10 / 3)
print("10 // 3 =", 10 // 3)
print("10 % 3 =", 10 % 3)
print("2 ** 8 =", 2**8)
print("Arredondado:", round(10 / 3, 2))
print(f"Formatado: {decimal:.1f}")

# Conversões
print(int("10") + 5)
print(float("2.5") * 2)
print("Idade: " + str(inteiro))
print("bool(0) =", bool(0), "| bool('texto') =", bool("texto"))

try:
    int("abc")
except ValueError as erro:
    print("Erro esperado ao converter 'abc':", erro)
