"""Aula 06: funções, parâmetros, argumentos e retorno."""


def saudar(nome: str, saudacao: str = "Olá") -> str:
    """Parâmetro com valor padrão."""
    return f"{saudacao}, {nome}!"


def calcular_media(*notas: float) -> float:
    """Quantidade variável de argumentos (vira uma tupla)."""
    if not notas:
        return 0.0
    return sum(notas) / len(notas)


def criar_aluno(nome: str, *, ativo: bool = True) -> dict:
    """Tudo depois de * precisa ser passado pelo nome."""
    return {"nome": nome, "ativo": ativo}


def dividir(a: float, b: float) -> float | None:
    """Retorna None quando não é possível calcular (cláusula de guarda)."""
    if b == 0:
        return None
    return a / b


print(saudar("Ana"))
print(saudar("Bruno", "Bom dia"))
print(saudar(saudacao="Oi", nome="Carla"))  # argumentos nomeados
print("Média:", calcular_media(8, 7, 9.5))
print("Média vazia:", calcular_media())
print(criar_aluno("Diego", ativo=False))
print("10 / 4 =", dividir(10, 4))
print("10 / 0 =", dividir(10, 0))

resultado = print("print não tem return...")
print("...então devolve:", resultado)
