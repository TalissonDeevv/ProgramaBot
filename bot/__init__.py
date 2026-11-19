"""Pacote principal do ProgramaBot.

Este arquivo transforma a pasta ``bot/`` em um *pacote* Python. Graças a ele,
outros arquivos podem escrever ``from bot.config import load_settings``.

Também guardamos aqui informações gerais do projeto, que são reutilizadas
por comandos como ``/about``.
"""

__version__ = "1.0.0-dev"
__maintainer__ = "Talisson Souza"

REPOSITORY_URL = "https://github.com/TalissonDeevv/ProgramaBot"
