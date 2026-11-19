"""Armazena os lembretes do comando ``/remind`` em um banco SQLite.

Por que um banco de dados? Se os lembretes ficassem só na memória (em uma
lista, por exemplo), todos seriam perdidos quando o bot reiniciasse. O SQLite
salva os dados em um arquivo (``data/programabot.db``) e já vem com o Python.

Este arquivo segue o padrão *Repository*: toda a conversa com o banco fica
aqui dentro. O comando ``/remind`` não escreve SQL; ele só chama métodos
como ``add`` e ``get_due``.
"""

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    remind_at INTEGER NOT NULL,
    created_at INTEGER NOT NULL
)
"""


@dataclass(frozen=True)
class Reminder:
    """Um lembrete salvo no banco."""

    id: int
    user_id: int
    channel_id: int
    message: str
    remind_at: datetime


class ReminderRepository:
    """Operações de criar, buscar, contar e apagar lembretes."""

    def __init__(self, database_path: Path) -> None:
        self.database_path = Path(database_path)

    def _execute(self, query: str, parameters: tuple = ()) -> tuple[list[sqlite3.Row], int | None]:
        """Abre uma conexão, executa uma instrução SQL e fecha a conexão.

        Returns:
            As linhas encontradas e o ID da última linha inserida.
        """
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome.
        try:
            # "with connection" confirma (commit) se der certo ou desfaz (rollback) se der erro.
            with connection:
                cursor = connection.execute(query, parameters)
                return cursor.fetchall(), cursor.lastrowid
        finally:
            connection.close()

    def setup(self) -> None:
        """Cria a pasta e a tabela, caso ainda não existam."""
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._execute(CREATE_TABLE_SQL)

    def add(self, user_id: int, channel_id: int, message: str, remind_at: datetime) -> int:
        """Salva um lembrete e retorna o ID gerado pelo banco."""
        now = int(datetime.now(timezone.utc).timestamp())
        # Os "?" são preenchidos pelo SQLite com segurança (evita SQL injection).
        _, reminder_id = self._execute(
            "INSERT INTO reminders (user_id, channel_id, message, remind_at, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (user_id, channel_id, message, int(remind_at.timestamp()), now),
        )
        return int(reminder_id)

    def get_due(self, now: datetime | None = None) -> list[Reminder]:
        """Retorna os lembretes cujo horário já chegou."""
        moment = now or datetime.now(timezone.utc)
        rows, _ = self._execute(
            "SELECT id, user_id, channel_id, message, remind_at FROM reminders "
            "WHERE remind_at <= ? ORDER BY remind_at",
            (int(moment.timestamp()),),
        )
        return [self._row_to_reminder(row) for row in rows]

    def count_for_user(self, user_id: int) -> int:
        """Quantos lembretes pendentes um usuário possui."""
        rows, _ = self._execute("SELECT COUNT(*) AS total FROM reminders WHERE user_id = ?", (user_id,))
        return int(rows[0]["total"])

    def delete(self, reminder_id: int) -> None:
        """Apaga um lembrete (normalmente depois de entregá-lo)."""
        self._execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))

    @staticmethod
    def _row_to_reminder(row: sqlite3.Row) -> Reminder:
        """Converte uma linha do banco em um objeto ``Reminder``."""
        return Reminder(
            id=row["id"],
            user_id=row["user_id"],
            channel_id=row["channel_id"],
            message=row["message"],
            remind_at=datetime.fromtimestamp(row["remind_at"], tz=timezone.utc),
        )
