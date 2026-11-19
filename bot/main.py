"""Ponto de entrada do ProgramaBot.

Para iniciar o bot, abra o terminal na pasta do projeto e execute:

    python -m bot.main

Este arquivo cria o bot, carrega todos os comandos e eventos e conecta ao Discord.
"""

import asyncio
import logging
from pathlib import Path

import discord
from discord.ext import commands

from bot import __version__
from bot.config import PROJECT_ROOT, ConfigError, Settings, load_settings
from bot.utils.logger import setup_logging
from bot.views.help_menu import HelpView

logger = logging.getLogger(__name__)

# Pasta bot/ (onde este arquivo está).
BOT_PACKAGE_DIR = Path(__file__).resolve().parent

# Pastas dentro de bot/ que contêm extensões (arquivos com a função setup).
EXTENSION_FOLDERS = ("commands", "events")


def discover_extensions(base_dir: Path = BOT_PACKAGE_DIR) -> list[str]:
    """Procura automaticamente todos os arquivos de comandos e eventos.

    Transforma caminhos como ``bot/commands/general/ping.py`` em nomes de
    módulo como ``bot.commands.general.ping``, que é o formato aceito por
    ``load_extension``. Arquivos que começam com ``_`` (como ``__init__.py``)
    são ignorados.
    """
    extensions: list[str] = []
    for folder in EXTENSION_FOLDERS:
        for file in sorted((base_dir / folder).rglob("*.py")):
            if file.name.startswith("_"):
                continue
            relative_path = file.relative_to(base_dir.parent).with_suffix("")
            extensions.append(".".join(relative_path.parts))
    return extensions


def build_intents(settings: Settings) -> discord.Intents:
    """Define quais tipos de evento o bot quer receber do Discord."""
    intents = discord.Intents.default()
    # Intents privilegiadas: precisam ser ativadas também no Developer Portal.
    intents.members = settings.enable_members_intent
    intents.message_content = settings.enable_message_content_intent
    return intents


class ProgramaBot(commands.Bot):
    """O bot em si. Herda tudo de ``commands.Bot`` e adiciona nossas configurações."""

    def __init__(self, settings: Settings) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or(settings.prefix),
            intents=build_intents(settings),
            help_command=None,  # Usamos o nosso próprio /help.
            activity=discord.Game(name="/help | aprendendo Python"),
        )
        self.settings = settings

    async def setup_hook(self) -> None:
        """Executado uma única vez, antes de o bot se conectar ao Discord."""
        for extension in discover_extensions():
            try:
                await self.load_extension(extension)
                logger.info("Extensão carregada: %s", extension)
            except commands.ExtensionError:
                # Um arquivo com erro não derruba o bot inteiro.
                logger.exception("Falha ao carregar a extensão %s", extension)

        # View persistente: continua funcionando mesmo depois de reiniciar o bot.
        self.add_view(HelpView())

        if self.settings.sync_commands:
            await self.sync_application_commands()

    async def sync_application_commands(self) -> None:
        """Envia a lista de slash commands para o Discord."""
        if self.settings.guild_id:
            # Sincronizar em um servidor específico é instantâneo: ideal para testes.
            guild = discord.Object(id=self.settings.guild_id)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            logger.info("%d slash commands sincronizados no servidor %s.", len(synced), guild.id)
        else:
            synced = await self.tree.sync()
            logger.info(
                "%d slash commands sincronizados globalmente (podem levar alguns minutos para aparecer).",
                len(synced),
            )


async def run_bot() -> None:
    """Carrega as configurações, prepara os logs e mantém o bot conectado."""
    settings = load_settings()
    setup_logging(settings.log_level, PROJECT_ROOT / "logs")
    logger.info("Iniciando ProgramaBot %s (discord.py %s)", __version__, discord.__version__)

    bot = ProgramaBot(settings)
    async with bot:
        await bot.start(settings.token)


def main() -> None:
    """Executa o bot e transforma erros comuns em mensagens fáceis de entender."""
    try:
        asyncio.run(run_bot())
    except ConfigError as error:
        print(f"[Erro de configuração] {error}")
        raise SystemExit(1) from None
    except discord.LoginFailure:
        logger.error(
            "O Discord recusou o token. Gere um novo token no Developer Portal "
            "(aba Bot > Reset Token) e atualize o arquivo .env."
        )
        raise SystemExit(1) from None
    except discord.PrivilegedIntentsRequired:
        logger.error(
            "As intents privilegiadas não estão ativadas. No Developer Portal, abra a aba "
            "Bot e ative SERVER MEMBERS INTENT e MESSAGE CONTENT INTENT, ou desative-as no .env."
        )
        raise SystemExit(1) from None
    except KeyboardInterrupt:
        logger.info("Bot encerrado pelo usuário (Ctrl+C).")


if __name__ == "__main__":
    main()
