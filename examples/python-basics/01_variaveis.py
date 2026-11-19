"""Aula 01: sintaxe e variáveis.

Execute: python examples/python-basics/01_variaveis.py
"""

# Comentários começam com # e são ignorados pelo Python.

# Variáveis: um nome que guarda um valor.
nome = "Ana"
idade = 20
cidade = "Fortaleza"

# Constante (por convenção, em MAIÚSCULAS).
ANO_ATUAL = 2026

print("Nome:", nome)
print(f"{nome} tem {idade} anos e mora em {cidade}.")
print(f"{nome} nasceu por volta de {ANO_ATUAL - idade}.")

# O valor de uma variável pode mudar.
idade = idade + 1
print(f"No ano que vem, {nome} terá {idade} anos.")

# Para praticar entrada de dados, descomente as duas linhas abaixo:
# nome = input("Qual é o seu nome? ")
# print(f"Prazer, {nome}!")
