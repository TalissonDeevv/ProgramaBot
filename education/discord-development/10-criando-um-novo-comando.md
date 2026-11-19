# 10. Criando um novo comando (passo a passo)

Vamos criar o comando `/coinflip` (cara ou coroa) seguindo **todas** as regras do projeto.

## Passo 1: escolha a categoria e crie o arquivo

Categorias existentes: `general`, `information`, `utility`, `moderation`, `fun`. Cara ou coroa é diversão:

```
bot/commands/fun/coinflip.py
```

> Uma categoria nova (`bot/commands/estudos/`) também precisa de um `__init__.py`.

## Passo 2: escreva o código

Use o modelo [`examples/commands/meu_comando.py`](../../examples/commands/meu_comando.py) como ponto de partida:

```python
"""Comando /coinflip: joga uma moeda."""

import random

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import base_embed

SIDES = ("Cara", "Coroa")


def flip_coin() -> str:
    """Lógica separada: fácil de testar."""
    return random.choice(SIDES)


class Coinflip(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="coinflip", description="Joga uma moeda: cara ou coroa.")
    async def coinflip(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(embed=base_embed("🪙 Cara ou coroa?", f"Deu **{flip_coin()}**!"))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Coinflip(bot))
```

Regras:

- nome do comando em minúsculas, sem espaços, até 32 caracteres;
- descrição de até 100 caracteres;
- **todo parâmetro com `@app_commands.describe`**;
- validação dos parâmetros (`Range`, verificações no código);
- permissões, se o comando for sensível;
- `AllowedMentions.none()` ao reenviar texto de usuários.

## Passo 3: adicione ao `/help`

Em [`bot/views/help_menu.py`](../code-explanation/views/help_menu.md), na categoria `"fun"`:

```python
"coinflip": "Joga uma moeda: cara ou coroa.",
```

## Passo 4: crie a explicação

Crie `education/code-explanation/commands/fun/coinflip.md` com as 18 seções. Use uma página existente como modelo, por exemplo [`dice.md`](../code-explanation/commands/fun/dice.md).

## Passo 5: teste

Em `tests/test_extensions.py`, adicione `"coinflip"` em `EXPECTED_SLASH_COMMANDS`. Crie um teste para a lógica:

```python
from bot.commands.fun.coinflip import SIDES, flip_coin

def test_flip_coin():
    for _ in range(20):
        assert flip_coin() in SIDES
```

Rode:

```bash
python -m pytest
```

Os testes do projeto avisam se você esqueceu algo:

| Teste | Falha quando |
|---|---|
| `test_every_python_file_has_documentation` | falta o `.md` do arquivo |
| `test_help_catalog_matches_registered_commands` | o comando não está no `/help` |
| `test_expected_commands_are_registered` | o comando não foi registrado ou não está na lista esperada |
| `test_commands_have_descriptions` | falta `describe` em algum parâmetro |

## Passo 6: teste no Discord

Reinicie o bot (com `GUILD_ID` configurado, o comando aparece na hora) e use `/coinflip`.

## Passo 7: registre a mudança

Adicione uma linha no [CHANGELOG](../../CHANGELOG.md), na seção "Não lançado":

```markdown
### Adicionado
- Comando `/coinflip` (cara ou coroa).
```

## ✅ Checklist

- [ ] Arquivo em `bot/commands/<categoria>/`
- [ ] Cog + função `setup`
- [ ] Parâmetros com `describe` e validação
- [ ] Permissões (se necessário)
- [ ] Entrada no `HELP_CATEGORIES`
- [ ] Explicação em `education/code-explanation/`
- [ ] Testes atualizados e passando (`python -m pytest`)
- [ ] Testado no Discord
- [ ] Linha no `CHANGELOG.md`
- [ ] Bibliotecas novas documentadas em `education/libraries/` (se houver)

Esse checklist também está no [CONTRIBUTING.md](../../CONTRIBUTING.md).
