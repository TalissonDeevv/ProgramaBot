"""Comando /avatar: mostra a foto de perfil de um usuário."""

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import base_embed


class Avatar(commands.Cog):
    """Cog que contém o /avatar."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="avatar", description="Mostra o avatar de um usuário.")
    @app_commands.describe(usuario="Usuário que você quer ver (deixe vazio para ver o seu).")
    async def avatar(
        self,
        interaction: discord.Interaction,
        usuario: discord.User | None = None,
    ) -> None:
        target = usuario or interaction.user
        # display_avatar sempre existe: se a pessoa não tem foto, vem o avatar padrão do Discord.
        avatar_url = target.display_avatar.url

        embed = base_embed(f"🖼️ Avatar de {target.display_name}")
        embed.set_image(url=avatar_url)

        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Abrir imagem no navegador", url=avatar_url))
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Avatar(bot))
