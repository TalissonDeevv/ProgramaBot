# `bot/views/help_menu.py`: o menu do /help (view persistente)

## 1. Nome e localização

- **Arquivo:** `bot/views/help_menu.py`
- **Usado por:** [`commands/general/help.py`](../commands/general/help.md) e [`main.py`](../main.md), que registra a view persistente

## 2. Finalidade

- Guardar o **catálogo** de todos os slash commands, organizado por categoria.
- Criar os embeds da central de ajuda.
- Oferecer um **menu de seleção** (*select menu*) que troca a categoria exibida.

## 3. Por que foi criado

Separar a parte visual (view e embeds) do comando deixa o `help.py` pequeno. Além disso, a view precisa ser importada pelo `main.py` para ser registrada como **persistente**, o que fica mais organizado quando ela tem um arquivo próprio.

## 4. Como se conecta ao restante do bot

- `help.py` envia `build_overview_embed()` com `HelpView()`.
- `main.py` chama `bot.add_view(HelpView())` no `setup_hook`.
- `tests/test_extensions.py` compara `HELP_CATEGORIES` com os comandos registrados. **Se você criar um comando e esquecer de colocá-lo aqui, o teste falha.**

## 5. Bibliotecas utilizadas

- [`discord.py`](../../libraries/discord-py.md): `discord.ui.Select`, `discord.ui.View`, `discord.SelectOption`.

## 6. Importações

```python
import discord

from bot.utils.embeds import PRIMARY_COLOR, base_embed
```

## 7. Conceitos de Python utilizados

- **Dicionários aninhados**: `HELP_CATEGORIES["general"]["commands"]["ping"]`.
- **Compreensão de listas**: monta as opções do menu e as linhas do embed.
- **`len()`** e iteração com `.items()` e `.values()`.
- **Herança** de `discord.ui.Select` e `discord.ui.View`.
- **Type hint de dicionário**: `dict[str, dict]`.

## 8. Variáveis e constantes

| Nome | Explicação |
|---|---|
| `HELP_SELECT_CUSTOM_ID` | `"programabot:help:select"`, um identificador fixo. É obrigatório para views persistentes. |
| `HELP_CATEGORIES` | O catálogo: chave da categoria → rótulo, emoji, descrição e comandos. |
| `PREFIX_EXAMPLES` | Texto com os comandos de prefixo de exemplo. |

## 9. Funções e classes

| Nome | O que faz |
|---|---|
| `build_overview_embed()` | Embed inicial com um campo por categoria. |
| `build_category_embed(category_key)` | Embed com os comandos de uma categoria. |
| `HelpSelect` | O menu suspenso. |
| `HelpSelect.callback(interaction)` | Chamado quando alguém escolhe uma opção. |
| `HelpView` | A view que contém o menu, com `timeout=None`. |

## 10. Parâmetros

- `category_key`: uma chave de `HELP_CATEGORIES` (`"general"`, `"utility"`...).
- `interaction`: a interação da escolha no menu.

## 11. Métodos do discord.py utilizados

| Método | Explicação |
|---|---|
| `discord.SelectOption(label=, value=, emoji=, description=)` | Uma opção do menu. `value` é o que o código recebe; `label` é o que o usuário vê. |
| `discord.ui.Select(placeholder=, options=, min_values=, max_values=, custom_id=)` | O menu. `min_values=1, max_values=1` = escolher exatamente uma opção. |
| `self.values` | Lista com os `value` escolhidos. |
| `interaction.response.edit_message(embed=...)` | Troca o embed da mensagem que contém o menu. |
| `self.add_item(item)` | Adiciona um componente à view. |
| `view.is_persistent()` | `True` se a view tiver `timeout=None` e todos os componentes tiverem `custom_id`. |

## 12. Funcionamento do código

### Views persistentes

Normalmente uma view "morre" quando o bot reinicia: o objeto Python deixa de existir e os cliques passam a falhar. Uma view persistente resolve isso:

1. `timeout=None`: a view nunca expira.
2. Todo componente tem um `custom_id` fixo.
3. Ao iniciar, o bot chama `bot.add_view(HelpView())`. Quando chega um clique com o `custom_id` `programabot:help:select`, o discord.py sabe que deve usar esta view.

Isso só funciona porque o callback **não depende de estado guardado em memória**: ele usa apenas `self.values[0]` e o catálogo fixo.

### O callback

```python
async def callback(self, interaction: discord.Interaction) -> None:
    selected = self.values[0]
    await interaction.response.edit_message(embed=build_category_embed(selected))
```

Não passamos `view=` no `edit_message`, então o Discord mantém o menu que já está na mensagem.

### Montando opções com compreensão de lista

```python
options = [
    discord.SelectOption(label=data["label"], value=key, emoji=data["emoji"], description=data["description"])
    for key, data in HELP_CATEGORIES.items()
]
```

## 13. Fluxo de execução

```
bot inicia → setup_hook → add_view(HelpView())     (registra o custom_id)
/help      → envia overview + HelpView
usuário escolhe "Moderação" → HelpSelect.callback
             └─ edit_message(build_category_embed("moderation"))
bot reinicia → o menu na mensagem antiga continua funcionando
```

## 14. Exemplos práticos

Adicionando uma categoria nova:

```python
"study": {
    "label": "Estudos",
    "emoji": "📝",
    "description": "Ferramentas para estudar.",
    "commands": {"pomodoro": "Inicia um timer pomodoro."},
},
```

## 15. Erros comuns

- **`ValueError` ao chamar `add_view`**: algum componente está sem `custom_id`, ou a view tem `timeout` diferente de `None`.
- **Mais de 25 opções**: o Discord limita um select a 25 opções.
- **`description` longa demais**: cada opção aceita até 100 caracteres de descrição.

## 16. Como testar

```bash
python -m pytest tests/test_extensions.py -k help -v
```

No Discord: use `/help`, escolha categorias, reinicie o bot e escolha outra categoria na **mesma** mensagem.

## 17. Como modificar

Sempre que criar um comando, adicione-o em `HELP_CATEGORIES`. Se quiser um texto de ajuda mais longo, crie uma chave `"details"` e mostre-a em `build_category_embed`.

## 18. Desafio

Hoje o catálogo é escrito à mão. Tente gerá-lo automaticamente: percorra `interaction.client.tree.get_commands()` e use `command.name` e `command.description`. Pense em como descobrir a categoria de cada comando (dica: `type(command.binding).__module__` mostra o módulo do Cog). Qual abordagem é mais fácil de entender para um iniciante?
