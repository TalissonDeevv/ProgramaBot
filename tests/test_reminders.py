"""Testes do banco de lembretes (bot/database/reminders.py), usando um arquivo temporário."""

from datetime import datetime, timedelta, timezone

import pytest

from bot.database.reminders import ReminderRepository


@pytest.fixture
def repository(tmp_path):
    repo = ReminderRepository(tmp_path / "subpasta" / "lembretes.db")
    repo.setup()
    return repo


def test_setup_creates_database_file(repository):
    assert repository.database_path.is_file()


def test_add_and_get_due(repository):
    now = datetime.now(timezone.utc)
    past_id = repository.add(user_id=1, channel_id=10, message="Estudar", remind_at=now - timedelta(minutes=1))
    repository.add(user_id=1, channel_id=10, message="Futuro", remind_at=now + timedelta(hours=1))

    due = repository.get_due(now)
    assert [reminder.id for reminder in due] == [past_id]
    assert due[0].message == "Estudar"
    assert due[0].remind_at.tzinfo is not None


def test_count_and_delete(repository):
    now = datetime.now(timezone.utc)
    first = repository.add(1, 10, "a", now)
    repository.add(1, 10, "b", now)
    repository.add(2, 10, "c", now)
    assert repository.count_for_user(1) == 2
    repository.delete(first)
    assert repository.count_for_user(1) == 1


def test_sql_injection_is_stored_as_text(repository):
    now = datetime.now(timezone.utc)
    malicious = "'); DROP TABLE reminders; --"
    repository.add(1, 10, malicious, now)
    assert repository.get_due(now + timedelta(seconds=1))[0].message == malicious
