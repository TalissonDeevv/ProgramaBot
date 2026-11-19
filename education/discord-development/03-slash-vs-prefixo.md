# 03. Slash commands vs. comandos de prefixo

## Os dois modelos

**Comandos de prefixo** (modelo antigo): o bot lê **todas** as mensagens e procura as que começam com um símbolo, como `!ping`.

**Slash commands** (modelo atual): o bot **registra** os comandos no Discord, que mostra um menu com autocompletar quando o usuário digita `/`. Quando alguém usa um comando, o Discord envia uma **interação** pronta ao bot.

## Comparação

| | Slash (`/ping`) | Prefixo (`!ping`) |
|---|---|---|
| Descoberta pelo usuário | Menu com descrição de cada comando | Precisa saber o nome |
| Parâmetros | Campos tipados e validados pelo Discord (números, membros, canais) | Texto livre, convertido pelo bot |
| Intent necessária | Nenhuma | **Message Content** (privilegiada) |
| Respostas ephemeral | Sim | Não |
| Registro | Precisa sincronizar (`tree.sync()`) | Não precisa |
| Permissões | Integradas (`default_permissions`) | Só verificação no código |
| Limite | 100 comandos globais por bot | Ilimitado |
| Recomendação do Discord | ✅ Recomendado | Mantido por compatibilidade |

## Lado a lado no ProgramaBot

**Slash** ([`ping.py`](../code-explanation/commands/general/ping.md)):

```python
@app_commands.command(name="ping", description="Mostra a latência do bot.")
async def ping(self, interaction: discord.Interaction) -> None:
    await interaction.response.send_message("Pong!")
```

**Prefixo** ([`prefix_examples.py`](../code-explanation/commands/general/prefix_examples.md)):

```python
@commands.command(name="ping")
async def ping_prefix(self, ctx: commands.Context) -> None:
    await ctx.send("Pong!")
```

## Sincronização de slash commands

Slash commands precisam ser enviados ao Discord. O ProgramaBot faz isso no `setup_hook`:

- com `GUILD_ID` no `.env`: sincroniza **só no seu servidor**, e os comandos aparecem na hora (ideal para desenvolver);
- sem `GUILD_ID`: sincronização **global**, para todos os servidores; pode levar alguns minutos.

> Se você usar os dois modos, os comandos podem aparecer **duplicados** no seu servidor (uma cópia global e outra do servidor). Para limpar, use um só modo. Comandos globais antigos podem ser removidos sincronizando uma árvore vazia, mas isso é um tópico avançado: consulte a documentação de `CommandTree.sync`.

## Tipos de parâmetro dos slash commands

| Anotação em Python | Campo no Discord |
|---|---|
| `str` | texto |
| `int` | inteiro |
| `float` | número |
| `bool` | verdadeiro/falso |
| `discord.Member` / `discord.User` | seletor de membro/usuário |
| `discord.TextChannel` | seletor de canal |
| `discord.Role` | seletor de cargo |
| `app_commands.Range[int, 1, 100]` | inteiro com limites |
| `app_commands.Range[str, 1, 50]` | texto com tamanho limitado |
| `X \| None = None` | parâmetro opcional |
| `app_commands.Choice[str]` + `@app_commands.choices` | lista fixa de opções |

## Exercício

1. Crie o comando de prefixo `!dado` e o slash `/dado2`, ambos rolando um dado. Compare a experiência do usuário.
2. Em qual modelo é mais fácil para o usuário errar um parâmetro? Por quê?

Documentação: <https://discordpy.readthedocs.io/en/stable/interactions/api.html> e <https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html>
