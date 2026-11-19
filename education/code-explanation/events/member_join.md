# `bot/events/member_join.py`: boas-vindas a novos membros

## 1. Nome e localização

- **Arquivo:** `bot/events/member_join.py`
- **Evento:** `on_member_join`
- **Requer:** a intent privilegiada **SERVER MEMBERS** (`ENABLE_MEMBERS_INTENT=true` e ativada no Developer Portal)

## 2. Finalidade

Enviar um embed de boas-vindas quando alguém entra no servidor.

## 3. Por que foi criado

Para ensinar **eventos com parâmetros** (o evento recebe o `Member` que entrou) e **intents privilegiadas**. Além disso, a função `get_welcome_channel` é reaproveitada pelo [`member_remove.py`](member_remove.md).

## 4. Como se conecta ao restante do bot

- Lê `self.bot.settings.welcome_channel_id` ([`config.py`](../config.md)).
- `member_remove.py` importa `get_welcome_channel` daqui.

## 5. Bibliotecas utilizadas

- [`discord.py`](../../libraries/discord-py.md).
- [`logging`](../../libraries/logging.md).

## 6. Importações

```python
import logging

import discord
from discord.ext import commands

from bot.utils.embeds import SUCCESS_COLOR, base_embed
```

## 7. Conceitos de Python utilizados

- **Expressão condicional**: `guild.get_channel(channel_id) if channel_id else None`.
- **`isinstance`** para garantir que o canal configurado é de texto.
- **Estratégia de fallback** ("se não tiver o configurado, use o padrão").
- **Função de nível de módulo reutilizada por outro módulo.**

## 8. Variáveis

- `channel`: o canal escolhido.
- `embed`: a mensagem.

## 9. Funções

- **`get_welcome_channel(guild, channel_id) -> discord.TextChannel | None`**:
  1. tenta o canal de `WELCOME_CHANNEL_ID`;
  2. senão, usa o *canal de mensagens do sistema* do servidor;
  3. só devolve o canal se o bot puder escrever nele.
- `MemberJoin.cog_load()`: avisa no log se a intent estiver desativada.
- `MemberJoin.on_member_join(member)`: o evento.

## 10. Parâmetros

- `guild`: o servidor.
- `channel_id`: o ID configurado (ou `None`).
- `member: discord.Member`: quem entrou.

## 11. Métodos utilizados

| Método | Explicação |
|---|---|
| `guild.get_channel(id)` | Busca o canal no cache (pode ser `None`). |
| `guild.system_channel` | Canal definido em *Configurações do servidor > Visão geral > Canal de mensagens do sistema*. |
| `channel.permissions_for(guild.me).send_messages` | O bot pode escrever ali? |
| `member.mention` | Texto `<@id>`, que marca a pessoa. |
| `member.guild.member_count` | Número de membros. |
| `self.bot.intents.members` | Indica se a intent está ativa. |

## 12. Funcionamento do código

```python
channel = guild.get_channel(channel_id) if channel_id else None
if not isinstance(channel, discord.TextChannel):
    channel = guild.system_channel
```

`get_channel` pode devolver um canal de voz ou uma categoria, caso o ID errado tenha sido configurado. O `isinstance` evita tentar enviar mensagens nesses tipos.

```python
if not channel.permissions_for(guild.me).send_messages:
    return None
```

Verificar antes evita um erro `Forbidden` toda vez que alguém entrar.

### Por que a intent é necessária?

Eventos de membros podem revelar quem está em um servidor. Por questões de privacidade, o Discord só envia esses eventos a bots que pediram explicitamente a intent. Bots em mais de 100 servidores precisam de aprovação do Discord para usá-la.

## 13. Fluxo de execução

```
Ana entra no servidor
 → Discord envia o evento GUILD_MEMBER_ADD (só com intent members)
 → discord.py chama on_member_join(member=Ana)
     ├─ get_welcome_channel → #boas-vindas
     └─ channel.send(embed "👋 Boas-vindas! Olá, @Ana!...")
```

## 14. Exemplos práticos

Dar um cargo automaticamente a quem entra (o bot precisa da permissão "Gerenciar cargos" e de um cargo acima do cargo dado):

```python
role = member.guild.get_role(123456789012345678)
if role is not None:
    await member.add_roles(role, reason="Cargo automático de entrada")
```

## 15. Erros comuns

- **Nada acontece**: (1) a intent está desativada no Portal ou no `.env`; (2) o servidor não tem canal do sistema e `WELCOME_CHANNEL_ID` está vazio; (3) o bot não pode escrever no canal.
- **`PrivilegedIntentsRequired` ao iniciar**: `ENABLE_MEMBERS_INTENT=true`, mas a intent não foi ativada no Portal.

## 16. Como testar

Entre no servidor de testes com uma conta secundária (ou saia e entre novamente).

## 17. Como modificar

Personalize a mensagem e adicione uma imagem com `embed.set_image(url=...)`.

## 18. Desafio

Resolva o [exercício 11](../../exercises/03-intermediario.md#exercício-11--criar-um-evento-de-boas-vindas): faça o bot também enviar uma **mensagem direta** de boas-vindas para o novo membro, tratando o caso de DMs fechadas.
