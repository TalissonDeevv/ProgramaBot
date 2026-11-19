"""Menu de seleção do comando ``/help``.

Este é um exemplo de *view persistente*: ela usa ``timeout=None`` e um
``custom_id`` fixo. Assim, mesmo depois de o bot reiniciar, o menu enviado
em mensagens antigas continua funcionando (o registro é feito em
``ProgramaBot.setup_hook`` com ``bot.add_view(HelpView())``).
"""

import discord

from bot.utils.embeds import PRIMARY_COLOR, base_embed

HELP_SELECT_CUSTOM_ID = "programabot:help:select"

# Catálogo de comandos. Ao criar um comando novo, adicione-o aqui também:
# o teste tests/test_extensions.py avisa se algum comando ficar de fora.
HELP_CATEGORIES: dict[str, dict] = {
    "general": {
        "label": "Gerais",
        "emoji": "📚",
        "description": "Comandos básicos para conhecer o bot.",
        "commands": {
            "ping": "Mostra a latência do bot.",
            "help": "Mostra esta central de ajuda.",
            "about": "Informações sobre o projeto ProgramaBot.",
            "hello": "O bot te cumprimenta de acordo com o horário.",
            "calculator": "Calcula expressões matemáticas com segurança.",
        },
    },
    "information": {
        "label": "Informações",
        "emoji": "🔎",
        "description": "Consultas sobre membros e servidores.",
        "commands": {
            "avatar": "Mostra o avatar de um usuário.",
            "userinfo": "Mostra informações de um membro.",
            "serverinfo": "Mostra informações do servidor.",
            "servericon": "Mostra o ícone do servidor.",
        },
    },
    "utility": {
        "label": "Utilidades",
        "emoji": "🧰",
        "description": "Ferramentas do dia a dia.",
        "commands": {
            "embed": "Abre um formulário para criar um embed.",
            "poll": "Cria uma enquete com botões.",
            "say": "Faz o bot enviar uma mensagem (moderadores).",
            "remind": "Cria um lembrete para você.",
        },
    },
    "moderation": {
        "label": "Moderação",
        "emoji": "🛡️",
        "description": "Comandos que exigem permissões especiais.",
        "commands": {
            "clear": "Apaga mensagens recentes do canal.",
            "kick": "Expulsa um membro do servidor.",
            "ban": "Bane um membro do servidor.",
            "timeout": "Silencia um membro temporariamente.",
            "unban": "Remove o banimento de um usuário.",
        },
    },
    "fun": {
        "label": "Diversão",
        "emoji": "🎲",
        "description": "Comandos para descontrair (e estudar aleatoriedade).",
        "commands": {
            "dice": "Rola um ou mais dados.",
            "fact": "Mostra uma curiosidade sobre programação.",
        },
    },
}

PREFIX_EXAMPLES = "`!ping`, `!hello`, `!soma 2 3`"


def build_overview_embed() -> discord.Embed:
    """Embed inicial do /help, com o resumo das categorias."""
    embed = base_embed(
        "📖 Central de ajuda do ProgramaBot",
        "Escolha uma categoria no menu abaixo para ver os comandos.\n"
        "Cada comando tem o código-fonte explicado em `education/code-explanation/`.",
        PRIMARY_COLOR,
    )
    for data in HELP_CATEGORIES.values():
        embed.add_field(
            name=f"{data['emoji']} {data['label']}",
            value=f"{data['description']} ({len(data['commands'])} comandos)",
            inline=False,
        )
    embed.add_field(
        name="⌨️ Comandos de prefixo (exemplos educacionais)",
        value=PREFIX_EXAMPLES,
        inline=False,
    )
    return embed


def build_category_embed(category_key: str) -> discord.Embed:
    """Embed com a lista de comandos de uma categoria."""
    data = HELP_CATEGORIES[category_key]
    lines = [f"`/{name}` — {description}" for name, description in data["commands"].items()]
    return base_embed(f"{data['emoji']} {data['label']}", "\n".join(lines), PRIMARY_COLOR)


class HelpSelect(discord.ui.Select):
    """Menu suspenso com uma opção para cada categoria."""

    def __init__(self) -> None:
        options = [
            discord.SelectOption(
                label=data["label"],
                value=key,
                emoji=data["emoji"],
                description=data["description"],
            )
            for key, data in HELP_CATEGORIES.items()
        ]
        super().__init__(
            placeholder="Escolha uma categoria de comandos",
            options=options,
            min_values=1,
            max_values=1,
            custom_id=HELP_SELECT_CUSTOM_ID,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        """Chamado quando alguém escolhe uma opção do menu."""
        selected = self.values[0]
        await interaction.response.edit_message(embed=build_category_embed(selected))


class HelpView(discord.ui.View):
    """View persistente que contém o menu de categorias."""

    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.add_item(HelpSelect())
