# `bot/commands/utility/poll.py`: o comando /poll

## 1. Nome e localização

- **Arquivo:** `bot/commands/utility/poll.py`
- **Comando:** `/poll pergunta:<texto> opcoes:<A; B; C> [duracao_minutos]`

## 2. Finalidade

Criar uma enquete com um botão por opção e encerrá-la automaticamente depois da duração escolhida (padrão: 10 minutos; máximo: 24 horas).

## 3. Por que foi criado

Para mostrar, na prática, que **`await asyncio.sleep` não trava o bot**. O comando fica "esperando" por vários minutos, e mesmo assim todos os outros comandos (e os votos na própria enquete) continuam funcionando.

## 4. Como se conecta ao restante do bot

A lógica e os botões estão em [`views/poll.py`](../../views/poll.md). Aqui ficam só a validação, o envio e o encerramento.

## 5. Bibliotecas utilizadas

- [`asyncio`](../../../libraries/asyncio.md): `asyncio.sleep`.
- [`datetime`](../../../libraries/datetime.md): `timedelta`.
- [`discord.py`](../../../libraries/discord-py.md).

## 6. Importações

```python
import asyncio
from datetime import timedelta

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import error_embed
from bot.views.poll import PollError, PollState, PollView, parse_poll_options
```

## 7. Conceitos de Python utilizados

- **Corrotinas e `await`**: o comando pausa sem bloquear.
- **`timedelta`** e `total_seconds()`.
- **Parâmetro com valor padrão** no Discord (`duracao_minutos = 10`).
- **Composição de objetos**: `PollView(PollState(...), ...)`.

## 8. Variáveis

- `options`: lista validada.
- `duration`: `timedelta(minutes=duracao_minutos)`.
- `view`: a `PollView`.
- `sent_message`: a mensagem enviada.

## 9. Funções

- `Poll.poll(interaction, pergunta, opcoes, duracao_minutos=10)` e `setup(bot)`.

## 10. Parâmetros

- `pergunta: Range[str, 1, 200]`: limitada para caber no título do embed (256 caracteres, com o emoji).
- `opcoes: str`: texto livre, validado por `parse_poll_options`.
- `duracao_minutos: Range[int, 1, 1440] = 10`: o Discord só aceita números nesse intervalo.

## 11. Métodos utilizados

| Método | Explicação |
|---|---|
| `interaction.original_response()` | Busca a mensagem que acabamos de enviar como resposta. |
| `message.channel.get_partial_message(id)` | Cria uma referência leve à mensagem, editável com o token do bot. |
| `asyncio.sleep(segundos)` | Pausa **esta** corrotina; o resto do bot continua. |
| `view.finish()` | Desativa os botões e mostra o resultado final. |

## 12. Funcionamento do código

```python
sent_message = await interaction.original_response()
view.message = sent_message.channel.get_partial_message(sent_message.id)

await asyncio.sleep(duration.total_seconds())
await view.finish()
```

**Por que não `time.sleep`?** `time.sleep(600)` congelaria o bot **inteiro** por 10 minutos: ninguém conseguiria usar comandos e nem votar. `asyncio.sleep` devolve o controle ao *event loop*, que continua atendendo outras tarefas. Veja [Programação assíncrona](../../../python/13-programacao-assincrona.md).

**Por que `PartialMessage`?** O token de uma interação expira em 15 minutos. Uma enquete de 1 hora não conseguiria se editar no final usando `interaction.edit_original_response`.

## 13. Fluxo de execução

```
/poll pergunta:"Linguagem?" opcoes:"Python; JS" duracao_minutos:5
 ├─ parse_poll_options → ["Python", "JS"]
 ├─ PollView(...) → send_message(embed, view)
 ├─ guarda PartialMessage
 ├─ await asyncio.sleep(300)  ← enquanto isso, as pessoas votam
 └─ view.finish() → resultado final, botões desativados
```

## 14. Exemplos práticos

`/poll pergunta:Qual o melhor horário para a aula? opcoes:Manhã; Tarde; Noite duracao_minutos:60`

## 15. Erros comuns

- **"Informe pelo menos 2 opções"**: as opções precisam estar separadas por **ponto e vírgula**, não por vírgula.
- **A enquete não termina**: se o bot reiniciar durante a espera, a corrotina é perdida e a mensagem fica com os botões ativos (mas sem funcionar).

## 16. Como testar

```bash
python -m pytest tests/test_poll.py -v
```

No Discord, crie uma enquete de 1 minuto e vote com duas contas.

## 17. Como modificar

Anuncie o vencedor ao final: depois de `view.finish()`, calcule `max(range(len(counts)), key=counts.__getitem__)` e envie uma mensagem no canal com `sent_message.channel.send(...)`.

## 18. Desafio

Trate o **empate**: se duas opções tiverem o mesmo número de votos, o anúncio deve listar todas as vencedoras.
