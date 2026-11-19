# `bot/commands/general/help.py`: o comando /help

## 1. Nome e localização

- **Arquivo:** `bot/commands/general/help.py`
- **Comando:** `/help`

## 2. Finalidade

Mostrar a central de ajuda: um embed com as categorias e um menu de seleção para ver os comandos de cada uma. A resposta é *ephemeral* (só quem pediu vê).

## 3. Por que foi criado

Todo bot precisa de um jeito de o usuário descobrir o que ele faz. O discord.py tem um `!help` automático para comandos de prefixo, mas ele não lista slash commands. Por isso o desativamos (`help_command=None` no `main.py`) e criamos o nosso.

## 4. Como se conecta ao restante do bot

Este arquivo é pequeno de propósito. Tudo o que é visual está em [`views/help_menu.py`](../../views/help_menu.md):

```python
from bot.views.help_menu import HelpView, build_overview_embed
```

## 5. Bibliotecas utilizadas

- [`discord.py`](../../../libraries/discord-py.md).

## 6. Importações

```python
import discord
from discord import app_commands
from discord.ext import commands

from bot.views.help_menu import HelpView, build_overview_embed
```

## 7. Conceitos de Python utilizados

- **Importação de funções e classes de outro módulo do projeto.**
- **Separação de responsabilidades**: o comando decide *quando* responder; a view decide *como* a resposta aparece.
- **Argumentos nomeados** (`embed=`, `view=`, `ephemeral=`).

## 8. Variáveis

Não há variáveis locais; os objetos são criados direto na chamada.

## 9. Funções

- `Help.help(interaction)`: o comando.
- `setup(bot)`: registra o Cog.

## 10. Parâmetros

- `interaction`: a interação do `/help`.

## 11. Métodos utilizados

| Método | Explicação |
|---|---|
| `build_overview_embed()` | Monta o embed com as categorias. |
| `HelpView()` | Cria a view com o menu. |
| `send_message(embed=, view=, ephemeral=True)` | Responde com embed **e** componentes, visível só para o usuário. |

## 12. Funcionamento do código

```python
@app_commands.command(name="help", description="Mostra todos os comandos do ProgramaBot.")
async def help(self, interaction: discord.Interaction) -> None:
    await interaction.response.send_message(
        embed=build_overview_embed(),
        view=HelpView(),
        ephemeral=True,
    )
```

O método se chama `help`, o mesmo nome da função nativa `help()` do Python. Dentro da classe isso não causa problema, porque o método é acessado como `self.help`. Mesmo assim, evite nomes iguais aos de funções nativas em variáveis comuns.

## 13. Fluxo de execução

```
/help → Help.help → send_message(overview + HelpView, ephemeral)
usuário escolhe categoria → HelpSelect.callback (help_menu.py) → edita o embed
```

## 14. Exemplos práticos

Para deixar o `/help` público, troque `ephemeral=True` por `ephemeral=False` (ou remova o argumento).

## 15. Erros comuns

- **Comando criado, mas fora do `/help`**: adicione-o em `HELP_CATEGORIES`. O teste `test_help_catalog_matches_registered_commands` avisa quando isso acontece.

## 16. Como testar

```bash
python -m pytest tests/test_extensions.py -k help -v
```

## 17. Como modificar

Adicione um parâmetro opcional `categoria` com escolhas fixas, para abrir direto em uma categoria:

```python
@app_commands.choices(categoria=[
    app_commands.Choice(name=data["label"], value=key) for key, data in HELP_CATEGORIES.items()
])
async def help(self, interaction, categoria: app_commands.Choice[str] | None = None): ...
```

## 18. Desafio

Implemente a modificação acima. Quando `categoria` for informada, envie `build_category_embed(categoria.value)` em vez do resumo. Não esqueça do `@app_commands.describe(categoria=...)`, porque o teste exige descrição em todos os parâmetros.
