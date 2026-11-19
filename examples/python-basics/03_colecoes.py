"""Aulas 03 e 11: listas, tuplas, dicionários, sets e compreensões."""

# Lista: ordenada e modificável
alunos = ["Ana", "Bruno", "Carla"]
alunos.append("Diego")
print("Alunos:", alunos)
print("Primeiro:", alunos[0], "| Último:", alunos[-1])
print("Do segundo em diante:", alunos[1:])

# Tupla: ordenada e imutável
DIAS_UTEIS = ("seg", "ter", "qua", "qui", "sex")
print("Dias úteis:", len(DIAS_UTEIS))

# Dicionário: chave -> valor
notas = {"Ana": 9.0, "Bruno": 6.5, "Carla": 8.0}
notas["Diego"] = 7.5
for nome, nota in notas.items():
    situacao = "aprovado" if nota >= 7 else "recuperação"
    print(f"{nome}: {nota} ({situacao})")
print("Nota de quem não existe:", notas.get("Zeca"))

# Set: sem repetição
linguagens = {"python", "java", "python"}
print("Linguagens únicas:", sorted(linguagens))

# --- Aula 11: iteradores e compreensões ---
quadrados = [numero**2 for numero in range(1, 6)]
print("Quadrados:", quadrados)

aprovados = [nome for nome, nota in notas.items() if nota >= 7]
print("Aprovados:", aprovados)

for posicao, nome in enumerate(alunos, start=1):
    print(f"{posicao}º {nome}")

idades = [17, 19, 21, 18]
for nome, idade in zip(alunos, idades):
    print(f"{nome} tem {idade} anos")

print("Alguém menor de idade?", any(idade < 18 for idade in idades))
print("Média das notas:", round(sum(notas.values()) / len(notas), 2))
