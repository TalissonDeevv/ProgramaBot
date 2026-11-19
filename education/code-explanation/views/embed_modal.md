# `bot/views/embed_modal.py`: o formulário do /embed

## 1. Nome e localização

- **Arquivo:** `bot/views/embed_modal.py`
- **Usado por:** [`commands/utility/embed.py`](../commands/utility/embed.md)

## 2. Finalidade

Definir um **modal**, uma janela de formulário do Discord, com três campos (título, descrição e cor). Quando o usuário envia, o bot publica um embed com esse conteúdo.

## 3. Por que foi criado

Textos longos com várias linhas são desconfortáveis de digitar como parâmetro de slash command. O modal oferece uma caixa de texto grande (`TextStyle.paragraph`) e validação de tamanho feita pelo próprio Discord.

## 4. Como se conecta ao restante do bot

```
/embed (embed.py) → interaction.response.send_modal(EmbedModal())
usuário preenche e envia → EmbedModal.on_submit → parse_hex_color (utils/embeds.py) → envia o embed
```

## 5. Bibliotecas utilizadas

- [`discord.py`](../../libraries/discord-py.md): `discord.ui.Modal`, `discord.ui.TextInput`, `discord.TextStyle`.
- [`logging`](../../libraries/logging.md): registra erros inesperados.

## 6. Importações

```python
import logging

import discord

from bot.utils.embeds import error_embed, parse_hex_color
```

## 7. Conceitos de Python utilizados

- **Atributos de classe**: os campos são declarados direto no corpo da classe, não no `__init__`.
- **Argumentos de classe**: `class EmbedModal(discord.ui.Modal, title="Criar um embed")`. O `title=` é passado para a classe-mãe no momento da definição da classe.
- **`try/except` com `as error`**: captura a exceção e usa a mensagem dela.
- **`return` antecipado** depois de responder com erro.

## 8. Variáveis e atributos

| Atributo | Tipo | Detalhes |
|---|---|---|
| `titulo` | `TextInput` curto | obrigatório, até 256 caracteres |
| `descricao` | `TextInput` parágrafo | obrigatório, até 2000 caracteres |
| `cor` | `TextInput` curto | opcional (`required=False`), até 7 caracteres |

Depois do envio, o texto digitado fica em `self.titulo.value`, `self.descricao.value` e `self.cor.value`.

## 9. Métodos

- **`on_submit(interaction)`**: chamado quando o formulário é enviado.
- **`on_error(interaction, error)`**: chamado se `on_submit` lançar uma exceção não tratada.

## 10. Parâmetros

- `interaction`: a interação do envio do modal. Ela precisa ser respondida, assim como a de um comando.
- `error`: a exceção que aconteceu.

## 11. Métodos do discord.py utilizados

| Método | Explicação |
|---|---|
| `discord.ui.TextInput(label=, style=, placeholder=, required=, max_length=)` | Um campo do formulário. |
| `discord.TextStyle.paragraph` | Caixa de várias linhas. |
| `discord.Embed(title=, description=, color=)` | Cria o embed. |
| `embed.set_author(name=, icon_url=)` | Mostra quem criou o embed, com a foto. |
| `interaction.user.display_avatar.url` | URL do avatar de quem enviou. |
| `discord.AllowedMentions.none()` | Impede que o conteúdo marque pessoas, cargos ou @everyone. |
| `interaction.response.is_done()` | Indica se a interação já foi respondida. |

## 12. Funcionamento do código

```python
async def on_submit(self, interaction: discord.Interaction) -> None:
    try:
        color = parse_hex_color(self.cor.value)
    except ValueError as error:
        await interaction.response.send_message(embed=error_embed(str(error)), ephemeral=True)
        return
```

Se a cor for inválida, mostramos o erro só para o usuário (`ephemeral=True`) e paramos com `return`.

```python
await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions.none())
```

**Segurança:** qualquer pessoa pode usar `/embed`. Sem `AllowedMentions.none()`, alguém poderia escrever `@everyone` na descrição e notificar o servidor inteiro.

O `on_error` usa `is_done()` para escolher entre `response.send_message` (ainda não respondeu) e `followup.send` (já respondeu).

## 13. Fluxo de execução

```
/embed → send_modal(EmbedModal())
        → o Discord mostra o formulário
usuário clica "Enviar"
        → on_submit
            ├─ cor inválida → mensagem de erro ephemeral → fim
            └─ cria o embed → envia no canal
        (exceção inesperada → on_error → log + mensagem)
```

## 14. Exemplos práticos

Um formulário simples de feedback:

```python
class FeedbackModal(discord.ui.Modal, title="Envie seu feedback"):
    texto = discord.ui.TextInput(label="O que achou do bot?", style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Obrigado pelo feedback!", ephemeral=True)
```

## 15. Erros comuns

- **Um modal pode ter no máximo 5 campos.**
- **Não é possível abrir um modal depois de usar `defer()`**. O modal precisa ser a primeira resposta à interação.
- **`label` com mais de 45 caracteres** gera erro.

## 16. Como testar

Use `/embed`. Teste uma cor válida (`#FF0000`), uma inválida (`vermelho`) e o campo vazio.

## 17. Como modificar

Adicione um quarto campo, `imagem`, opcional, com uma URL. Se ele for preenchido, chame `embed.set_image(url=self.imagem.value)`.

## 18. Desafio

Valide se a URL da imagem começa com `https://`. Se não começar, mostre uma mensagem de erro *ephemeral*, como fizemos com a cor.
