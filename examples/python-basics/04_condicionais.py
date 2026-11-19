"""Aula 04: condicionais (o mesmo raciocínio do /hello do ProgramaBot)."""


def saudacao(hora: int) -> str:
    if not 0 <= hora <= 23:
        return "Hora inválida"
    if 5 <= hora < 12:
        return "Bom dia"
    if 12 <= hora < 18:
        return "Boa tarde"
    return "Boa noite"


for hora in (3, 8, 13, 20, 25):
    print(f"{hora:>2}h -> {saudacao(hora)}")

idade = 16
tem_autorizacao = True
if idade >= 18 or tem_autorizacao:
    print("Pode participar do evento.")
else:
    print("Não pode participar.")

opcoes = []
if not opcoes:
    print("A lista de opções está vazia.")

resposta = "SIM".lower()
if resposta in ("sim", "s", "yes"):
    print("Resposta positiva!")

quantidade = 1
palavra = "voto" if quantidade == 1 else "votos"
print(f"{quantidade} {palavra}")
