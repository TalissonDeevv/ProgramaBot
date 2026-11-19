# discord.py

## O que é?

O **discord.py** é uma biblioteca de código aberto para criar bots do Discord em Python. Ela "conversa" com o Discord por você: mantém a conexão aberta, recebe os eventos (mensagens, membros entrando, comandos usados) e transforma tudo em objetos Python fáceis de usar.

## Para que serve? Que problema resolve?

O Discord oferece duas formas de comunicação para bots:

- a **API REST** (requisições HTTP), para *fazer* coisas: enviar mensagens, banir, criar canais;
- o **Gateway** (uma conexão WebSocket permanente), para *receber* eventos em tempo real.

Usar essas interfaces diretamente exigiria lidar com autenticação, *heartbeats* (sinais periódicos de "estou vivo"), reconexões, limites de requisições (*rate limits*) e muito JSON. O discord.py cuida de tudo isso, e você escreve só a lógica do seu bot.

## Como funciona?

```
Discord ──(Gateway/WebSocket)──► discord.py ──► seus eventos e comandos
Discord ◄──(API REST/HTTP)────── discord.py ◄── await channel.send(...)
```

Ele é **assíncrono**: usa `async`/`await` e o `asyncio` para atender muitos eventos ao mesmo tempo sem travar. Veja [asyncio.md](asyncio.md).

## Nativa ou externa?

**Externa.** Precisa ser instalada.

## Como instalar

```bash
pip install -r requirements.txt
```

Isso instala a versão fixada no projeto (`discord.py==2.7.1`). Para instalar só ele:

```bash
pip install discord.py==2.7.1
```

> Instala-se como `discord.py`, mas importa-se como `discord`.

## Como importar

```python
import discord                      # classes principais: Embed, Intents, Member...
from discord import app_commands    # slash commands
from discord.ext import commands    # framework de comandos: Bot, Cog, comandos de prefixo
from discord.ext import tasks       # tarefas repetitivas em segundo plano
```

## O que o ProgramaBot usa

### `discord.ext.commands`

| Item | Onde | Explicação |
|---|---|---|
| `commands.Bot` | `main.py` | Classe do bot, com suporte a Cogs, extensões e comandos. |
| `commands.when_mentioned_or(prefixo)` | `main.py` | Aceita o prefixo ou uma menção. |
| `bot.load_extension(nome)` | `main.py` | Importa um módulo e chama a função `setup(bot)` dele. |
| `bot.add_cog(cog)` | todos os comandos | Registra um Cog. |
| `commands.Cog` | todos os comandos | Classe base para agrupar comandos e eventos. |
| `@commands.Cog.listener()` | `events/*.py` | Ouve um evento. |
| `@commands.command()` | `prefix_examples.py` | Cria um comando de prefixo. |
| `commands.Context` | `prefix_examples.py` | Contexto de um comando de prefixo (`ctx.send`, `ctx.author`). |
| `commands.CommandError` e subclasses | `errors.py` | Erros de comandos de prefixo. |

### `discord.app_commands`

| Item | Onde | Explicação |
|---|---|---|
| `@app_commands.command(name=, description=)` | todos os slash commands | Cria um slash command. |
| `@app_commands.describe(param=...)` | comandos com parâmetros | Descrição de cada parâmetro. |
| `app_commands.Range[tipo, min, max]` | vários | Limita valores ou tamanho do texto, validado pelo Discord. |
| `@app_commands.guild_only()` | vários | Só em servidores. |
| `@app_commands.default_permissions(...)` | moderação, `/say` | Quem vê o comando por padrão. |
| `@app_commands.checks.has_permissions(...)` | moderação, `/say` | Verifica a permissão de quem usa. |
| `@app_commands.checks.bot_has_permissions(...)` | moderação, `/say` | Verifica a permissão do bot. |
| `@app_commands.checks.cooldown(usos, segundos)` | `/embed` | Limita a frequência de uso. |
| `bot.tree` (`CommandTree`) | `main.py`, `errors.py` | A "árvore" com todos os slash commands. |
| `tree.sync()` / `tree.copy_global_to()` | `main.py` | Registra os comandos no Discord. |
| `tree.on_error` | `errors.py` | Tratador de erros dos slash commands. |

### `discord.Interaction`

Representa "alguém usou um comando, clicou em um botão ou enviou um modal".

| Item | Explicação |
|---|---|
| `interaction.user` | Quem interagiu. |
| `interaction.guild` / `.channel` / `.channel_id` | Onde. |
| `interaction.response.send_message(...)` | Primeira resposta (até 3 segundos). |
| `interaction.response.defer(...)` | "Estou pensando...", ganha até 15 minutos. |
| `interaction.response.edit_message(...)` | Responde a um clique editando a mensagem. |
| `interaction.response.send_modal(modal)` | Abre um formulário. |
| `interaction.response.is_done()` | Já respondeu? |
| `interaction.followup.send(...)` | Mensagens depois da primeira resposta. |
| `interaction.original_response()` | A mensagem da primeira resposta. |
| `interaction.edit_original_response(...)` | Edita a primeira resposta. |

### `discord.ui` (componentes)

| Item | Onde | Explicação |
|---|---|---|
| `discord.ui.View` | `views/*.py`, `about.py` | Contêiner de componentes. |
| `discord.ui.Button` / `@discord.ui.button` | `confirm.py`, `poll.py`, `about.py` | Botões (com callback ou de link). |
| `discord.ui.Select` / `discord.SelectOption` | `help_menu.py` | Menu de seleção. |
| `discord.ui.Modal` / `discord.ui.TextInput` | `embed_modal.py` | Formulário. |
| `view.wait()` / `view.stop()` | `confirm.py` | Esperar e encerrar a view. |
| `bot.add_view(view)` | `main.py` | Registrar uma view persistente. |

### `discord.ext.tasks`

| Item | Onde | Explicação |
|---|---|---|
| `@tasks.loop(seconds=30)` | `remind.py` | Executa uma função repetidamente. |
| `.start()` / `.cancel()` / `@loop.before_loop` | `remind.py` | Controle da tarefa. |

### Modelos (objetos do Discord)

`discord.Member`, `discord.User`, `discord.Guild`, `discord.TextChannel`, `discord.Thread`, `discord.Role`, `discord.Message`, `discord.Asset`, `discord.Object`, `discord.abc.Messageable`.

### Outros

| Item | Explicação |
|---|---|
| `discord.Intents` | Quais eventos receber. Veja [Intents](../discord-development/02-intents.md). |
| `discord.Embed` | Mensagens formatadas. |
| `discord.AllowedMentions` | Controla quem pode ser notificado. |
| `discord.utils.format_dt(dt, estilo)` | Datas no fuso de quem lê. |
| `discord.utils.utcnow()` | Horário atual em UTC. |
| `discord.Game(name=)` | Status "Jogando...". |
| `discord.LoginFailure`, `discord.PrivilegedIntentsRequired`, `discord.HTTPException`, `discord.Forbidden`, `discord.NotFound` | Exceções. |

## Exemplo independente do ProgramaBot

O menor bot possível com um slash command (sem Cogs):

```python
import discord
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="oi", description="Diz oi")
async def oi(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(f"Oi, {interaction.user.display_name}!")


@client.event
async def on_ready() -> None:
    await tree.sync()
    print(f"Online como {client.user}")


client.run("SEU_TOKEN_AQUI")  # ⚠️ só para teste local; nunca publique o token
```

Uma versão comentada está em [`examples/minimal-bot/bot_minimo.py`](../../examples/minimal-bot/bot_minimo.py).

## Documentação oficial

- Documentação: <https://discordpy.readthedocs.io/en/stable/>
- Guia de slash commands e interações: <https://discordpy.readthedocs.io/en/stable/interactions/api.html>
- Extensão de comandos: <https://discordpy.readthedocs.io/en/stable/ext/commands/index.html>
- Tarefas: <https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html>
- Código-fonte e exemplos: <https://github.com/Rapptz/discord.py/tree/master/examples>
