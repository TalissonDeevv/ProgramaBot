# `bot/commands/information/serverinfo.py`: o comando /serverinfo

## 1. Nome e localização

- **Arquivo:** `bot/commands/information/serverinfo.py`
- **Comando:** `/serverinfo` (só em servidores)

## 2. Finalidade

Mostrar dados do servidor: dono, número de membros, ID, quantidade de canais de texto e voz, cargos, impulsos (*boosts*) e data de criação.

## 3. Por que foi criado

Para explorar o objeto `discord.Guild` ("guild" é o nome técnico de "servidor" na API do Discord) e praticar a construção de embeds com vários campos.

## 4. Como se conecta ao restante do bot

Usa `base_embed`. Segue o mesmo padrão do [`/userinfo`](userinfo.md).

## 5. Bibliotecas utilizadas

- [`discord.py`](../../../libraries/discord-py.md).

## 6. Importações

```python
import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import base_embed
```

## 7. Conceitos de Python utilizados

- Verificação de `None` (`if guild is None`, `if guild.icon is not None`).
- `len()` em listas.
- `or` para valores ausentes (`guild.member_count or "Desconhecido"`).
- f-strings com chamadas de função dentro.

## 8. Variáveis

- `guild`: o servidor onde o comando foi usado.
- `embed`: a resposta.

## 9. Funções

- `ServerInfo.serverinfo(interaction)` e `setup(bot)`.

## 10. Parâmetros

- Apenas `interaction`.

## 11. Atributos utilizados

| Atributo | Explicação |
|---|---|
| `interaction.guild` | O servidor, ou `None` em mensagens diretas. |
| `guild.name` / `guild.description` | Nome e descrição (a descrição pode ser `None`). |
| `guild.icon` | Ícone (`Asset`) ou `None`. |
| `guild.owner_id` | ID do dono. Usamos `<@id>` para exibi-lo como menção. |
| `guild.member_count` | Total de membros (pode ser `None` sem as informações completas do servidor). |
| `guild.text_channels` / `guild.voice_channels` | Listas de canais. |
| `guild.roles` | Lista de cargos (inclui `@everyone`). |
| `guild.premium_subscription_count` | Número de impulsos. |
| `guild.premium_tier` | Nível de impulso (0 a 3). |
| `guild.created_at` | Data de criação. |

## 12. Funcionamento do código

```python
guild = interaction.guild
if guild is None:
    await interaction.response.send_message("Use este comando em um servidor.", ephemeral=True)
    return
```

Mesmo com `@app_commands.guild_only()`, verificamos `None`. É uma **programação defensiva** que também ajuda o editor a saber que, dali em diante, `guild` não é `None`.

```python
embed.add_field(name="Dono", value=f"<@{guild.owner_id}>")
```

Usar `guild.owner` exigiria o membro em cache (o que depende da intent `members`). Já o ID está sempre disponível, e a sintaxe `<@id>` faz o Discord mostrar o nome.

## 13. Fluxo de execução

```
/serverinfo → guild existe? → embed com thumbnail e 8 campos → resposta sem notificar menções
```

## 14. Exemplos práticos

Contar membros que são bots (requer a intent `members`):

```python
bots = sum(1 for member in guild.members if member.bot)
```

## 15. Erros comuns

- **Membros = "Desconhecido"**: em casos raros, o Discord não envia a contagem.
- **Valor de campo vazio** (`""`) gera erro. Por isso usamos `or 0` e `or "Desconhecido"`.

## 16. Como testar

Use `/serverinfo` em um servidor com e sem ícone.

## 17. Como modificar

Adicione a quantidade de **emojis** personalizados: `len(guild.emojis)`.

## 18. Desafio

Adicione um campo "Categorias" com `len(guild.categories)` e um campo "Nível de verificação" usando `guild.verification_level`. Traduza os valores do *enum* para português com um dicionário.
