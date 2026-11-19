"""Aula 13: programação assíncrona com asyncio.

Repare no tempo total: as três tarefas rodam "juntas" e o programa termina em
cerca de 1,5 segundo (a mais longa), e não em 3 segundos (a soma).
"""

import asyncio
import time


async def preparar(item: str, segundos: float) -> str:
    print(f"Começando: {item}")
    await asyncio.sleep(segundos)  # pausa ESTA tarefa sem travar as outras
    print(f"Pronto: {item}")
    return item


async def main() -> None:
    inicio = time.perf_counter()
    resultados = await asyncio.gather(
        preparar("café", 1.5),
        preparar("pão", 1.0),
        preparar("suco", 0.5),
    )
    duracao = time.perf_counter() - inicio
    print(f"Resultados: {resultados}")
    print(f"Tempo total: {duracao:.1f} s")


if __name__ == "__main__":
    asyncio.run(main())
