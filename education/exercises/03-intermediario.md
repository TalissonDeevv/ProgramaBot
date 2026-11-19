# Exercícios: nível intermediário

## Exercício 10 — Criar um botão

- **Objetivo:** criar uma View com estado e um botão que se atualiza.
- **Nível:** intermediário
- **Conteúdos necessários:** [classes](../python/09-classes-e-objetos.md), [decorators](../python/10-decorators.md), [componentes](../discord-development/07-componentes.md)
- **Arquivos envolvidos:** novo `bot/commands/fun/counter.py` + documentação, catálogo e testes

**Enunciado:** crie o comando `/contador`, que envia uma mensagem com um botão `Cliques: 0`. Cada clique (de qualquer pessoa) soma 1 e atualiza o texto do botão. Adicione um segundo botão, **Zerar**, que só quem usou o comando pode apertar. Depois de 2 minutos sem cliques, os botões devem ser desativados.

**Dicas:**
- Guarde o contador em `self.count` dentro da View.
- Para mudar o texto: `button.label = f"Cliques: {self.count}"` e `await interaction.response.edit_message(view=self)`.
- Para desativar no fim: sobrescreva `async def on_timeout(self)` e edite a mensagem. Você vai precisar guardar a mensagem com `interaction.original_response()`.
- Para restringir o botão Zerar, compare `interaction.user.id` com o ID do autor **dentro do callback** (não use `interaction_check`, que bloquearia os dois botões).

**Resultado esperado:** o botão conta os cliques; Zerar responde com erro *ephemeral* para outras pessoas; tudo é desativado após 2 minutos sem uso.

➡️ [Solução](solucoes/03-intermediario.md#solução-do-exercício-10)

---

## Exercício 11 — Criar um evento de boas-vindas

- **Objetivo:** modificar um evento e tratar falhas de envio.
- **Nível:** intermediário
- **Conteúdos necessários:** [intents](../discord-development/02-intents.md), [member_join](../code-explanation/events/member_join.md), [exceções](../python/08-excecoes.md)
- **Arquivos envolvidos:** `bot/events/member_join.py` e `education/code-explanation/events/member_join.md`

**Enunciado:** além da mensagem no canal, o bot deve enviar uma **mensagem direta** ao novo membro com:
- boas-vindas com o nome do servidor;
- três dicas de comandos (`/help`, `/hello`, `/fact`).

Se a pessoa tiver as DMs fechadas, o bot deve apenas registrar um aviso no log, sem erro. A DM deve ser enviada **mesmo se** o servidor não tiver canal de boas-vindas.

**Dicas:**
- `await member.send(...)` lança `discord.Forbidden` se as DMs estiverem fechadas (e `Forbidden` é um tipo de `discord.HTTPException`).
- Hoje, o evento termina com `return` quando não há canal. Reorganize a ordem.
- Crie uma função auxiliar `build_dm_text(guild_name) -> str` e teste-a.

**Resultado esperado:** ao entrar no servidor com uma conta de teste, a DM chega; com DMs fechadas, aparece um `WARNING` no log.

➡️ [Solução](solucoes/03-intermediario.md#solução-do-exercício-11)

---

## Exercício 12 — Criar um comando com permissões

- **Objetivo:** proteger um comando com as permissões do usuário e do bot.
- **Nível:** intermediário
- **Conteúdos necessários:** [permissões](../discord-development/08-permissoes.md), [tratamento de erros](../code-explanation/events/errors.md)
- **Arquivos envolvidos:** novo `bot/commands/moderation/slowmode.py` + documentação, catálogo e testes; `bot/events/errors.py` (tradução da permissão)

**Enunciado:** crie `/slowmode segundos:<0-21600>`, que define o **modo lento** do canal de texto atual (0 desativa). Requisitos:
- só funciona em servidores e em canais de texto;
- exige "Gerenciar canais" (`manage_channels`) de quem usa **e** do bot;
- fica escondido de quem não tem a permissão;
- responde com uma mensagem que diga a duração por extenso (reutilize `format_duration`).

**Dicas:**
- `await channel.edit(slowmode_delay=segundos)`.
- 21600 segundos = 6 horas, o limite do Discord.
- Adicione `"manage_channels": "Gerenciar canais"` em `PERMISSION_NAMES`.
- Adicione o comando em `MODERATION_PERMISSIONS` no `tests/test_extensions.py` para testar as permissões automaticamente.

**Resultado esperado:** um membro sem permissão não vê o comando; se conseguir usá-lo (por configuração do servidor), recebe "Você precisa da permissão: Gerenciar canais".

➡️ [Solução](solucoes/03-intermediario.md#solução-do-exercício-12)
