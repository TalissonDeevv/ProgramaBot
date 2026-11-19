"""Aula 05: repetições com for e while."""

print("Tabuada do 7:")
for multiplicador in range(1, 11):
    print(f"7 x {multiplicador:>2} = {7 * multiplicador}")

print("\nNúmeros pares de 2 a 10:")
for numero in range(2, 11, 2):
    print(numero, end=" ")
print()

print("\nContagem regressiva:")
contador = 5
while contador > 0:
    print(contador)
    contador -= 1
print("Lançar! 🚀")

print("\nbreak e continue:")
for numero in range(10):
    if numero == 3:
        continue  # pula o 3
    if numero == 7:
        break  # para no 7
    print(numero, end=" ")
print()

total = 0
for numero in range(1, 101):
    total += numero
print("\nSoma de 1 a 100:", total)

vogais = 0
for letra in "programabot":
    if letra in "aeiou":
        vogais += 1
print("Vogais em 'programabot':", vogais)
