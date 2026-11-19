# `bot/events/member_remove.py`: aviso de saída de membros

## 1. Nome e localização

- **Arquivo:** `bot/events/member_remove.py`
- **Evento:** `on_member_remove`
- **Requer:** intent **SERVER MEMBERS**

## 2. Finalidade

Avisar no canal de boas-vindas quando alguém sai do servidor (por vontade própria, expulso ou banido).

## 3. Por que foi criado

Para mostrar a **reutilização de código entre módulos**: em vez de copiar a lógica de escolha de canal, importamos a função de `member_join.py`.

## 4. Como se conecta ao restante do bot

```python
from bot.events.member_join import get_welcome_channel
```

## 5. Bibliotecas utilizadas

- [`discord.py`](../../libraries/discord-py.md).
- [`logging`](../../libraries/logging.md).

## 6. Importações

```python
import logging

import discord
from discord.ext import commands

from bot.events.member_join import get_welcome_channel
from bot.utils.embeds import WARNING_COLOR, base_embed
```

## 7. Conceitos de Python utilizados

- Importar uma função de outro módulo do projeto.
- Tratamento de exceção com `except discord.HTTPException`.

## 8. Variáveis

- `channel`, `embed`.

## 9. Funções

- `MemberRemove.on_member_remove(member)` e `setup(bot)`.

## 10. Parâmetros

- `member: discord.Member`: quem saiu. As informações vêm do cache do bot, do momento em que a pessoa ainda estava no servidor.

## 11. Métodos utilizados

Os mesmos de [`member_join.md`](member_join.md). A diferença é que usamos `str(member)` (nome de usuário), e não `member.mention`: marcar alguém que já saiu não faz sentido.

## 12. Funcionamento do código

```python
channel = get_welcome_channel(member.guild, self.bot.settings.welcome_channel_id)
if channel is None:
    return
```

Se no futuro a regra de escolha do canal mudar, basta alterar `get_welcome_channel`, e os dois eventos passam a seguir a regra nova.

## 13. Fluxo de execução

```
João sai → GUILD_MEMBER_REMOVE → on_member_remove(João)
 → get_welcome_channel → channel.send("👋 Até logo! João saiu...")
```

## 14. Exemplos práticos

Para diferenciar quem foi banido, seria preciso ouvir também o evento `on_member_ban(guild, user)`.

## 15. Erros comuns

- **O aviso aparece também quando eu expulso alguém**: é o comportamento esperado; expulsões também disparam `on_member_remove`.

## 16. Como testar

Saia do servidor de testes com uma conta secundária.

## 17. Como modificar

Envie o aviso em um canal diferente, criando a configuração `GOODBYE_CHANNEL_ID`.

## 18. Desafio

Mostre há quanto tempo a pessoa estava no servidor, usando `member.joined_at` e `discord.utils.format_dt(..., "R")`. Lembre-se de que `joined_at` pode ser `None`.
