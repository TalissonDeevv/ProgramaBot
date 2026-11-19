# `bot/commands/general/prefix_examples.py`: comandos de prefixo

## 1. Nome e localização

- **Arquivo:** `bot/commands/general/prefix_examples.py`
- **Comandos:** `!ping`, `!hello` (aliases `!ola` e `!oi`), `!soma <a> <b>`
- O prefixo vem de `BOT_PREFIX` no `.env` (padrão `!`). Mencionar o bot também funciona: `@ProgramaBot ping`.

## 2. Finalidade

Mostrar, **lado a lado com os slash commands**, como funcionam os comandos de prefixo: o modelo antigo, em que o bot lê o texto das mensagens.

## 3. Por que foi criado

Muitos tutoriais e bots antigos usam esse modelo, então é importante reconhecê-lo. Comparando com [`ping.py`](ping.md) e [`hello.py`](hello.md), você percebe as diferenças:

| | Slash command (`/ping`) | Prefixo (`!ping`) |
|---|---|---|
| Decorator | `@app_commands.command` | `@commands.command` |
| Primeiro parâmetro | `interaction: discord.Interaction` | `ctx: commands.Context` |
| Responder | `interaction.response.send_message` | `ctx.send` |
| Intent necessária | nenhuma | **MESSAGE CONTENT** (privilegiada) |
| Autocompletar no Discord | sim | não |
| Validação de tipos | feita pelo Discord | feita pelo bot (*converters*) |
| Respostas ephemeral | sim | não |
| Registro (sync) | necessário | não |

Explicação completa em [Slash commands vs. prefixo](../../../discord-development/03-slash-vs-prefixo.md).

## 4. Como se conecta ao restante do bot

- O prefixo é configurado em [`main.py`](../../main.md) com `commands.when_mentioned_or(settings.prefix)`.
- `format_result` vem de [`utils/calculator.py`](../../utils/calculator.md).
- Erros sem tratador próprio vão para `on_command_error` em [`events/errors.py`](../../events/errors.md).

## 5. Bibliotecas utilizadas

- [`discord.py`](../../../libraries/discord-py.md): `discord.ext.commands`.

## 6. Importações

```python
from discord.ext import commands

from bot.utils.calculator import format_result
```

Repare que não importamos `app_commands`: ele não é necessário para comandos de prefixo.

## 7. Conceitos de Python utilizados

- **Parâmetro somente-palavra-chave** (`*`): em `async def hello_prefix(self, ctx, *, nome=None)`, o `*` faz o discord.py juntar **todo o resto da mensagem** em `nome`.
- **Type hints que viram conversões**: `a: float` faz o discord.py converter `"2.5"` em `2.5`.
- **Decorators que criam outros decorators**: `@soma.error`.
- **Relançar exceções** (`raise error`).

## 8. Variáveis

- `latency_ms`, `name`: iguais às dos slash commands.

## 9. Funções

| Método | Comando |
|---|---|
| `ping_prefix(ctx)` | `!ping` |
| `hello_prefix(ctx, *, nome=None)` | `!hello`, `!ola`, `!oi` |
| `soma(ctx, a, b)` | `!soma 2 3` |
| `soma_error(ctx, error)` | tratador de erros exclusivo do `!soma` |

O nome Python do método (`ping_prefix`) é diferente do nome do comando (`name="ping"`), porque já existe um método `ping` no Cog do `/ping`. Os Cogs são separados, então não haveria conflito, mas nomes distintos deixam o código mais claro.

## 10. Parâmetros

- `ctx: commands.Context`: o **contexto** da mensagem: autor (`ctx.author`), canal (`ctx.channel`), servidor (`ctx.guild`), a mensagem (`ctx.message`) e o comando (`ctx.command`).
- `a: float, b: float`: os dois números, já convertidos.
- `error: commands.CommandError`: o erro que aconteceu.

## 11. Métodos utilizados

| Método | Explicação |
|---|---|
| `@commands.command(name=, aliases=)` | Cria um comando de prefixo, com nomes alternativos. |
| `ctx.send(texto)` | Envia uma mensagem no canal. |
| `ctx.author.display_name` | Nome de quem enviou. |
| `@soma.error` | Registra uma função que trata erros **só** desse comando. |
| `commands.MissingRequiredArgument` | Faltou um argumento (`!soma 2`). |
| `commands.BadArgument` | A conversão falhou (`!soma a b`). |

## 12. Funcionamento do código

### Como o discord.py reconhece um comando de prefixo

1. Chega uma mensagem: `!soma 2 3`.
2. O `commands.Bot` verifica se ela começa com o prefixo.
3. Separa o nome (`soma`) e os argumentos (`"2"`, `"3"`).
4. Converte cada argumento segundo a *type hint* (`float`).
5. Chama `soma(ctx, 2.0, 3.0)`.

Sem a intent MESSAGE CONTENT, o texto das mensagens chega vazio (exceto quando o bot é mencionado), e o passo 2 nunca encontra o prefixo.

### Tratamento de erro local

```python
@soma.error
async def soma_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Faltou um número. Uso correto: `!soma 2 3`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Use apenas números. Exemplo: `!soma 2.5 4`")
    else:
        raise error
```

Erros que não sabemos tratar são **relançados**, para não serem engolidos em silêncio. O tratador global em `errors.py` verifica `ctx.command.has_error_handler()` e não responde de novo.

## 13. Fluxo de execução

```
mensagem "!soma 2 x"
 → on_message do commands.Bot → process_commands
 → converter "x" para float falha → BadArgument
 → soma_error → "Use apenas números..."
```

## 14. Exemplos práticos

No Discord: `!ping`, `!oi`, `!hello Maria Silva`, `!soma 10 5.5`, `!soma 1`, `!soma a b`.

## 15. Erros comuns

- **Nada acontece com `!ping`**: verifique se MESSAGE CONTENT INTENT está ativada no Developer Portal **e** `ENABLE_MESSAGE_CONTENT_INTENT=true` no `.env`.
- **Funciona só quando menciono o bot**: é o mesmo problema. Quando o bot é mencionado, o Discord envia o texto mesmo sem a intent.

## 16. Como testar

```bash
python -m pytest tests/test_extensions.py -k expected_commands -v
```

O teste confere se `ping`, `hello` e `soma` foram registrados como comandos de prefixo.

## 17. Como modificar

Crie `!dobro <número>`:

```python
@commands.command(name="dobro")
async def dobro(self, ctx: commands.Context, numero: int) -> None:
    await ctx.send(f"O dobro de {numero} é {numero * 2}")
```

Depois, atualize `EXPECTED_PREFIX_COMMANDS` em `tests/test_extensions.py` e `PREFIX_EXAMPLES` em `views/help_menu.py`.

## 18. Desafio

Crie `!media <números...>`, que calcula a média de quantos números a pessoa digitar. Dica: `*numeros: float` recebe uma quantidade variável de argumentos como tupla. Trate o caso em que nenhum número é enviado.
