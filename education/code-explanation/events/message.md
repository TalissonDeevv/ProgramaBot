# `bot/events/message.py`: o evento on_message

## 1. Nome e localização

- **Arquivo:** `bot/events/message.py`
- **Evento:** `on_message`

## 2. Finalidade

Responder com uma dica quando alguém envia uma mensagem contendo **apenas** a menção ao bot (`@ProgramaBot`).

## 3. Por que foi criado

`on_message` é o evento mais usado (e mais mal usado) em bots. Este arquivo mostra:

- como **ignorar bots** para evitar loops infinitos;
- como adicionar um ouvinte **sem quebrar** os comandos de prefixo;
- o que é possível fazer mesmo **sem** a intent MESSAGE CONTENT.

## 4. Como se conecta ao restante do bot

Usa `self.bot.settings.prefix` para sugerir o comando de prefixo certo.

## 5. Bibliotecas utilizadas

- [`discord.py`](../../libraries/discord-py.md).

## 6. Importações

```python
import discord
from discord.ext import commands
```

## 7. Conceitos de Python utilizados

- Função pura auxiliar (`is_only_mention`), testável.
- Tupla e `in` para comparar com duas formas possíveis.
- `or` em condições de saída (`if message.author.bot or self.bot.user is None`).

## 8. Variáveis

Nenhuma além dos parâmetros.

## 9. Funções

- **`is_only_mention(content, bot_id) -> bool`**: a mensagem é exatamente `<@id>` ou `<@!id>`?
- `Message.on_message(message)` e `setup(bot)`.

## 10. Parâmetros

- `content`: o texto da mensagem.
- `bot_id`: o ID do bot.
- `message: discord.Message`: a mensagem recebida.

## 11. Métodos utilizados

| Item | Explicação |
|---|---|
| `message.author.bot` | `True` se quem enviou é um bot. |
| `message.content` | O texto. Sem a intent MESSAGE CONTENT, fica vazio, **exceto** quando o bot é mencionado, em DMs e nas mensagens do próprio bot. |
| `message.reply(texto, mention_author=False)` | Responde citando a mensagem, sem notificar o autor. |

## 12. Funcionamento do código

```python
if message.author.bot or self.bot.user is None:
    return
```

Se o bot respondesse a bots, dois bots poderiam ficar respondendo um ao outro para sempre. Essa é a primeira linha de qualquer `on_message`.

### `@commands.Cog.listener()` vs. `@bot.event`

O `commands.Bot` já tem um `on_message` interno que processa os comandos de prefixo. Se você **substituísse** esse método com `@bot.event async def on_message(...)`, os comandos `!ping` parariam de funcionar (a não ser que você chamasse `await bot.process_commands(message)` no final). Com `Cog.listener()`, nosso código é um ouvinte **adicional**, e nada quebra.

### Menções: `<@id>` e `<@!id>`

O formato `<@!id>` era usado antigamente para menções por apelido. Aceitamos os dois por compatibilidade.

## 13. Fluxo de execução

```
mensagem "@ProgramaBot"
 ├─ (discord.py) process_commands → não é comando
 └─ Message.on_message
     ├─ autor é bot? não
     ├─ is_only_mention? sim
     └─ reply("Olá! Eu sou o ProgramaBot... Use /help...")
```

## 14. Exemplos práticos

Reagir com 👋 a mensagens que contêm "bom dia" (requer MESSAGE CONTENT):

```python
if "bom dia" in message.content.lower():
    await message.add_reaction("👋")
```

## 15. Erros comuns

- **Bot responde a si mesmo sem parar**: faltou verificar `message.author.bot`.
- **Comandos `!` pararam de funcionar**: alguém usou `@bot.event` para `on_message` sem chamar `process_commands`.
- **`message.content` sempre vazio**: a intent MESSAGE CONTENT está desativada.

## 16. Como testar

```bash
python -m pytest tests/test_command_helpers.py -k mention -v
```

No Discord, envie apenas `@ProgramaBot`.

## 17. Como modificar

Implemente o exemplo do "bom dia" e teste com a intent ativada e desativada.

## 18. Desafio

Crie um contador de mensagens por usuário (em um dicionário `self.counts: dict[int, int]`) e um comando `/mensagens` que mostra quantas mensagens a pessoa enviou desde que o bot ligou. O que acontece com o contador quando o bot reinicia? Como resolver isso? (Dica: [database/reminders.md](../database/reminders.md).)
