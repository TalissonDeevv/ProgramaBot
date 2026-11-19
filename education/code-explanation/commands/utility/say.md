# `bot/commands/utility/say.py`: o comando /say

## 1. Nome e localização

- **Arquivo:** `bot/commands/utility/say.py`
- **Comando:** `/say mensagem:<texto>` (requer "Gerenciar mensagens")

## 2. Finalidade

Fazer o bot enviar uma mensagem no canal atual. Quem usou o comando recebe uma confirmação visível só para si.

## 3. Por que foi criado

É um comando simples, mas que exige atenção à **segurança**. Ele ensina:

- a diferença entre `default_permissions` e `checks.has_permissions`;
- a verificar as permissões **do bot** (`bot_has_permissions`);
- a bloquear menções com `AllowedMentions`.

## 4. Como se conecta ao restante do bot

Erros de permissão são traduzidos por [`events/errors.py`](../../events/errors.md) (ex.: "Você precisa da permissão: **Gerenciar mensagens**").

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

- Decorators empilhados.
- `isinstance` com uma *classe abstrata* (`discord.abc.Messageable`).

## 8. Variáveis

- `channel`: o canal onde o comando foi usado.

## 9. Funções

- `Say.say(interaction, mensagem)` e `setup(bot)`.

## 10. Parâmetros

- `mensagem: Range[str, 1, 2000]`: 2000 é o limite de caracteres de uma mensagem do Discord.

## 11. Decorators e métodos utilizados

| Item | Explicação |
|---|---|
| `@app_commands.guild_only()` | Só em servidores. |
| `@app_commands.default_permissions(manage_messages=True)` | **Esconde** o comando de quem não tem a permissão. Os administradores podem mudar isso em *Configurações do servidor > Integrações*. |
| `@app_commands.checks.has_permissions(manage_messages=True)` | **Verifica de verdade**, no momento do uso. |
| `@app_commands.checks.bot_has_permissions(send_messages=True)` | Verifica se o **bot** pode enviar mensagens ali. |
| `discord.abc.Messageable` | "Qualquer coisa onde dá para enviar mensagens" (canal de texto, thread, DM...). |
| `channel.send(texto, allowed_mentions=...)` | Envia a mensagem. |

## 12. Funcionamento do código

### Duas camadas de permissão

`default_permissions` é uma **sugestão** ao Discord sobre quem deve ver o comando, e o dono do servidor pode alterá-la. Já `checks.has_permissions` roda **no bot**, toda vez. Se a verificação falhar, o comando nem executa, e o discord.py lança `MissingPermissions`. Use sempre as duas.

### Bloqueando menções

```python
await channel.send(mensagem, allowed_mentions=discord.AllowedMentions.none())
```

Mesmo um moderador poderia, por engano ou de propósito, usar o bot para marcar `@everyone`. Com `AllowedMentions.none()`, o texto aparece, mas ninguém é notificado.

### Duas respostas diferentes

```python
await channel.send(...)                                   # mensagem pública do bot
await interaction.response.send_message(..., ephemeral=True)  # confirmação privada
```

A interação **sempre** precisa de uma resposta, senão aparece "O aplicativo não respondeu".

## 13. Fluxo de execução

```
/say mensagem:"Olá!"
 ├─ guild_only ✔
 ├─ has_permissions(manage_messages) ✔ (senão: MissingPermissions → errors.py)
 ├─ bot_has_permissions(send_messages) ✔
 ├─ channel.send("Olá!")
 └─ resposta ephemeral "Mensagem enviada!"
```

## 14. Exemplos práticos

Para permitir menções a **usuários**, mas não a cargos ou a @everyone:

```python
allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True)
```

## 15. Erros comuns

- **Comando invisível para alguns membros**: é o `default_permissions` funcionando.
- **"Eu preciso da permissão: Enviar mensagens"**: o bot não pode escrever naquele canal. Ajuste as permissões do canal.

## 16. Como testar

Teste com uma conta **com** e outra **sem** a permissão. Teste também `@everyone` no texto.

## 17. Como modificar

Adicione um parâmetro opcional `canal: discord.TextChannel | None = None` para enviar em outro canal.

## 18. Desafio

Depois de implementar o parâmetro `canal`, verifique se **quem executou** pode enviar mensagens naquele canal: `canal.permissions_for(interaction.user).send_messages`. Sem isso, um moderador poderia usar o bot para escrever em canais que ele mesmo não pode usar.
