# 13. Programação assíncrona: `async` e `await`

## Explicação

### O problema

Imagine um garçom que anota o pedido de uma mesa, vai até a cozinha e **fica parado esperando** o prato ficar pronto antes de atender a próxima mesa. Esse é o código **síncrono**: cada tarefa bloqueia todas as outras enquanto espera.

Um bom garçom anota o pedido, entrega na cozinha e, **enquanto espera**, atende outras mesas. Esse é o código **assíncrono**.

Um bot do Discord passa a maior parte do tempo esperando (mensagens, respostas da API, temporizadores), por isso o discord.py é todo assíncrono.

### As peças

| Conceito | O que é |
|---|---|
| `async def` | Define uma **corrotina**: uma função que pode ser pausada e retomada. |
| `await` | "Espere este resultado; enquanto isso, o event loop pode fazer outra coisa." Só pode ser usado dentro de `async def`. |
| **event loop** | O "garçom": alterna entre as corrotinas que estão prontas para continuar. |
| `asyncio.run(main())` | Liga o event loop e executa a corrotina principal. |

```python
import asyncio


async def tarefa(nome: str, segundos: float) -> None:
    print(f"{nome}: começou")
    await asyncio.sleep(segundos)      # pausa SEM travar
    print(f"{nome}: terminou")


async def main() -> None:
    await asyncio.gather(              # executa as três "ao mesmo tempo"
        tarefa("A", 2),
        tarefa("B", 1),
        tarefa("C", 1.5),
    )


asyncio.run(main())                    # leva ~2 s no total, e não 4,5 s
```

### Erros clássicos

```python
async def enviar(): ...

enviar()            # ❌ não executa! Cria uma corrotina e gera o aviso "coroutine ... was never awaited"
await enviar()      # ✅
```

```python
import time
time.sleep(5)       # ❌ dentro de um bot: congela TUDO por 5 s
await asyncio.sleep(5)  # ✅ pausa só esta corrotina
```

### Concorrência não é paralelismo

O asyncio roda em **uma** linha de execução: só uma corrotina executa por vez. O ganho vem de não ficar parado nas esperas. Por isso, um cálculo pesado (sem `await`) ainda trava o bot. Para trabalho pesado ou bloqueante, existe `await asyncio.to_thread(funcao, args)`.

## Exemplo simples

```python
import asyncio


async def ola():
    await asyncio.sleep(1)
    print("Olá depois de 1 segundo")


asyncio.run(ola())
```

## Código executável

[`examples/python-basics/09_async_basico.py`](../../examples/python-basics/09_async_basico.py)

## Aplicação no ProgramaBot

| Onde | O quê |
|---|---|
| [`main.py`](../code-explanation/main.md) | `asyncio.run(run_bot())`, `async with bot`, `await bot.start(token)` |
| todos os comandos | `async def comando(self, interaction)` e `await interaction.response.send_message(...)` |
| [`poll.py`](../code-explanation/commands/utility/poll.md) | `await asyncio.sleep(...)` por vários minutos, sem travar o bot |
| [`kick.py`](../code-explanation/commands/moderation/kick.md) | `await view.wait()`: o comando "pausa" esperando um clique |
| [`remind.py`](../code-explanation/commands/utility/remind.md) | `tasks.loop`: uma corrotina que o discord.py agenda a cada 30 s |

Quando 10 pessoas usam `/poll` ao mesmo tempo, existem 10 corrotinas "dormindo" no `asyncio.sleep`, e o bot continua respondendo `/ping` normalmente.

## Exercício

1. Escreva `contagem(nome, n)`, que conta de `n` até 1 com `await asyncio.sleep(1)` entre os números. Rode duas contagens ao mesmo tempo com `asyncio.gather`.
2. Troque `asyncio.sleep` por `time.sleep` no exercício 1. O que muda no tempo total? Por quê?
3. Em [`bot/commands/utility/poll.py`](../../bot/commands/utility/poll.py), explique o que aconteceria com o bot se a linha `await asyncio.sleep(...)` fosse `time.sleep(...)`.
