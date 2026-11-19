# 07. Componentes: botões, menus de seleção e modais

## Views

Componentes ficam dentro de uma **View** (`discord.ui.View`). A view:

- guarda os componentes (até 25, em até 5 linhas);
- define o **tempo limite** (`timeout`, padrão 180 segundos **desde a última interação**);
- permite filtrar quem pode usar (`interaction_check`);
- é enviada junto com a mensagem: `send_message(..., view=minha_view)`.

## Botões

**Com callback** (usando decorator):

```python
class MinhaView(discord.ui.View):
    @discord.ui.button(label="Clique", style=discord.ButtonStyle.primary)
    async def clicar(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.send_message("Clicou!", ephemeral=True)
```

**Criados dinamicamente** (quando a quantidade varia), como na [enquete](../code-explanation/views/poll.md):

```python
class OpcaoButton(discord.ui.Button):
    async def callback(self, interaction): ...

view.add_item(OpcaoButton(label="Opção 1"))
```

**De link** (abrem um site; sem callback), como no [`/about`](../code-explanation/commands/general/about.md):

```python
view.add_item(discord.ui.Button(label="GitHub", url="https://github.com"))
```

Estilos: `primary` (azul), `secondary` (cinza), `success` (verde), `danger` (vermelho), `link`.

## Menus de seleção

```python
class MeuMenu(discord.ui.Select):
    def __init__(self):
        super().__init__(options=[
            discord.SelectOption(label="Python", value="py"),
            discord.SelectOption(label="JavaScript", value="js"),
        ])

    async def callback(self, interaction):
        await interaction.response.send_message(f"Você escolheu {self.values[0]}")
```

Existem também menus prontos de usuário, cargo e canal (`discord.ui.UserSelect`, `RoleSelect`, `ChannelSelect`).

No projeto: [`help_menu.py`](../code-explanation/views/help_menu.md).

## Modais (formulários)

```python
class Formulario(discord.ui.Modal, title="Cadastro"):
    nome = discord.ui.TextInput(label="Nome")

    async def on_submit(self, interaction):
        await interaction.response.send_message(f"Olá, {self.nome.value}!")

await interaction.response.send_modal(Formulario())
```

No projeto: [`embed_modal.py`](../code-explanation/views/embed_modal.md).

## Esperando uma resposta

```python
view = ConfirmView(autor_id)
await interaction.response.send_message("Tem certeza?", view=view)
await view.wait()          # até view.stop() ou timeout
if view.confirmed: ...
```

No projeto: [`confirm.py`](../code-explanation/views/confirm.md).

## Views persistentes

Uma view comum para de funcionar quando o bot reinicia. Para criar uma **persistente**:

1. `super().__init__(timeout=None)`;
2. todo componente com `custom_id` fixo;
3. `bot.add_view(MinhaView())` no `setup_hook`.

No projeto: o menu do `/help` ([`help_menu.py`](../code-explanation/views/help_menu.md)).

## Erros comuns

| Erro | Causa |
|---|---|
| "Esta interação falhou" | O callback não respondeu à interação |
| Botões param de funcionar após 3 minutos | `timeout` padrão de 180 s |
| `InteractionResponded` | Duas respostas na mesma interação |

## Exercício

Resolva o [exercício 10](../exercises/03-intermediario.md#exercício-10--criar-um-botão): um botão "contador" que mostra quantas vezes foi clicado.

Documentação: <https://discordpy.readthedocs.io/en/stable/interactions/api.html#bot-ui-kit> e exemplos oficiais em <https://github.com/Rapptz/discord.py/tree/master/examples/views>
