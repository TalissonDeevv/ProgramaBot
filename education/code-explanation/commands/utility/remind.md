# `bot/commands/utility/remind.py`: o comando /remind

## 1. Nome e localização

- **Arquivo:** `bot/commands/utility/remind.py`
- **Comando:** `/remind tempo:<10m> mensagem:<texto>` (só em servidores)

## 2. Finalidade

Criar lembretes. O bot avisa a pessoa, no mesmo canal, quando chegar a hora, **mesmo que tenha reiniciado** nesse meio-tempo.

## 3. Por que foi criado

É o comando mais completo do projeto. Ele reúne:

- **interpretação de texto** ([`time_parser`](../../utils/time_parser.md));
- **banco de dados** ([`database/reminders`](../../database/reminders.md));
- **tarefas em segundo plano** (`discord.ext.tasks`);
- **ciclo de vida de um Cog** (`cog_load` / `cog_unload`);
- **regras de negócio** (limite de 7 dias e de 10 lembretes por pessoa).

## 4. Como se conecta ao restante do bot

```
bot.settings.database_path (config.py) → ReminderRepository
parse_duration / format_duration (utils/time_parser.py)
success_embed / error_embed / info_embed (utils/embeds.py)
```

## 5. Bibliotecas utilizadas

- [`discord.py`](../../../libraries/discord-py.md), incluindo `discord.ext.tasks`.
- [`datetime`](../../../libraries/datetime.md).
- [`logging`](../../../libraries/logging.md).

## 6. Importações

```python
import logging
from datetime import datetime, timedelta, timezone

import discord
from discord import app_commands
from discord.ext import commands, tasks

from bot.database.reminders import Reminder, ReminderRepository
from bot.utils.embeds import error_embed, info_embed, success_embed
from bot.utils.time_parser import TimeParseError, format_duration, parse_duration
```

## 7. Conceitos de Python utilizados

- **`try / except / finally`** dentro de um `for`.
- **Comparação de `timedelta`** (`delay > MAX_DURATION`).
- **Aritmética de datas** (`datetime.now(timezone.utc) + delay`).
- **Argumentos nomeados** (`user_id=...`), que deixam a chamada autoexplicativa.
- **Métodos "privados"** (`_deliver`).
- **Decorators de outro objeto** (`@check_reminders.before_loop`).

## 8. Variáveis e constantes

| Constante | Valor | Motivo |
|---|---|---|
| `MAX_DURATION` | 7 dias | Evita lembretes "esquecidos" por meses. |
| `MAX_REMINDERS_PER_USER` | 10 | Evita abuso (alguém criando milhares). |
| `CHECK_INTERVAL_SECONDS` | 30 | Frequência da verificação. O lembrete pode chegar até ~30 s depois do horário. |

## 9. Funções e métodos

| Método | Papel |
|---|---|
| `__init__(bot)` | Cria o repositório. |
| `cog_load()` | Cria a tabela e **inicia** a tarefa. |
| `cog_unload()` | **Para** a tarefa. |
| `remind(interaction, tempo, mensagem)` | O comando. |
| `check_reminders()` | Tarefa que roda a cada 30 s. |
| `before_check_reminders()` | Espera o bot ficar pronto antes da primeira execução. |
| `_deliver(reminder)` | Envia um lembrete. |

## 10. Parâmetros

- `tempo: str`: texto como `10m` ou `1d12h`.
- `mensagem: Range[str, 1, 300]`.
- `reminder: Reminder`: um lembrete vindo do banco.

## 11. Métodos do discord.py utilizados

| Método | Explicação |
|---|---|
| `@tasks.loop(seconds=30)` | Transforma o método em uma tarefa repetitiva. |
| `self.check_reminders.start()` / `.cancel()` | Liga / desliga a tarefa. |
| `@check_reminders.before_loop` | Função executada uma vez antes do primeiro ciclo. |
| `self.bot.wait_until_ready()` | Espera o evento `on_ready`. |
| `self.bot.get_channel(id)` | Busca o canal no **cache** (memória). Rápido; pode retornar `None`. |
| `self.bot.fetch_channel(id)` | Busca o canal na **API**. Mais lento; lança exceção se não tiver acesso. |
| `discord.AllowedMentions(everyone=False, roles=False, users=True)` | Só marca usuários. |
| `discord.utils.format_dt(remind_at, "R")` | "em 10 minutos", no fuso de quem lê. |

## 12. Funcionamento do código

### Ciclo de vida do Cog

```python
async def cog_load(self) -> None:
    self.repository.setup()
    self.check_reminders.start()

async def cog_unload(self) -> None:
    self.check_reminders.cancel()
```

O discord.py chama `cog_load` quando o Cog é adicionado e `cog_unload` quando ele é removido. Sem o `cancel`, recarregar a extensão criaria **duas** tarefas rodando ao mesmo tempo.

### Validações em sequência

O comando verifica o formato do tempo, o limite de 7 dias e o limite de lembretes. Cada falha responde com um erro *ephemeral* e termina com `return`.

### A tarefa em segundo plano

```python
@tasks.loop(seconds=CHECK_INTERVAL_SECONDS)
async def check_reminders(self) -> None:
    for reminder in self.repository.get_due():
        try:
            await self._deliver(reminder)
        except Exception:
            logger.exception("Erro ao entregar o lembrete #%s", reminder.id)
        finally:
            self.repository.delete(reminder.id)
```

- Se uma exceção escapar de um `tasks.loop`, **a tarefa para para sempre**. Por isso capturamos `Exception` aqui e registramos com `logger.exception`. Este é um dos poucos lugares em que capturar `Exception` é a escolha certa.
- O `finally` apaga o lembrete mesmo se a entrega falhar. Sem isso, um lembrete para um canal apagado seria tentado a cada 30 segundos, para sempre.

### Por que os lembretes sobrevivem a reinicializações

O lembrete está no arquivo SQLite. Quando o bot volta, a tarefa recomeça e encontra os lembretes vencidos durante o tempo em que ele esteve desligado.

## 13. Fluxo de execução

```
carregamento → cog_load → setup() + start()
                         → before_loop → wait_until_ready → (on_ready)
                         → a cada 30s: get_due → _deliver → delete

/remind tempo:10m mensagem:"Pausa"
 ├─ parse_duration → 10 min
 ├─ ≤ 7 dias? ≤ 10 lembretes? ✔
 ├─ repository.add(...) → id 3
 └─ "Lembrete #3 criado! Vou te avisar em 10 minutos..."
```

## 14. Exemplos práticos

- `/remind tempo:30s mensagem:Teste rápido`
- `/remind tempo:1h30m mensagem:Revisar a aula de funções`

## 15. Erros comuns

- **Lembrete não chega**: confira se o bot tem permissão para enviar mensagens no canal e veja o log.
- **`AttributeError: 'Bot' object has no attribute 'settings'`**: o Cog foi carregado em um bot que não é o `ProgramaBot`.
- **Lembrete atrasado alguns segundos**: é esperado, porque a verificação acontece a cada 30 segundos.

## 16. Como testar

```bash
python -m pytest tests/test_reminders.py tests/test_time_parser.py -v
```

No Discord: crie um lembrete de `30s`, desligue o bot com `Ctrl+C`, espere 1 minuto e ligue de novo. O lembrete será entregue.

## 17. Como modificar

Para enviar o lembrete por **mensagem direta**, troque o canal por `user = await self.bot.fetch_user(reminder.user_id)` e use `await user.send(...)`. Trate `discord.Forbidden`, que acontece quando a pessoa bloqueia DMs.

## 18. Desafio

Crie o comando `/reminders` (lista os seus lembretes) e `/remind-cancel id:<número>` (cancela um lembrete **seu**). Para isso, você precisará de novos métodos no repositório. Verifique que `user_id` é o de quem pediu, para que ninguém cancele os lembretes de outra pessoa.
