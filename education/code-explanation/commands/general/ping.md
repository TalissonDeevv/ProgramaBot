# `bot/commands/general/ping.py`: o comando /ping

## 1. Nome e localização

- **Arquivo:** `bot/commands/general/ping.py`
- **Comando:** `/ping`

## 2. Finalidade

Responder "Pong!" com a **latência** do bot, o tempo de ida e volta entre o bot e o Discord, em milissegundos.

## 3. Por que foi criado

É o "Olá, mundo" dos bots: o comando mais simples possível. Ele serve para confirmar que o bot está online e para estudar a **estrutura básica** que todos os outros comandos repetem:

```
imports → (funções auxiliares) → class Cog → @app_commands.command → async def → setup()
```

## 4. Como se conecta ao restante do bot

- É encontrado e carregado automaticamente por `discover_extensions` em [`main.py`](../../main.md).
- Usa `info_embed` de [`utils/embeds.py`](../../utils/embeds.md).
- Tem um "irmão" de prefixo, `!ping`, em [`prefix_examples.py`](prefix_examples.md).

## 5. Bibliotecas utilizadas

- [`discord.py`](../../../libraries/discord-py.md): `discord`, `app_commands` e `commands`.

## 6. Importações

```python
import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import info_embed
```

- `discord`: o pacote principal (`discord.Interaction`, `discord.Embed`...).
- `app_commands`: tudo sobre slash commands (*application commands*).
- `commands`: o framework de comandos, que contém `commands.Cog` e `commands.Bot`.

## 7. Conceitos de Python utilizados

- **Funções** com parâmetro e retorno (`latency_status`).
- **Condicionais** encadeadas com `return` antecipado.
- **Classes** e o método `__init__`.
- **Decorators** (`@app_commands.command`).
- **Funções assíncronas** (`async def`, `await`).
- **f-strings** para montar o texto.
- **Arredondamento** com `round()`.

## 8. Variáveis

- `latency_ms`: a latência em milissegundos (`int`).
- `embed`: o embed da resposta.
- `self.bot`: referência ao bot, guardada no `__init__`.

## 9. Funções

- **`latency_status(latency_ms) -> str`**: classifica a latência (abaixo de 100 é "Excelente", abaixo de 250 é "Boa" e o resto é "Alta"). Fica **fora** da classe para poder ser testada sozinha.
- **`Ping.ping(interaction)`**: o comando em si.
- **`setup(bot)`**: registra o Cog. Toda extensão precisa ter essa função.

## 10. Parâmetros

- `latency_ms: int`: número de milissegundos.
- `interaction: discord.Interaction`: representa "alguém usou o comando". Contém quem usou (`interaction.user`), onde (`interaction.channel`, `interaction.guild`) e o objeto para responder (`interaction.response`).
- `bot: commands.Bot`: o bot que está carregando a extensão.

## 11. Métodos utilizados

| Método/atributo | Explicação |
|---|---|
| `@app_commands.command(name=, description=)` | Transforma o método em slash command. O nome deve ter letras minúsculas, sem espaços, até 32 caracteres; a descrição, até 100 caracteres. |
| `self.bot.latency` | Latência do *heartbeat* com o gateway, em **segundos** (`float`). |
| `interaction.response.send_message(embed=)` | Responde ao comando. Precisa acontecer em até **3 segundos**. |
| `bot.add_cog(cog)` | Adiciona o Cog e todos os comandos dele ao bot. |

## 12. Funcionamento do código

```python
class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
```

Um **Cog** é uma classe que agrupa comandos e eventos. Guardamos o bot em `self.bot` para usá-lo depois (aqui, para ler a latência).

```python
    @app_commands.command(name="ping", description="Mostra a latência (tempo de resposta) do bot.")
    async def ping(self, interaction: discord.Interaction) -> None:
        latency_ms = round(self.bot.latency * 1000)
```

`0.0874` segundo × 1000 = `87.4` milissegundos; `round` arredonda para `87`.

```python
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ping(bot))
```

Quando o `main.py` chama `load_extension("bot.commands.general.ping")`, o discord.py importa o arquivo e executa esta função.

## 13. Fluxo de execução

```
Usuário digita /ping
  → Discord envia uma interação ao bot
  → discord.py encontra o comando "ping" na árvore (bot.tree)
  → chama Ping.ping(interaction)
      → calcula a latência
      → latency_status(87) → "🟢 Excelente"
      → send_message(embed)
  → o usuário vê "🏓 Pong! Latência: 87 ms"
```

## 14. Exemplos práticos

Teste a função auxiliar no terminal:

```bash
python -c "from bot.commands.general.ping import latency_status; print(latency_status(42), latency_status(300))"
```

## 15. Erros comuns

- **O comando não aparece no Discord**: configure o `GUILD_ID` para sincronização instantânea, ou espere alguns minutos pela sincronização global. Reiniciar o aplicativo do Discord (`Ctrl+R`) também ajuda.
- **"O aplicativo não respondeu"**: o comando demorou mais de 3 segundos para responder ou deu erro. Olhe o terminal do bot.
- **Esquecer o `await`**: `interaction.response.send_message(...)` sem `await` não envia nada e gera o aviso `coroutine was never awaited`.

## 16. Como testar

- Automatizado: `python -m pytest tests/test_command_helpers.py -k latency`
- No Discord: use `/ping`.

## 17. Como modificar

- Mude os limites de `latency_status` ou os emojis.
- Adicione um campo ao embed: `embed.add_field(name="Servidores", value=str(len(self.bot.guilds)))`.

## 18. Desafio

Faça o `/ping` medir também o **tempo de resposta da API**: guarde `time.perf_counter()` antes do `send_message`, calcule a diferença depois e edite a resposta com `await interaction.edit_original_response(embed=...)` mostrando os dois valores. Resolva o [exercício 8](../../../exercises/02-basico.md#exercício-8--modificar-o-comando-ping) para um passo a passo.
