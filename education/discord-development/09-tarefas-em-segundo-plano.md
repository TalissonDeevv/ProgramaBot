# 09. Tarefas em segundo plano (`tasks.loop`)

## Para que servem?

Algumas ações não dependem de alguém usar um comando: verificar lembretes, trocar o status do bot de tempos em tempos, publicar uma mensagem diária. Para isso existe a extensão `discord.ext.tasks`.

## Como usar

```python
from discord.ext import commands, tasks


class Relogio(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def cog_load(self) -> None:
        self.tic.start()            # liga a tarefa

    async def cog_unload(self) -> None:
        self.tic.cancel()           # desliga a tarefa

    @tasks.loop(minutes=5)
    async def tic(self) -> None:
        print("Mais 5 minutos se passaram")

    @tic.before_loop
    async def antes(self) -> None:
        await self.bot.wait_until_ready()   # espera o bot conectar
```

Outras opções do decorator: `seconds=`, `hours=`, `time=` (horários fixos do dia) e `count=` (número de repetições).

## Cuidados

1. **Sempre cancele no `cog_unload`.** Sem isso, recarregar a extensão cria tarefas duplicadas.
2. **Use `before_loop` com `wait_until_ready()`** se a tarefa usa canais, membros ou o cache.
3. **Exceções param a tarefa.** Se um erro escapar, o loop para para sempre. Trate os erros dentro do loop.
4. **Não bloqueie.** Dentro da tarefa valem as mesmas regras dos comandos: nada de `time.sleep`.

## No ProgramaBot

O [`/remind`](../code-explanation/commands/utility/remind.md) usa uma tarefa que roda a cada 30 segundos:

```python
@tasks.loop(seconds=CHECK_INTERVAL_SECONDS)
async def check_reminders(self) -> None:
    for reminder in self.repository.get_due():
        try:
            await self._deliver(reminder)
        except Exception:
            logger.exception("Erro ao entregar o lembrete #%s", reminder.id)
        finally:
            self.repository.delete(reminder.id)
```

## Exercício

Crie um Cog que troque o status do bot a cada minuto entre três frases ("/help", "aprendendo Python", "em N servidores"). Dica: guarde um índice em `self` e use `await self.bot.change_presence(activity=discord.Game(name=...))`.

Documentação: <https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html>
