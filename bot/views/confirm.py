"""View com botões "Confirmar" e "Cancelar".

Usada pelos comandos de moderação (``/kick`` e ``/ban``) para evitar que um
moderador expulse ou bana alguém por engano.
"""

import discord

CONFIRM_TIMEOUT_SECONDS = 30


class ConfirmView(discord.ui.View):
    """Pergunta "tem certeza?" e guarda a resposta em ``self.confirmed``.

    ``confirmed`` começa como ``None`` (ninguém respondeu). Depois de um clique,
    vira ``True`` (confirmou) ou ``False`` (cancelou).
    """

    def __init__(self, author_id: int, timeout: float = CONFIRM_TIMEOUT_SECONDS) -> None:
        super().__init__(timeout=timeout)
        self.author_id = author_id
        self.confirmed: bool | None = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Só quem executou o comando pode clicar nos botões."""
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "Apenas quem executou o comando pode responder.", ephemeral=True
            )
            return False
        return True

    async def _finish(self, interaction: discord.Interaction, confirmed: bool) -> None:
        """Registra a resposta, desativa os botões e encerra a view."""
        self.confirmed = confirmed
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()  # Libera quem está esperando em view.wait().

    @discord.ui.button(label="Confirmar", style=discord.ButtonStyle.danger, emoji="✔️")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self._finish(interaction, confirmed=True)

    @discord.ui.button(label="Cancelar", style=discord.ButtonStyle.secondary, emoji="✖️")
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self._finish(interaction, confirmed=False)
