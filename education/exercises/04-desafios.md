# Desafios práticos

Projetos maiores, sem passo a passo. Planeje antes de codar ([Resolução de problemas](../programming-basics/05-resolucao-de-problemas.md)) e siga o [checklist de novas funcionalidades](../best-practices/05-checklist-de-novas-funcionalidades.md).

## Desafio D1 — /coinflip completo

- **Objetivo:** passar por **todo** o fluxo de contribuição do projeto.
- **Nível:** desafio (fácil)
- **Conteúdos necessários:** [Criando um novo comando](../discord-development/10-criando-um-novo-comando.md)
- **Arquivos envolvidos:** `bot/commands/fun/coinflip.py`, documentação, `help_menu.py`, testes, `CHANGELOG.md`

**Enunciado:** implemente `/coinflip` com um parâmetro opcional `aposta` (Cara ou Coroa). Se houver aposta, diga se a pessoa acertou. Inclua a documentação com as 18 seções, a entrada no `/help`, os testes e a linha no CHANGELOG.

**Resultado esperado:** `python -m pytest` passa; `/coinflip aposta:Cara` → "Deu Coroa. Não foi desta vez!".

➡️ [Solução](solucoes/04-desafios.md#solução-do-desafio-d1)

---

## Desafio D2 — /quiz com botões

- **Objetivo:** combinar JSON, views dinâmicas e validação de respostas.
- **Nível:** desafio (médio)
- **Conteúdos necessários:** [json](../libraries/json.md), [componentes](../discord-development/07-componentes.md), [views/poll](../code-explanation/views/poll.md)
- **Arquivos envolvidos:** `bot/data/quiz.json`, `bot/commands/fun/quiz.py`, `bot/views/quiz.py`, documentação e testes

**Enunciado:** o bot sorteia uma pergunta de programação de um JSON e mostra 4 alternativas em botões. Só quem usou o comando pode responder; ao responder, os botões são desativados, a resposta certa fica verde (`ButtonStyle.success`) e a escolhida errada, vermelha (`ButtonStyle.danger`).

**Dicas:** separe a lógica (carregar e validar perguntas, conferir a resposta) da view, como em `views/poll.py`.

➡️ [Solução](solucoes/04-desafios.md#solução-do-desafio-d2)

---

## Desafio D3 — Gerenciar lembretes

- **Objetivo:** estender o banco de dados com segurança.
- **Nível:** desafio (médio)
- **Conteúdos necessários:** [sqlite3](../libraries/sqlite3.md), [database/reminders](../code-explanation/database/reminders.md)
- **Arquivos envolvidos:** `bot/database/reminders.py`, `bot/commands/utility/remind.py` (ou um arquivo novo), testes e documentação

**Enunciado:** crie `/reminders` (lista os seus lembretes pendentes, *ephemeral*) e `/remind-cancel id:<número>` (cancela um lembrete **seu**). Ninguém pode cancelar o lembrete de outra pessoa.

**Dicas:** `DELETE FROM reminders WHERE id = ? AND user_id = ?` e `cursor.rowcount` dizem se algo foi apagado. Para isso, o `_execute` precisará devolver o `rowcount` também.

➡️ [Solução](solucoes/04-desafios.md#solução-do-desafio-d3)

---

## Desafio D4 — Refatorar a confirmação

- **Objetivo:** reduzir código duplicado sem mudar o comportamento.
- **Nível:** desafio (médio)
- **Conteúdos necessários:** [funções](../python/06-funcoes.md), [views/confirm](../code-explanation/views/confirm.md)
- **Arquivos envolvidos:** `bot/views/confirm.py`, `bot/commands/moderation/kick.py`, `bot/commands/moderation/ban.py` e as respectivas documentações

**Enunciado:** crie `async def confirm_action(interaction, description) -> bool | None` em `views/confirm.py`, que envia a confirmação, espera e devolve o resultado, editando a mensagem em caso de tempo esgotado ou cancelamento. Use-a no `/kick` e no `/ban`.

**Resultado esperado:** `kick.py` e `ban.py` ficam menores; o comportamento no Discord é idêntico; todos os testes passam.

➡️ [Solução](solucoes/04-desafios.md#solução-do-desafio-d4)
