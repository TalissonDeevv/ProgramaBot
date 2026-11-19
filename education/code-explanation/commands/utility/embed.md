# `bot/commands/utility/embed.py`: o comando /embed

## 1. Nome e localização

- **Arquivo:** `bot/commands/utility/embed.py`
- **Comando:** `/embed`

## 2. Finalidade

Abrir um formulário (modal) para o usuário criar um embed personalizado.

## 3. Por que foi criado

Para mostrar que **abrir um modal é uma forma de responder a uma interação** e para introduzir o **cooldown** (tempo de espera entre usos).

## 4. Como se conecta ao restante do bot

Toda a lógica está em [`views/embed_modal.py`](../../views/embed_modal.md). Se alguém usar o comando antes do fim do cooldown, o erro `CommandOnCooldown` é tratado por [`events/errors.py`](../../events/errors.md).

## 5. Bibliotecas utilizadas

- [`discord.py`](../../../libraries/discord-py.md).

## 6. Importações

```python
import discord
from discord import app_commands
from discord.ext import commands

from bot.views.embed_modal import EmbedModal
```

## 7. Conceitos de Python utilizados

- Vários decorators empilhados.
- Criação de objeto e passagem como argumento.

## 8. Variáveis

Nenhuma variável local.

## 9. Funções

- `EmbedBuilder.embed(interaction)` e `setup(bot)`.

O Cog se chama `EmbedBuilder`, e não `Embed`, para não ser confundido com a classe `discord.Embed`.

## 10. Parâmetros

- Apenas `interaction`. Os dados vêm do formulário.

## 11. Métodos utilizados

| Método | Explicação |
|---|---|
| `@app_commands.checks.cooldown(1, 30.0)` | Permite **1** uso a cada **30** segundos **por usuário**. |
| `interaction.response.send_modal(modal)` | Abre o formulário. |

## 12. Funcionamento do código

```python
@app_commands.command(name="embed", description="Abre um formulário para criar um embed.")
@app_commands.checks.cooldown(1, 30.0)
async def embed(self, interaction: discord.Interaction) -> None:
    await interaction.response.send_modal(EmbedModal())
```

Decorators são aplicados **de baixo para cima**: primeiro o `cooldown` é aplicado à função, depois o `command` transforma tudo em slash command. O cooldown protege o canal contra *spam* de embeds.

## 13. Fluxo de execução

```
/embed → cooldown ok? → send_modal(EmbedModal()) → formulário na tela → on_submit (embed_modal.py)
/embed de novo em 10 s → CommandOnCooldown → errors.py → "Calma! ... 20 segundo(s)."
```

## 14. Exemplos práticos

Cooldown por **servidor** em vez de por usuário:

```python
@app_commands.checks.cooldown(1, 30.0, key=lambda interaction: interaction.guild_id)
```

## 15. Erros comuns

- **Usar `defer()` antes de `send_modal`**: não funciona, porque o modal precisa ser a primeira resposta.

## 16. Como testar

Use `/embed` duas vezes seguidas e veja a mensagem de cooldown.

## 17. Como modificar

Restrinja o comando a quem tem a permissão "Gerenciar mensagens", copiando os decorators de permissão do [`/say`](say.md).

## 18. Desafio

Crie um comando `/anuncio` que abre um modal com título e texto e envia o embed em um canal específico, escolhido como parâmetro (`canal: discord.TextChannel`). Dica: passe o canal para o `__init__` do modal.
