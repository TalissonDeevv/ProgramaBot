# 05. Interações e respostas

## O que é uma interação?

Uma **interação** é criada quando alguém usa um slash command, clica em um botão, escolhe uma opção de menu ou envia um modal. No discord.py, ela chega como um objeto `discord.Interaction`.

## A regra dos 3 segundos

Toda interação precisa receber uma **primeira resposta em até 3 segundos**. Senão, o Discord mostra "O aplicativo não respondeu" e a interação expira.

Depois da primeira resposta, o *token* da interação vale por **15 minutos** para mensagens adicionais e edições.

## Formas de responder (a primeira resposta)

Escolha **uma**:

| Método | Quando usar | Exemplo no projeto |
|---|---|---|
| `response.send_message(...)` | Responder com uma mensagem | quase todos os comandos |
| `response.defer(...)` | A resposta vai demorar mais de 3 s | [`/clear`](../code-explanation/commands/moderation/clear.md) |
| `response.edit_message(...)` | Responder a um clique editando a mensagem | [botões](../code-explanation/views/confirm.md), [menu do /help](../code-explanation/views/help_menu.md) |
| `response.send_modal(...)` | Abrir um formulário | [`/embed`](../code-explanation/commands/utility/embed.md) |

Usar `interaction.response` duas vezes gera o erro `InteractionResponded`.

## Depois da primeira resposta

| Método | O que faz | Exemplo |
|---|---|---|
| `interaction.followup.send(...)` | Envia mais mensagens | [`/poll`](../code-explanation/views/poll.md) ("Voto registrado!") |
| `interaction.edit_original_response(...)` | Edita a primeira resposta | [`/kick`](../code-explanation/commands/moderation/kick.md) |
| `interaction.original_response()` | Busca a mensagem da primeira resposta | [`/poll`](../code-explanation/commands/utility/poll.md) |
| `interaction.response.is_done()` | Indica se a interação já foi respondida | [`errors.py`](../code-explanation/events/errors.md) |

## Mensagens ephemeral

```python
await interaction.response.send_message("Só você vê isto.", ephemeral=True)
```

Uma mensagem *ephemeral* aparece só para quem usou o comando, com o aviso "Somente você pode ver esta mensagem". Use para erros, confirmações e informações pessoais.

## Padrão com defer

```python
await interaction.response.defer(ephemeral=True, thinking=True)  # "pensando..."
resultado = await algo_demorado()
await interaction.followup.send(f"Pronto: {resultado}", ephemeral=True)
```

## Dados úteis da interação

| Atributo | Conteúdo |
|---|---|
| `interaction.user` | Quem interagiu (`Member` em servidores, `User` em DMs) |
| `interaction.guild` / `guild_id` | O servidor (`None` em DMs) |
| `interaction.channel` / `channel_id` | O canal |
| `interaction.command` | O comando usado |
| `interaction.client` | O bot |

## Exercício

1. Crie um comando `/espera` que use `defer`, espere 5 segundos com `asyncio.sleep` e responda com `followup.send`.
2. Agora remova o `defer` e veja o que acontece. Por quê?

Documentação: <https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.Interaction>
