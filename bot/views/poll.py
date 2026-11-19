"""Enquete com botões, usada pelo comando ``/poll``.

O arquivo está dividido em duas partes:

1. ``PollState`` e ``parse_poll_options``: lógica pura (sem Discord), fácil de testar.
2. ``PollButton`` e ``PollView``: a parte visual, com os botões do Discord.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

import discord

from bot.utils.embeds import PRIMARY_COLOR, base_embed

logger = logging.getLogger(__name__)

MIN_OPTIONS = 2
MAX_OPTIONS = 5
MAX_OPTION_LENGTH = 80  # limite de caracteres do texto de um botão
NUMBER_EMOJIS = ("1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣")
BAR_SIZE = 10


class PollError(ValueError):
    """Erro de validação das opções da enquete."""


def parse_poll_options(raw_options: str) -> list[str]:
    """Transforma ``"Python; JavaScript; Java"`` em ``["Python", "JavaScript", "Java"]``.

    Remove espaços extras, opções vazias e opções repetidas.

    Raises:
        PollError: se houver menos de 2 ou mais de 5 opções, ou alguma for longa demais.
    """
    options: list[str] = []
    seen: set[str] = set()
    for part in raw_options.split(";"):
        option = part.strip()
        if option and option.lower() not in seen:
            options.append(option)
            seen.add(option.lower())

    if len(options) < MIN_OPTIONS:
        raise PollError(
            f"Informe pelo menos {MIN_OPTIONS} opções diferentes, separadas por ponto e vírgula. "
            "Exemplo: Python; JavaScript"
        )
    if len(options) > MAX_OPTIONS:
        raise PollError(f"A enquete pode ter no máximo {MAX_OPTIONS} opções.")
    for option in options:
        if len(option) > MAX_OPTION_LENGTH:
            raise PollError(f"Cada opção pode ter no máximo {MAX_OPTION_LENGTH} caracteres.")
    return options


@dataclass
class PollState:
    """Guarda a pergunta, as opções e o voto de cada pessoa."""

    question: str
    options: list[str]
    # Dicionário {id_do_usuario: indice_da_opcao}. Cada pessoa tem um único voto.
    votes: dict[int, int] = field(default_factory=dict)

    def vote(self, user_id: int, option_index: int) -> str:
        """Registra um voto e retorna o que aconteceu: ``added``, ``changed`` ou ``removed``.

        Clicar de novo na mesma opção remove o voto.
        """
        if not 0 <= option_index < len(self.options):
            raise IndexError("Opção de enquete inexistente.")

        previous = self.votes.get(user_id)
        if previous == option_index:
            del self.votes[user_id]
            return "removed"
        self.votes[user_id] = option_index
        return "added" if previous is None else "changed"

    def counts(self) -> list[int]:
        """Quantidade de votos de cada opção, na mesma ordem de ``options``."""
        totals = [0] * len(self.options)
        for option_index in self.votes.values():
            totals[option_index] += 1
        return totals

    @property
    def total_votes(self) -> int:
        return len(self.votes)

    def result_lines(self) -> list[str]:
        """Linhas de texto com uma barra de progresso para cada opção."""
        lines = []
        total = self.total_votes
        for index, (option, count) in enumerate(zip(self.options, self.counts())):
            percentage = (count / total * 100) if total else 0
            filled = round(percentage / 100 * BAR_SIZE)
            bar = "▓" * filled + "░" * (BAR_SIZE - filled)
            word = "voto" if count == 1 else "votos"
            lines.append(
                f"{NUMBER_EMOJIS[index]} **{option}**\n`{bar}` {count} {word} ({percentage:.0f}%)"
            )
        return lines


class PollButton(discord.ui.Button["PollView"]):
    """Um botão para cada opção da enquete."""

    def __init__(self, index: int, label: str) -> None:
        super().__init__(label=label, emoji=NUMBER_EMOJIS[index], style=discord.ButtonStyle.secondary)
        self.index = index

    async def callback(self, interaction: discord.Interaction) -> None:
        view = self.view
        if view is None:
            return
        status = view.state.vote(interaction.user.id, self.index)
        await interaction.response.edit_message(embed=view.build_embed())

        feedback = {
            "added": "Voto registrado!",
            "changed": "Voto alterado!",
            "removed": "Voto removido.",
        }[status]
        await interaction.followup.send(feedback, ephemeral=True)


class PollView(discord.ui.View):
    """Reúne os botões da enquete e controla quando ela termina."""

    def __init__(self, state: PollState, author_name: str, duration: timedelta) -> None:
        # timeout=None: quem encerra a enquete é o comando /poll, depois da duração escolhida.
        super().__init__(timeout=None)
        self.state = state
        self.author_name = author_name
        self.ends_at = datetime.now(timezone.utc) + duration
        self.finished = False
        # Preenchido pelo comando depois que a mensagem é enviada.
        self.message: discord.PartialMessage | None = None

        for index, option in enumerate(state.options):
            self.add_item(PollButton(index, option))

    def build_embed(self) -> discord.Embed:
        """Cria o embed com o resultado atual da enquete."""
        status = "Encerrada" if self.finished else f"Termina {discord.utils.format_dt(self.ends_at, 'R')}"
        embed = base_embed(f"📊 {self.state.question}", "\n\n".join(self.state.result_lines()), PRIMARY_COLOR)
        embed.add_field(name="Total de votos", value=str(self.state.total_votes))
        embed.add_field(name="Status", value=status)
        embed.add_field(name="Criada por", value=self.author_name)
        return embed

    async def finish(self) -> None:
        """Encerra a enquete: desativa os botões e mostra o resultado final."""
        self.finished = True
        self.stop()
        for item in self.children:
            item.disabled = True
        if self.message is None:
            return
        try:
            await self.message.edit(embed=self.build_embed(), view=self)
        except discord.HTTPException:
            logger.warning("Não foi possível atualizar a enquete encerrada (a mensagem foi apagada?).")
