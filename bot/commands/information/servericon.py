"""Comando /servericon: mostra o ícone do servidor em tamanho grande."""

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import base_embed, info_embed


class ServerIcon(commands.Cog):
    """Cog que contém o /servericon."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="servericon", description="Mostra o ícone do servidor.")
    @app_commands.guild_only()
    async def servericon(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("Use este comando em um servidor.", ephemeral=True)
            return

        # Nem todo servidor tem ícone. Nesse caso, guild.icon é None.
        if guild.icon is None:
            await interaction.response.send_message(
                embed=info_embed("Este servidor ainda não tem um ícone."), ephemeral=True
            )
            return

        icon_url = guild.icon.with_size(1024).url
        embed = base_embed(f"🖼️ Ícone de {guild.name}")
        embed.set_image(url=icon_url)

        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Abrir imagem no navegador", url=icon_url))
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ServerIcon(bot))
