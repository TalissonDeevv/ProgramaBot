"""Configuração dos logs (registros) do ProgramaBot.

Logs são mensagens que o programa escreve para contar o que está acontecendo:
"bot conectado", "comando executado", "erro ao enviar mensagem"... Eles aparecem
no terminal e também são salvos em ``logs/programabot.log``.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%d/%m/%Y %H:%M:%S"
LOG_FILE_NAME = "programabot.log"
MAX_LOG_BYTES = 1_000_000  # 1 MB por arquivo
BACKUP_COUNT = 3  # mantém até 3 arquivos antigos


def setup_logging(level: str = "INFO", log_dir: Path | None = None) -> None:
    """Configura onde e como os logs serão exibidos.

    Args:
        level: nível mínimo das mensagens (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_dir: pasta onde o arquivo de log será salvo. ``None`` desativa o arquivo.
    """
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()  # Evita mensagens duplicadas se for chamado duas vezes.

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_dir / LOG_FILE_NAME,
            maxBytes=MAX_LOG_BYTES,
            backupCount=BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # A biblioteca discord.py registra muitas mensagens de rede; mostramos só avisos.
    logging.getLogger("discord.http").setLevel(logging.WARNING)
