# `bot/database/reminders.py`: banco de dados dos lembretes

## 1. Nome e localização

- **Arquivo:** `bot/database/reminders.py`
- **Banco gerado:** `data/programabot.db` (configurável em `DATABASE_PATH`; ignorado pelo Git)

## 2. Finalidade

Guardar os lembretes do `/remind` em um banco de dados **SQLite**, para que eles não se percam quando o bot reinicia.

## 3. Por que foi criado

Tudo o que fica em variáveis desaparece quando o programa termina. Para *persistir* dados, eles precisam ir para um arquivo. O SQLite é ideal para começar:

- já vem com o Python (módulo `sqlite3`);
- o banco inteiro é **um único arquivo**;
- usa SQL, a linguagem de bancos de dados mais usada do mundo.

Este arquivo segue o padrão **Repository**: todo o SQL fica aqui. O comando `/remind` não sabe que existe SQL; ele só chama `repository.add(...)`. Se um dia o projeto trocar SQLite por PostgreSQL, só este arquivo muda.

## 4. Como se conecta ao restante do bot

```
commands/utility/remind.py
 ├─ __init__   → ReminderRepository(bot.settings.database_path)
 ├─ cog_load   → repository.setup()
 ├─ /remind    → repository.count_for_user(...) e repository.add(...)
 └─ a cada 30s → repository.get_due() → entrega → repository.delete(id)
```

## 5. Bibliotecas utilizadas

- [`sqlite3`](../../libraries/sqlite3.md) (nativa).
- [`dataclasses`](../../libraries/dataclasses.md) (nativa).
- [`datetime`](../../libraries/datetime.md) (nativa).
- [`pathlib`](../../libraries/pathlib.md) (nativa).

## 6. Importações

```python
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
```

## 7. Conceitos de Python utilizados

- **Classes com estado** (`self.database_path`).
- **Dataclass imutável** para representar um registro (`Reminder`).
- **`try/finally`**: garante que a conexão seja fechada, mesmo com erro.
- **Context manager** (`with connection:`) para controlar transações.
- **Retorno de tupla**: `return rows, lastrowid` e desempacotamento `_, reminder_id = ...`. O `_` indica "valor que não vou usar".
- **`@staticmethod`**: método que não usa `self`.
- **Timestamps**: datas guardadas como número de segundos desde 01/01/1970 (UTC).

## 8. Variáveis e constantes

`CREATE_TABLE_SQL` define a tabela:

| Coluna | Tipo | Significado |
|---|---|---|
| `id` | `INTEGER PRIMARY KEY AUTOINCREMENT` | Número único gerado pelo banco |
| `user_id` | `INTEGER` | Quem criou |
| `channel_id` | `INTEGER` | Onde avisar |
| `message` | `TEXT` | O texto do lembrete |
| `remind_at` | `INTEGER` | Quando avisar (timestamp) |
| `created_at` | `INTEGER` | Quando foi criado (timestamp) |

`NOT NULL` impede que a coluna fique vazia. `IF NOT EXISTS` permite executar o comando várias vezes sem erro.

## 9. Funções e métodos

| Método | SQL executado | Retorno |
|---|---|---|
| `setup()` | `CREATE TABLE IF NOT EXISTS ...` | — |
| `add(user_id, channel_id, message, remind_at)` | `INSERT INTO reminders ...` | ID do lembrete |
| `get_due(now=None)` | `SELECT ... WHERE remind_at <= ?` | lista de `Reminder` |
| `count_for_user(user_id)` | `SELECT COUNT(*) ...` | `int` |
| `delete(reminder_id)` | `DELETE FROM reminders WHERE id = ?` | — |
| `_execute(query, parameters)` | qualquer um | `(linhas, lastrowid)` |
| `_row_to_reminder(row)` | — | `Reminder` |

## 10. Parâmetros

- `database_path`: caminho do arquivo `.db`.
- `query`: o texto SQL.
- `parameters`: uma **tupla** com os valores que substituem cada `?`. Para um único valor, a vírgula é obrigatória: `(user_id,)`.
- `now`: momento de referência. Os testes passam um horário fixo; o bot usa o horário atual.

## 11. Métodos do sqlite3 utilizados

| Método | Explicação |
|---|---|
| `sqlite3.connect(caminho)` | Abre o arquivo do banco (e cria, se não existir). |
| `connection.row_factory = sqlite3.Row` | As linhas passam a aceitar `row["coluna"]`, não só `row[0]`. |
| `with connection:` | Faz `commit` (salva) se o bloco terminar bem, ou `rollback` (desfaz) se der erro. **Não fecha a conexão.** |
| `connection.execute(sql, params)` | Executa o SQL e devolve um cursor. |
| `cursor.fetchall()` | Lista com todas as linhas do resultado. |
| `cursor.lastrowid` | ID da última linha inserida. |
| `connection.close()` | Fecha a conexão. |

## 12. Funcionamento do código

### Abrindo e fechando conexões com segurança

```python
connection = sqlite3.connect(self.database_path)
connection.row_factory = sqlite3.Row
try:
    with connection:
        cursor = connection.execute(query, parameters)
        return cursor.fetchall(), cursor.lastrowid
finally:
    connection.close()
```

O `finally` executa **sempre**, até depois do `return`. O `with connection` cuida apenas da transação. Essa diferença costuma surpreender: muita gente acha que ele também fecha a conexão.

### Evitando SQL injection

```python
"INSERT INTO reminders (user_id, channel_id, message, remind_at, created_at) VALUES (?, ?, ?, ?, ?)"
```

Os valores **nunca** são colados no texto do SQL com f-string. Se fossem, uma mensagem como `'); DROP TABLE reminders; --` poderia apagar a tabela. Com `?`, o SQLite trata o valor sempre como **dado**, nunca como comando. O teste `test_sql_injection_is_stored_as_text` comprova isso.

### Por que timestamps?

```python
int(remind_at.timestamp())
datetime.fromtimestamp(row["remind_at"], tz=timezone.utc)
```

Números são fáceis de comparar (`remind_at <= agora`) e não têm ambiguidade de fuso horário.

## 13. Fluxo de execução

```
/remind 10m "Beber água"
 └─ add(...) → INSERT → id = 7

loop a cada 30s
 └─ get_due() → SELECT ... WHERE remind_at <= agora
     └─ [Reminder(id=7, ...)] → entrega → delete(7)
```

## 14. Exemplos práticos

```python
from datetime import datetime, timedelta, timezone
from pathlib import Path
from bot.database.reminders import ReminderRepository

repo = ReminderRepository(Path("teste.db"))
repo.setup()
repo.add(user_id=1, channel_id=2, message="Estudar SQL", remind_at=datetime.now(timezone.utc))
print(repo.get_due())
```

Para explorar o arquivo `.db` visualmente, use o programa gratuito [DB Browser for SQLite](https://sqlitebrowser.org/).

## 15. Erros comuns

- **`sqlite3.OperationalError: no such table`**: `setup()` não foi chamado.
- **`database is locked`**: outro programa (como o DB Browser) está com o banco aberto e com alterações não salvas.
- **`(user_id)` sem vírgula**: isso não é uma tupla, só um número entre parênteses. Use `(user_id,)`.

## 16. Como testar

```bash
python -m pytest tests/test_reminders.py -v
```

Os testes usam a fixture `tmp_path` do pytest, que cria uma pasta temporária. Assim, seu banco real nunca é tocado.

## 17. Como modificar

Para listar os lembretes de um usuário, crie um método:

```python
def list_for_user(self, user_id: int) -> list[Reminder]:
    rows, _ = self._execute(
        "SELECT id, user_id, channel_id, message, remind_at FROM reminders WHERE user_id = ? ORDER BY remind_at",
        (user_id,),
    )
    return [self._row_to_reminder(row) for row in rows]
```

## 18. Desafio

Usando o método acima, crie o comando `/reminders`, que mostra os lembretes pendentes de quem o executou (*ephemeral*). Depois, crie um teste para `list_for_user`.

> **Nota técnica:** o `sqlite3` é *síncrono*, ou seja, bloqueia o bot enquanto executa. Para consultas pequenas como estas, isso leva frações de milissegundo e não causa problemas. Em bots grandes, usa-se `asyncio.to_thread(...)` ou bibliotecas assíncronas. Veja [Programação assíncrona](../../python/13-programacao-assincrona.md).
