"""Fixtures compartilhadas pelos testes.

Uma *fixture* é uma função que prepara algo que vários testes precisam.
O pytest a executa automaticamente quando um teste pede por ela pelo nome.
"""

from pathlib import Path

import pytest

from bot.config import Settings
from bot.main import ProgramaBot, discover_extensions

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    """Configurações falsas: o banco fica em uma pasta temporária e o token não é real."""
    return Settings(token="token-de-teste", database_path=tmp_path / "test.db")


@pytest.fixture
async def loaded_bot(settings: Settings):
    """Um ProgramaBot com todas as extensões carregadas, SEM conectar ao Discord."""
    bot = ProgramaBot(settings)
    # "async with bot" prepara o estado interno do bot (sem fazer login no Discord)
    # e o fecha corretamente no final do teste.
    async with bot:
        for extension in discover_extensions():
            await bot.load_extension(extension)
        yield bot
        # Descarregar para a tarefa de lembretes (tasks.loop) ser cancelada.
        for extension in list(bot.extensions):
            await bot.unload_extension(extension)
