"""Modal (formulário) usado pelo comando ``/embed``.

Um *modal* é uma janela que abre por cima do Discord com campos de texto.
Quando o usuário clica em "Enviar", o método ``on_submit`` é chamado.
"""

import logging

import discord

from bot.utils.embeds import error_embed, parse_hex_color

logger = logging.getLogger(__name__)


class EmbedModal(discord.ui.Modal, title="Criar um embed"):
    """Formulário com título, descrição e cor do embed."""

    # Cada TextInput declarado na classe vira um campo do formulário.
    titulo = discord.ui.TextInput(
        label="Título",
        placeholder="Ex.: Aviso importante",
        max_length=256,
    )
    descricao = discord.ui.TextInput(
        label="Descrição",
        style=discord.TextStyle.paragraph,
        placeholder="Escreva o conteúdo do embed...",
        max_length=2000,
    )
    cor = discord.ui.TextInput(
        label="Cor em hexadecimal (opcional)",
        placeholder="#5865F2",
        required=False,
        max_length=7,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        """Executado quando o usuário envia o formulário."""
        try:
            color = parse_hex_color(self.cor.value)
        except ValueError as error:
            await interaction.response.send_message(embed=error_embed(str(error)), ephemeral=True)
            return

        embed = discord.Embed(
            title=self.titulo.value,
            description=self.descricao.value,
            color=color,
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url,
        )
        # AllowedMentions.none() impede que o texto marque @everyone ou cargos.
        await interaction.response.send_message(
            embed=embed, allowed_mentions=discord.AllowedMentions.none()
        )

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        """Executado se acontecer um erro inesperado dentro de ``on_submit``."""
        logger.exception("Erro no formulário de embed", exc_info=error)
        message = error_embed("Não consegui criar o embed. Tente novamente.")
        if interaction.response.is_done():
            await interaction.followup.send(embed=message, ephemeral=True)
        else:
            await interaction.response.send_message(embed=message, ephemeral=True)
