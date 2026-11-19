# asyncio

## O que é?

O módulo da biblioteca padrão que implementa a **programação assíncrona** em Python: o sistema por trás de `async def` e `await`.

## Para que serve? Que problema resolve?

Um bot passa a maior parte do tempo **esperando**: a próxima mensagem, a resposta da API, o fim de um `sleep`. Em um programa comum (síncrono), enquanto ele espera uma coisa, não faz nenhuma outra. O `asyncio` permite que, durante uma espera, o programa adiante outras tarefas. Assim, um único bot atende centenas de pessoas ao mesmo tempo.

## Como funciona?

O coração do asyncio é o **event loop** (laço de eventos), uma espécie de gerente que alterna entre tarefas:

```
event loop
 ├─ tarefa A: /poll  → await asyncio.sleep(600)   ⏸ (esperando)
 ├─ tarefa B: /ping  → executa → responde → fim  ▶
 ├─ tarefa C: clique em botão → executa          ▶
 └─ volta para A quando os 600 s passarem
```

Cada `await` é um ponto em que a tarefa diz: "vou esperar; enquanto isso, pode cuidar de outra coisa".

- `async def` cria uma **corrotina** (*coroutine*), uma função que pode ser pausada.
- `await` pausa a corrotina até o resultado ficar pronto.

## Nativa ou externa?

**Nativa.** Não precisa instalar.

## Como importar

```python
import asyncio
```

## Funções utilizadas no ProgramaBot

| Função | Onde | Explicação |
|---|---|---|
| `asyncio.run(corrotina)` | `main.py` | Cria o event loop, executa a corrotina até o fim e fecha o loop. É o "botão de ligar" de um programa assíncrono. |
| `asyncio.sleep(segundos)` | `commands/utility/poll.py` | Espera **sem travar** o resto do programa. |

O discord.py usa o asyncio internamente o tempo todo (`async with bot`, `await bot.start(...)`, `tasks.loop`).

## `asyncio.sleep` vs. `time.sleep`

```python
import time
time.sleep(10)          # ❌ trava o bot INTEIRO por 10 segundos

import asyncio
await asyncio.sleep(10) # ✅ pausa só esta tarefa
```

Essa é a regra mais importante ao escrever bots com discord.py: **nunca use funções bloqueantes demoradas** (`time.sleep`, `requests.get`, leituras de arquivos enormes) dentro de comandos.

## Exemplo independente do ProgramaBot

```python
import asyncio


async def preparar(nome: str, segundos: int) -> str:
    print(f"Começando {nome}...")
    await asyncio.sleep(segundos)
    print(f"{nome} pronto!")
    return nome


async def main() -> None:
    # As três "tarefas" rodam ao mesmo tempo: o total leva ~3 s, e não 6 s.
    resultados = await asyncio.gather(
        preparar("café", 3),
        preparar("pão", 2),
        preparar("suco", 1),
    )
    print(resultados)


asyncio.run(main())
```

Versão comentada: [`examples/python-basics/09_async_basico.py`](../../examples/python-basics/09_async_basico.py).

## Documentação oficial

- <https://docs.python.org/pt-br/3/library/asyncio.html>

Aula completa: [Programação assíncrona](../python/13-programacao-assincrona.md).
