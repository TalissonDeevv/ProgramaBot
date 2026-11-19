# `bot/commands/moderation/clear.py`: o comando /clear

## 1. Nome e localização

- **Arquivo:** `bot/commands/moderation/clear.py`
- **Comando:** `/clear quantidade:<1-100>` (requer "Gerenciar mensagens")

## 2. Finalidade

Apagar de 1 a 100 mensagens recentes do canal atual.

## 3. Por que foi criado

Para ensinar o **`defer()`**: como responder a um comando que pode levar mais de 3 segundos.

## 4. Como se conecta ao restante do bot

Usa os embeds de sucesso/erro. Os erros de permissão vão para [`events/errors.py`](../../events/errors.md).

## 5. Bibliotecas utilizadas

- [`discord.py`](../../../libraries/discord-py.md).

## 6. Importações

```python
import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import error_embed, success_embed
```

## 7. Conceitos de Python utilizados

- **Tupla de classes** em `isinstance(channel, (A, B, C))`.
- `len()` em uma lista retornada.
- Expressão condicional para singular/plural.

## 8. Variáveis e constantes

- `PURGEABLE_CHANNELS = (discord.TextChannel, discord.Thread, discord.VoiceChannel)`: tipos de canal que têm o método `purge`.
- `deleted`: a lista de mensagens apagadas.

## 9. Funções

- `Clear.clear(interaction, quantidade)` e `setup(bot)`.

## 10. Parâmetros

- `quantidade: Range[int, 1, 100]`: o Discord recusa valores fora desse intervalo antes de chegar ao bot.

## 11. Métodos utilizados

| Método | Explicação |
|---|---|
| `interaction.response.defer(ephemeral=True, thinking=True)` | Responde "ProgramaBot está pensando..." e ganha **15 minutos** para concluir. |
| `channel.purge(limit=, reason=)` | Apaga mensagens. Retorna a lista das apagadas. |
| `interaction.followup.send(...)` | Envia a resposta final depois do `defer`. |
| `bot_has_permissions(manage_messages=True, read_message_history=True)` | O bot precisa ver o histórico e poder apagar. |

## 12. Funcionamento do código

```python
await interaction.response.defer(ephemeral=True, thinking=True)
deleted = await channel.purge(limit=quantidade, reason=f"/clear usado por {interaction.user}")
await interaction.followup.send(embed=success_embed(...), ephemeral=True)
```

O Discord exige uma resposta em até **3 segundos**. Apagar 100 mensagens pode demorar mais. O `defer` "segura" a interação, e o `followup.send` entrega o resultado depois.

**Limite de 14 dias:** o Discord só permite apagar *em massa* mensagens com menos de 14 dias. O `purge` apaga as mais antigas uma a uma, o que é bem mais lento.

## 13. Fluxo de execução

```
/clear quantidade:20
 ├─ permissões (usuário e bot) ✔
 ├─ tipo de canal ✔
 ├─ defer → "pensando..."
 ├─ purge(limit=20) → 20 mensagens
 └─ followup "🧹 20 mensagens apagadas." (ephemeral)
```

## 14. Exemplos práticos

Apagar só as mensagens de bots:

```python
deleted = await channel.purge(limit=quantidade, check=lambda message: message.author.bot)
```

## 15. Erros comuns

- **`InteractionResponded`**: usar `response.send_message` depois do `defer`. Depois do `defer`, use `followup`.
- **"Eu preciso da permissão: Ver histórico de mensagens"**: ajuste as permissões do bot no canal.

## 16. Como testar

Envie algumas mensagens em um canal de testes e use `/clear quantidade:5`.

## 17. Como modificar

Adicione um parâmetro opcional `usuario: discord.Member | None` e use o `check=` para apagar só as mensagens dessa pessoa.

## 18. Desafio

Implemente a modificação acima. Atenção: com `check`, `limit` passa a ser a quantidade de mensagens **analisadas**, não de apagadas. Explique esse comportamento na resposta ao usuário.
