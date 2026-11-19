# Soluções: nível básico

## Solução do exercício 5

```python
numero = 7
for multiplicador in range(1, 11):
    print(f"{numero} x {multiplicador} = {numero * multiplicador}")

contador = 10
while contador >= 1:
    print(contador)
    contador -= 1
print("Bot online!")

soma = 0
for par in range(2, 101, 2):   # começa em 2 e anda de 2 em 2 até 100
    soma += par
print("Soma dos pares:", soma)  # 2550
```

**Comentários:** `range(2, 101, 2)` gera só os pares, sem precisar de `if`. A alternativa com `if numero % 2 == 0` também está correta.

## Solução do exercício 6

```python
usuarios = [
    {"nome": "Ana", "cargo": "Moderador", "mensagens": 120},
    {"nome": "Bruno", "cargo": "Membro", "mensagens": 45},
    {"nome": "Carla", "cargo": "Membro", "mensagens": 300},
]

usuarios.append({"nome": "Diego", "cargo": "Membro", "mensagens": 80})

nomes = [usuario["nome"] for usuario in usuarios]
print("Usuários:", ", ".join(nomes))

ativos = [usuario["nome"] for usuario in usuarios if usuario["mensagens"] > 100]
print("Mais de 100 mensagens:", ", ".join(ativos))

total = sum(usuario["mensagens"] for usuario in usuarios)
print("Total de mensagens:", total)

mais_ativo = max(usuarios, key=lambda usuario: usuario["mensagens"])
print("Mais ativo:", mais_ativo["nome"])
```

**Comentários:**
- Cada usuário é um dicionário; a lista guarda vários dicionários. Esse formato é muito parecido com o JSON que APIs devolvem.
- `key=lambda usuario: usuario["mensagens"]` diz ao `max` **o que** comparar. `lambda` é uma função pequena, sem nome.

## Solução do exercício 7

`bot/commands/fun/ola.py`:

```python
"""Comando /ola: exercício 7 da trilha."""

import discord
from discord import app_commands
from discord.ext import commands


class Ola(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ola", description="Diz olá para você.")
    @app_commands.describe(nome="Como você quer ser chamado (opcional).")
    async def ola(self, interaction: discord.Interaction, nome: str | None = None) -> None:
        name = nome or interaction.user.display_name
        await interaction.response.send_message(
            f"Olá, {name}!",
            allowed_mentions=discord.AllowedMentions.none(),  # @everyone não notifica ninguém
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ola(bot))
```

Depois:

1. Em `bot/views/help_menu.py`, na categoria `"fun"`: `"ola": "Diz olá para você.",`
2. Em `tests/test_extensions.py`, adicione `"ola"` em `EXPECTED_SLASH_COMMANDS`.
3. Crie `education/code-explanation/commands/fun/ola.md` (copie a estrutura de `hello.md`).
4. `python -m pytest`.

**Comentários:** os testes falham, de propósito, até que os três passos acima sejam feitos. É assim que o projeto garante que nenhum comando fique sem documentação.

## Solução do exercício 8

Trecho alterado em `bot/commands/general/ping.py`:

```python
import time

# ... dentro da classe Ping:
    @app_commands.command(name="ping", description="Mostra a latência (tempo de resposta) do bot.")
    async def ping(self, interaction: discord.Interaction) -> None:
        latency_ms = round(self.bot.latency * 1000)
        embed = info_embed(f"🏓 Pong!\nQualidade: {latency_status(latency_ms)}", title="Ping")
        embed.add_field(name="Gateway", value=f"{latency_ms} ms")

        start = time.perf_counter()
        await interaction.response.send_message(embed=embed)
        api_ms = round((time.perf_counter() - start) * 1000)

        embed.add_field(name="API", value=f"{api_ms} ms")
        await interaction.edit_original_response(embed=embed)
```

**Comentários:**
- `time.perf_counter()` é o relógio mais preciso para medir intervalos curtos.
- A primeira resposta precisa acontecer em até 3 segundos; a edição pode vir depois.
- Lembre-se de atualizar `education/code-explanation/commands/general/ping.md` (seções 5, 6, 11, 12 e 13) e de documentar o módulo `time`, criando `education/libraries/time.md`, conforme o [checklist](../../best-practices/05-checklist-de-novas-funcionalidades.md).

## Solução do exercício 9

`bot/commands/fun/perfil.py`:

```python
"""Comando /perfil: cartão de estudante (exercício 9)."""

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import base_embed

LEVELS = [
    app_commands.Choice(name="Iniciante", value="iniciante"),
    app_commands.Choice(name="Básico", value="basico"),
    app_commands.Choice(name="Intermediário", value="intermediario"),
]


class Perfil(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="perfil", description="Mostra o seu cartão de estudante.")
    @app_commands.describe(nivel="Seu nível atual.", linguagem="Sua linguagem favorita.")
    @app_commands.choices(nivel=LEVELS)
    async def perfil(
        self,
        interaction: discord.Interaction,
        nivel: app_commands.Choice[str],
        linguagem: app_commands.Range[str, 1, 30] = "Python",
    ) -> None:
        user = interaction.user
        embed = base_embed(f"🎓 Cartão de estudante de {user.display_name}")
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="Membro desde", value=discord.utils.format_dt(user.created_at, "R"))
        embed.add_field(name="Linguagem favorita", value=linguagem)
        embed.add_field(name="Nível", value=nivel.name)
        await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions.none())


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Perfil(bot))
```

**Comentários:**
- Parâmetros obrigatórios precisam vir **antes** dos opcionais, por isso `nivel` vem primeiro.
- `nivel.name` é o texto exibido; `nivel.value` é o valor interno.
- Complete com o `/help`, os testes e a documentação, como no exercício 7.
