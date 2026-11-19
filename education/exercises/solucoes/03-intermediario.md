# Soluções: nível intermediário

## Solução do exercício 10

`bot/commands/fun/counter.py`:

```python
"""Comando /contador: botão que conta cliques (exercício 10)."""

import discord
from discord import app_commands
from discord.ext import commands

COUNTER_TIMEOUT_SECONDS = 120


class CounterView(discord.ui.View):
    def __init__(self, author_id: int) -> None:
        super().__init__(timeout=COUNTER_TIMEOUT_SECONDS)
        self.author_id = author_id
        self.count = 0
        self.message: discord.InteractionMessage | None = None

    @discord.ui.button(label="Cliques: 0", style=discord.ButtonStyle.primary)
    async def click(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.count += 1
        button.label = f"Cliques: {self.count}"
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Zerar", style=discord.ButtonStyle.secondary)
    async def reset(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Só quem criou o contador pode zerar.", ephemeral=True)
            return
        self.count = 0
        self.click.label = "Cliques: 0"  # self.click é o objeto Button criado pelo decorator
        await interaction.response.edit_message(view=self)

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        if self.message is not None:
            try:
                await self.message.edit(view=self)
            except discord.HTTPException:
                pass  # a mensagem pode ter sido apagada


class Counter(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="contador", description="Cria um botão que conta cliques.")
    async def contador(self, interaction: discord.Interaction) -> None:
        view = CounterView(interaction.user.id)
        await interaction.response.send_message("Clique no botão!", view=view)
        view.message = await interaction.original_response()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Counter(bot))
```

**Comentários:**
- O estado (`self.count`) fica na **instância** da view, então cada `/contador` tem o seu próprio número.
- O `timeout` conta a partir da **última** interação: aqui, isso é exatamente o comportamento desejado ("2 minutos sem cliques"). Compare com a enquete, em que esse comportamento era um problema ([views/poll](../../code-explanation/views/poll.md#por-que-timeoutnone-e-partialmessage)).
- Guardar `InteractionMessage` funciona aqui porque o timeout é curto (o token da interação dura 15 minutos). Se cada clique mantiver a view viva por mais de 15 minutos no total, a edição final pode falhar, e por isso o `try/except`.
- Teste a parte sem Discord criando a view dentro de um teste `async def` e verificando `view.count` e `view.timeout`.

## Solução do exercício 11

Trechos de `bot/events/member_join.py`:

```python
def build_dm_text(guild_name: str) -> str:
    """Texto da mensagem direta de boas-vindas."""
    return (
        f"Olá! Boas-vindas ao **{guild_name}**! 🎉\n"
        "Algumas dicas para começar:\n"
        "• `/help`: veja todos os comandos\n"
        "• `/hello`: receba um cumprimento\n"
        "• `/fact`: aprenda uma curiosidade sobre programação"
    )


class MemberJoin(commands.Cog):
    ...

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        await self._send_dm(member)  # primeiro a DM: não depende do canal

        channel = get_welcome_channel(member.guild, self.bot.settings.welcome_channel_id)
        if channel is None:
            return
        ...  # (o envio no canal continua igual)

    async def _send_dm(self, member: discord.Member) -> None:
        try:
            await member.send(build_dm_text(member.guild.name))
        except discord.HTTPException:  # inclui Forbidden (DMs fechadas)
            logger.warning("Não foi possível enviar DM de boas-vindas para %s.", member)
```

Teste em `tests/test_command_helpers.py`:

```python
from bot.events.member_join import build_dm_text

def test_build_dm_text():
    text = build_dm_text("Servidor de Estudos")
    assert "Servidor de Estudos" in text
    assert "/help" in text
```

**Comentários:** separar o texto em `build_dm_text` permite testá-lo sem o Discord. Atualize também `education/code-explanation/events/member_join.md`.

## Solução do exercício 12

`bot/commands/moderation/slowmode.py`:

```python
"""Comando /slowmode: define o modo lento do canal (exercício 12)."""

from datetime import timedelta

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import error_embed, success_embed
from bot.utils.time_parser import format_duration

MAX_SLOWMODE_SECONDS = 21_600  # 6 horas, limite do Discord


class Slowmode(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="slowmode", description="Define o modo lento deste canal.")
    @app_commands.describe(segundos="Intervalo entre mensagens (0 desativa, máximo 21600).")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.checks.bot_has_permissions(manage_channels=True)
    async def slowmode(
        self,
        interaction: discord.Interaction,
        segundos: app_commands.Range[int, 0, MAX_SLOWMODE_SECONDS],
    ) -> None:
        channel = interaction.channel
        if not isinstance(channel, discord.TextChannel):
            await interaction.response.send_message(
                embed=error_embed("Use este comando em um canal de texto."), ephemeral=True
            )
            return

        await channel.edit(slowmode_delay=segundos, reason=f"/slowmode por {interaction.user}")

        if segundos == 0:
            message = "🐇 Modo lento desativado."
        else:
            message = f"🐢 Modo lento: uma mensagem a cada **{format_duration(timedelta(seconds=segundos))}**."
        await interaction.response.send_message(embed=success_embed(message))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Slowmode(bot))
```

Mudanças complementares:

```python
# bot/events/errors.py → PERMISSION_NAMES
"manage_channels": "Gerenciar canais",

# tests/test_extensions.py → EXPECTED_SLASH_COMMANDS e MODERATION_PERMISSIONS
"slowmode": "manage_channels",

# bot/views/help_menu.py → categoria "moderation"
"slowmode": "Define o modo lento do canal.",
```

**Comentários:**
- As três camadas de permissão (`default_permissions`, `has_permissions`, `bot_has_permissions`) funcionam juntas, como explicado em [Permissões](../../discord-development/08-permissoes.md).
- Reutilizar `format_duration` evita reescrever a formatação de tempo.
