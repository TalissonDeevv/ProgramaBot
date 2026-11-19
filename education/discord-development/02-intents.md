# 02. Intents

## O que são?

*Intents* ("intenções") são a lista de **tipos de evento** que o bot quer receber pelo gateway. O bot as informa ao se conectar, e o Discord só envia os eventos correspondentes.

Por que existem? Para economizar recursos (um bot em milhares de servidores não precisa receber tudo) e para proteger a **privacidade** dos usuários.

## Intents comuns e privilegiadas

`discord.Intents.default()` liga todas as intents **comuns** (servidores, canais, cargos, reações, mensagens sem o texto...).

Três intents são **privilegiadas**. Além de serem pedidas no código, precisam ser **ativadas no Developer Portal** (aba **Bot** > *Privileged Gateway Intents*):

| Intent | No código | Libera | Usado no ProgramaBot por |
|---|---|---|---|
| **Server Members** | `intents.members` | eventos de entrada e saída de membros; lista completa de membros | `on_member_join`, `on_member_remove` |
| **Message Content** | `intents.message_content` | o **texto** das mensagens | comandos de prefixo (`!ping`) |
| **Presence** | `intents.presences` | status online e atividade dos usuários | não usado |

> Bots em **mais de 100 servidores** precisam ser verificados pelo Discord e justificar o uso das intents privilegiadas.

## Como o ProgramaBot configura

Em [`bot/main.py`](../code-explanation/main.md):

```python
def build_intents(settings: Settings) -> discord.Intents:
    intents = discord.Intents.default()
    intents.members = settings.enable_members_intent
    intents.message_content = settings.enable_message_content_intent
    return intents
```

E no `.env`:

```ini
ENABLE_MEMBERS_INTENT=true
ENABLE_MESSAGE_CONTENT_INTENT=true
```

## O que acontece se...

| Situação | Resultado |
|---|---|
| `true` no `.env`, mas **desligada** no Portal | O bot não conecta: `PrivilegedIntentsRequired`. O ProgramaBot mostra uma mensagem explicando. |
| `false` no `.env` | O bot conecta, mas: sem `members`, não há boas-vindas; sem `message_content`, os comandos `!` não funcionam (só com `@ProgramaBot ping`). |
| Slash commands | Funcionam **sem** nenhuma intent privilegiada. |

## Por que slash commands não precisam de Message Content?

Ao usar um slash command, o Discord envia uma **interação** com os parâmetros já separados e validados. O bot não precisa ler mensagens. É um dos motivos pelos quais o Discord recomenda slash commands. Veja [Slash commands vs. prefixo](03-slash-vs-prefixo.md).

## Exceções da Message Content

Mesmo sem a intent, o bot recebe o texto das mensagens que **o mencionam**, das mensagens diretas e das próprias mensagens. É por isso que o [`on_message`](../code-explanation/events/message.md) do ProgramaBot funciona com a intent desligada.

## Exercício

1. Coloque `ENABLE_MESSAGE_CONTENT_INTENT=false` no `.env`, reinicie e teste `!ping` e `@ProgramaBot ping`. Explique a diferença.
2. Desligue a Server Members Intent **só no Portal** (deixe `true` no `.env`) e inicie o bot. Leia a mensagem de erro. Depois, volte a ligar.

Documentação: <https://discord.com/developers/docs/topics/gateway#gateway-intents> e <https://discordpy.readthedocs.io/en/stable/intents.html>
