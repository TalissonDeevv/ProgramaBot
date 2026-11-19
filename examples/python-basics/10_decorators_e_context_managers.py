"""Aulas 10 e 12: decorators e context managers."""

import functools
import tempfile
import time
from pathlib import Path


# ---------- Decorators ----------
def cronometrar(funcao):
    """Decorator que mede quanto tempo a função levou."""

    @functools.wraps(funcao)
    def nova_funcao(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = funcao(*args, **kwargs)
        print(f"{funcao.__name__} levou {time.perf_counter() - inicio:.4f} s")
        return resultado

    return nova_funcao


def repetir(vezes: int):
    """Fábrica de decorators: recebe um argumento e devolve um decorator."""

    def decorator(funcao):
        @functools.wraps(funcao)
        def nova_funcao(*args, **kwargs):
            for _ in range(vezes):
                funcao(*args, **kwargs)

        return nova_funcao

    return decorator


@cronometrar
def somar_ate(limite: int) -> int:
    return sum(range(limite))


@repetir(3)
def acenar(nome: str) -> None:
    print(f"👋 {nome}")


print("Soma:", somar_ate(1_000_000))
acenar("ProgramaBot")


# ---------- Context managers ----------
class Mensagem:
    def __enter__(self):
        print("Início do bloco")
        return self

    def __exit__(self, tipo_erro, erro, traceback):
        print("Fim do bloco (sempre executa)")
        return False  # não esconde erros


with Mensagem():
    print("Dentro do bloco")

with tempfile.TemporaryDirectory() as pasta:
    arquivo = Path(pasta) / "diario.txt"
    with arquivo.open("w", encoding="utf-8") as f:
        f.write("Hoje estudei decorators.\n")
        f.write("Também estudei context managers.\n")
    with arquivo.open(encoding="utf-8") as f:
        for linha in f:
            print("Lido:", linha.strip())
print("A pasta temporária já foi apagada pelo context manager.")
