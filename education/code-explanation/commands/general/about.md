# `bot/commands/general/about.py`: o comando /about

## 1. Nome e localização

- **Arquivo:** `bot/commands/general/about.py`
- **Comando:** `/about`

## 2. Finalidade

Apresentar o projeto: versão, versão do discord.py, mantenedor, número de servidores e licença, com **botões de link** para o GitHub e para a trilha de estudos.

## 3. Por que foi criado

Para divulgar o projeto open source e mostrar o tipo mais simples de componente: o **botão de link**, que abre uma URL e não precisa de código para tratar o clique.

## 4. Como se conecta ao restante do bot

Importa metadados de [`bot/__init__.py`](../../pacotes-e-init.md):

```python
from bot import REPOSITORY_URL, __maintainer__, __version__
```

Assim, ao mudar a versão em um único lugar, o `/about` se atualiza sozinho.

## 5. Bibliotecas utilizadas

- [`discord.py`](../../../libraries/discord-py.md).

## 6. Importações

```python
import discord
from discord import app_commands
from discord.ext import commands

from bot import REPOSITORY_URL, __maintainer__, __version__
from bot.utils.embeds import base_embed
```

## 7. Conceitos de Python utilizados

- Constantes compostas com f-string (`DOCS_URL`).
- Funções que constroem e retornam objetos (`build_about_view`).
- Verificação de `None` (`if self.bot.user is not None`).
- `len()` para contar servidores e `str()` para converter número em texto.

## 8. Variáveis e constantes

- `DOCS_URL = f"{REPOSITORY_URL}/tree/main/education"`: link para a pasta de educação no GitHub.
- `embed`, `view`: a resposta.

## 9. Funções

- `build_about_view()`: cria a view com dois botões de link.
- `About.about(interaction)`: o comando.
- `setup(bot)`.

## 10. Parâmetros

- `interaction`: a interação do comando.

## 11. Métodos utilizados

| Método/atributo | Explicação |
|---|---|
| `discord.ui.View()` | View sem subclasse, usada só como "caixa" de componentes. |
| `discord.ui.Button(label=, url=, emoji=)` | Com `url`, o botão vira automaticamente um botão de link (`ButtonStyle.link`). |
| `view.add_item(botao)` | Coloca o botão na view. |
| `embed.add_field(name=, value=)` | Adiciona um campo. Por padrão, `inline=True` (lado a lado). |
| `embed.set_thumbnail(url=)` | Imagem pequena no canto superior direito. |
| `discord.__version__` | Versão instalada do discord.py. |
| `self.bot.guilds` | Lista de servidores em que o bot está. |
| `self.bot.user.display_avatar.url` | Avatar do próprio bot. |

## 12. Funcionamento do código

```python
def build_about_view() -> discord.ui.View:
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Código no GitHub", url=REPOSITORY_URL, emoji="💻"))
    view.add_item(discord.ui.Button(label="Trilha de estudos", url=DOCS_URL, emoji="📚"))
    return view
```

Botões de link não geram interação: o Discord abre o site diretamente. Por isso não há callback.

```python
if self.bot.user is not None:
    embed.set_thumbnail(url=self.bot.user.display_avatar.url)
```

`bot.user` é `None` antes do login. Durante um comando o bot sempre está logado, mas a verificação deixa o código seguro e satisfaz o verificador de tipos do editor.

## 13. Fluxo de execução

```
/about → monta embed (versão, discord.py, mantenedor, servidores, licença)
       → build_about_view()
       → send_message(embed, view)
```

## 14. Exemplos práticos

Adicionar um botão para a documentação oficial do discord.py:

```python
view.add_item(discord.ui.Button(label="discord.py", url="https://discordpy.readthedocs.io/en/stable/"))
```

## 15. Erros comuns

- **URL inválida** (sem `https://`) gera `HTTPException` ao enviar.
- **Botão de link com `custom_id`**: não é permitido; botões de link usam só `url`.

## 16. Como testar

Use `/about` e clique nos dois botões.

## 17. Como modificar

Se você fizer um *fork* do projeto, troque `REPOSITORY_URL` em `bot/__init__.py` pela URL do seu repositório.

## 18. Desafio

Mostre há quanto tempo o bot está online (*uptime*). Dicas: guarde `datetime.now(timezone.utc)` em um atributo no `__init__` do `ProgramaBot` (`self.started_at`) e use `discord.utils.format_dt(self.bot.started_at, "R")` em um novo campo do embed.
