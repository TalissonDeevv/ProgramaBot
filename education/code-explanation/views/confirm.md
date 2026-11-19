# `bot/views/confirm.py`: botões de confirmação

## 1. Nome e localização

- **Arquivo:** `bot/views/confirm.py`
- **Usado por:** [`/kick`](../commands/moderation/kick.md) e [`/ban`](../commands/moderation/ban.md)

## 2. Finalidade

Mostrar os botões **Confirmar** e **Cancelar** e guardar a escolha do usuário, para que o comando decida o que fazer depois.

## 3. Por que foi criado

Expulsar ou banir alguém por engano é desagradável. Uma etapa de confirmação é uma prática comum de **experiência do usuário** em ações destrutivas. Como dois comandos precisam disso, a view fica em um arquivo próprio e reutilizável.

## 4. Como se conecta ao restante do bot

```python
view = ConfirmView(author_id=interaction.user.id)
await interaction.response.send_message(embed=..., view=view, ephemeral=True)
await view.wait()
if view.confirmed: ...
```

## 5. Bibliotecas utilizadas

- [`discord.py`](../../libraries/discord-py.md): `discord.ui.View`, `discord.ui.button` e `discord.ButtonStyle`.

## 6. Importações

```python
import discord
```

## 7. Conceitos de Python utilizados

- **Herança**: `ConfirmView(discord.ui.View)`.
- **Decorators com argumentos**: `@discord.ui.button(label=..., style=...)`.
- **Atributos com três estados**: `bool | None`, em que `None` significa "ainda sem resposta".
- **Métodos assíncronos** e **métodos sobrescritos** (`interaction_check`).
- **Reutilização**: `_finish` concentra o código comum aos dois botões.

## 8. Variáveis e atributos

- `CONFIRM_TIMEOUT_SECONDS = 30`: depois de 30 segundos sem clique, a view expira.
- `self.author_id`: quem pode clicar.
- `self.confirmed`: `None` → `True` ou `False`.

## 9. Funções e métodos

| Método | Quando é chamado |
|---|---|
| `__init__(author_id, timeout)` | Ao criar a view. |
| `interaction_check(interaction)` | Pelo discord.py, **antes** de qualquer clique ser processado. |
| `_finish(interaction, confirmed)` | Pelos dois botões, para encerrar. |
| `confirm(interaction, button)` | Clique em "Confirmar". |
| `cancel(interaction, button)` | Clique em "Cancelar". |

## 10. Parâmetros

- `author_id`: ID de quem executou o comando.
- `timeout`: segundos até expirar (padrão 30).
- `interaction`: a interação do **clique** (diferente da interação do comando).
- `button`: o objeto do botão clicado. O discord.py sempre passa esse argumento.

## 11. Métodos do discord.py utilizados

| Método | Explicação |
|---|---|
| `super().__init__(timeout=...)` | Inicializa a `View` com tempo limite. |
| `@discord.ui.button(...)` | Transforma o método em um botão da view. |
| `discord.ButtonStyle.danger` / `.secondary` | Botão vermelho / cinza. |
| `interaction.response.edit_message(view=self)` | Atualiza a mensagem com os botões desativados. Também serve como resposta ao clique. |
| `self.children` | Lista de componentes da view. |
| `item.disabled = True` | Desativa o botão. |
| `self.stop()` | Encerra a view e libera quem está esperando em `view.wait()`. |
| `await view.wait()` | Espera até `stop()` ser chamado **ou** o tempo acabar. |

## 12. Funcionamento do código

```python
async def interaction_check(self, interaction: discord.Interaction) -> bool:
    if interaction.user.id != self.author_id:
        await interaction.response.send_message("Apenas quem executou o comando pode responder.", ephemeral=True)
        return False
    return True
```

Se o método retornar `False`, o discord.py **não** chama o botão. A mensagem do `/kick` já é *ephemeral* (só o autor vê), mas esta verificação deixa a view segura mesmo se for reutilizada em uma mensagem pública.

```python
async def _finish(self, interaction, confirmed: bool) -> None:
    self.confirmed = confirmed
    for item in self.children:
        item.disabled = True
    await interaction.response.edit_message(view=self)
    self.stop()
```

Todo clique precisa de uma resposta em até 3 segundos, senão o Discord mostra "Esta interação falhou". Aqui, a resposta é a própria edição da mensagem.

## 13. Fluxo de execução

```
/kick → envia mensagem com ConfirmView → await view.wait() (o comando "pausa")
                                              │
usuário clica "Confirmar" ─► interaction_check ─► confirm ─► _finish ─► stop()
                                              │
comando continua ◄──────────────────────────────┘ view.confirmed == True → kick
(ou: 30 s sem clique → timeout → wait() termina com confirmed == None)
```

## 14. Exemplos práticos

Reutilize a view em qualquer comando:

```python
view = ConfirmView(interaction.user.id, timeout=15)
await interaction.response.send_message("Apagar seus lembretes?", view=view, ephemeral=True)
await view.wait()
if view.confirmed:
    ...
```

## 15. Erros comuns

- **"Esta interação falhou"**: o botão não respondeu à interação. Todo callback precisa chamar `interaction.response...`.
- **O comando nunca continua**: você esqueceu `self.stop()` e o comando fica esperando até o `timeout`.
- **`InteractionResponded`**: tentou usar `interaction.response` duas vezes. Depois da primeira resposta, use `interaction.followup` ou `edit_original_response`.

## 16. Como testar

Execute `/kick` em um servidor de testes com uma conta secundária. Teste três caminhos: confirmar, cancelar e esperar 30 segundos.

## 17. Como modificar

- Mude os textos com `label="Sim"` e `label="Não"`.
- Para mudar a cor do botão de confirmação para verde, use `discord.ButtonStyle.success`.

## 18. Desafio

Adicione um parâmetro `confirm_label: str = "Confirmar"` ao `__init__` e use-o para alterar o texto do botão. Dica: decorators são aplicados na criação da classe, então você precisará mudar o texto dentro do `__init__`, com `self.confirm.label = confirm_label`.

Mais sobre componentes: [discord-development/07-componentes.md](../../discord-development/07-componentes.md).
