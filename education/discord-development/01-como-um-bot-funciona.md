# 01. Como um bot do Discord funciona

## As peças

| Peça | O que é |
|---|---|
| **Aplicação** | O "cadastro" do seu bot no [Discord Developer Portal](https://discord.com/developers/applications). Tem nome, ícone e um ID (*Application ID*). |
| **Usuário bot** | A "conta" do bot, que aparece nos servidores. |
| **Token** | A **senha** do bot. Quem tiver o token controla o bot. Nunca compartilhe. |
| **Seu código** | O programa (o ProgramaBot) que roda no **seu** computador ou em um servidor e usa o token para se conectar. |

Um ponto importante: **o bot não roda dentro do Discord.** Ele roda onde você executar `python -m bot.main`. Se você fechar o terminal, o bot fica offline.

## Dois canais de comunicação

```
                 ┌────────────── Gateway (WebSocket) ──────────────┐
                 │  conexão sempre aberta; o Discord ENVIA eventos  │
  Discord  ◄─────┤                                                  ├────►  ProgramaBot
                 │  API REST (HTTP); o bot PEDE ações               │
                 └──────────────────────────────────────────────────┘
```

- **Gateway**: o Discord avisa o bot sobre acontecimentos em tempo real (*eventos*): "mensagem criada", "membro entrou", "alguém usou /ping".
- **API REST**: o bot faz pedidos: "envie esta mensagem", "bana este usuário".

O discord.py esconde esses detalhes. `await channel.send("oi")` vira uma requisição HTTP; `on_member_join` é chamado quando chega um evento pelo gateway.

## O ciclo de vida do ProgramaBot

```
python -m bot.main
 1. lê o .env (token, configurações)
 2. login com o token (API)
 3. setup_hook: carrega comandos e eventos; sincroniza os slash commands
 4. conecta ao gateway, informando as intents
 5. on_ready: "pronto!"
 6. fica esperando eventos... (para sempre, até Ctrl+C)
```

## O que acontece quando alguém usa `/ping`

1. A pessoa digita `/ping` no Discord.
2. O Discord envia um evento **INTERACTION_CREATE** pelo gateway.
3. O discord.py encontra o comando `ping` na `CommandTree` e chama `Ping.ping(interaction)`.
4. O código calcula a latência e chama `interaction.response.send_message(...)`.
5. Isso vira uma requisição HTTP para a API.
6. A resposta aparece no Discord.

Tudo isso precisa acontecer em até **3 segundos**. Veja [Interações e respostas](05-interacoes-e-respostas.md).

## Limites de requisição (*rate limits*)

O Discord limita quantas requisições um bot pode fazer por segundo. Se o bot exagerar, o Discord manda esperar. O discord.py respeita esses limites automaticamente, mas evite loops que enviam muitas mensagens.

## No ProgramaBot

- Configuração e token: [config.md](../code-explanation/config.md)
- Ciclo de vida: [main.md](../code-explanation/main.md)
- Evento `on_ready`: [ready.md](../code-explanation/events/ready.md)

## Exercício

Desenhe, no papel, o caminho completo de um clique no botão "Confirmar" do `/kick`: do clique até a mensagem "foi expulso(a)". Indique quais passos usam o gateway e quais usam a API REST.

Documentação oficial do Discord: <https://discord.com/developers/docs/intro>
