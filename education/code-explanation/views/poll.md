# `bot/views/poll.py`: lógica e botões da enquete

## 1. Nome e localização

- **Arquivo:** `bot/views/poll.py`
- **Usado por:** [`commands/utility/poll.py`](../commands/utility/poll.md)

## 2. Finalidade

Implementar a enquete do `/poll`: interpretar as opções, contar votos (um por pessoa), desenhar barras de resultado e criar um botão para cada opção.

## 3. Por que foi criado

O arquivo mostra uma ideia importante de arquitetura: **separar a lógica da interface**.

- `parse_poll_options` e `PollState` são Python puro, sem nada do Discord, e por isso são fáceis de testar.
- `PollButton` e `PollView` cuidam só da parte visual e chamam a lógica.

## 4. Como se conecta ao restante do bot

```
commands/utility/poll.py
 ├─ parse_poll_options(opcoes)        → lista validada
 ├─ PollView(PollState(...), ...)     → botões
 ├─ view.build_embed()                → embed inicial
 └─ (depois do tempo) view.finish()   → resultado final
```

## 5. Bibliotecas utilizadas

- [`discord.py`](../../libraries/discord-py.md): botões, views e `format_dt`.
- [`dataclasses`](../../libraries/dataclasses.md): `@dataclass` e `field`.
- [`datetime`](../../libraries/datetime.md): horário de término.
- [`logging`](../../libraries/logging.md).

## 6. Importações

```python
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

import discord

from bot.utils.embeds import PRIMARY_COLOR, base_embed
```

## 7. Conceitos de Python utilizados

- **Sets** (`seen: set[str]`) para detectar repetições rapidamente.
- **Dicionários** para os votos: `{id_do_usuario: indice}`.
- **`dict.get`** para ler sem erro quando a chave não existe.
- **`del`** para remover uma chave.
- **`enumerate` e `zip`** para percorrer duas listas ao mesmo tempo.
- **`@property`**: `total_votes` é usado como atributo, mas é calculado na hora.
- **`field(default_factory=dict)`**: cada enquete ganha um dicionário **novo**. Usar `votes: dict = {}` faria todas as enquetes compartilharem o mesmo dicionário.
- **Multiplicação de strings/listas**: `"▓" * 3` → `"▓▓▓"`, e `[0] * 3` → `[0, 0, 0]`.
- **Generics**: `discord.ui.Button["PollView"]` avisa ao editor que `self.view` é uma `PollView`.

## 8. Variáveis e constantes

| Nome | Valor | Motivo |
|---|---|---|
| `MIN_OPTIONS` / `MAX_OPTIONS` | 2 / 5 | Uma enquete precisa de escolhas; 5 botões cabem em uma linha do Discord. |
| `MAX_OPTION_LENGTH` | 80 | Limite de texto de um botão no Discord. |
| `NUMBER_EMOJIS` | `1️⃣` ... `5️⃣` | Emoji de cada opção. |
| `BAR_SIZE` | 10 | Tamanho da barra de progresso. |

## 9. Funções e classes

| Nome | Responsabilidade |
|---|---|
| `parse_poll_options(raw_options)` | `"A; B; a"` → `["A", "B"]`, com validação. |
| `PollState.vote(user_id, option_index)` | Registra, troca ou remove um voto. Retorna `"added"`, `"changed"` ou `"removed"`. |
| `PollState.counts()` | Votos por opção. |
| `PollState.total_votes` | Total de votos. |
| `PollState.result_lines()` | Linhas com as barras. |
| `PollButton.callback(interaction)` | Clique em um botão. |
| `PollView.build_embed()` | Embed com o resultado. |
| `PollView.finish()` | Encerra a enquete. |

## 10. Parâmetros

- `raw_options`: texto digitado com as opções separadas por `;`.
- `user_id` / `option_index`: quem votou e em qual opção (começando em 0).
- `state`: o `PollState` da enquete.
- `author_name`: nome de quem criou.
- `duration`: um `timedelta` com a duração.

## 11. Métodos do discord.py utilizados

| Método | Explicação |
|---|---|
| `discord.ui.Button(label=, emoji=, style=)` | Cria um botão sem usar decorator, porque a quantidade de botões varia. |
| `self.view` | A view a que o botão pertence. |
| `interaction.response.edit_message(embed=)` | Atualiza o resultado na mensagem. |
| `interaction.followup.send(..., ephemeral=True)` | Segunda mensagem, depois da resposta. |
| `discord.utils.format_dt(dt, "R")` | Mostra "em 10 minutos" de forma relativa, no fuso de cada leitor. |
| `PartialMessage.edit(embed=, view=)` | Edita a mensagem usando o token do bot. |

## 12. Funcionamento do código

### Um voto por pessoa

```python
def vote(self, user_id: int, option_index: int) -> str:
    previous = self.votes.get(user_id)
    if previous == option_index:
        del self.votes[user_id]
        return "removed"
    self.votes[user_id] = option_index
    return "added" if previous is None else "changed"
```

Como o dicionário usa o ID como chave, cada pessoa só pode ter **um** voto. Votar de novo sobrescreve o anterior. Clicar na mesma opção remove o voto.

### Criando botões dinamicamente

```python
for index, option in enumerate(state.options):
    self.add_item(PollButton(index, option))
```

Cada botão guarda seu `index`. No callback, `view.state.vote(interaction.user.id, self.index)` sabe qual opção foi clicada.

### Por que `timeout=None` e `PartialMessage`?

O `timeout` de uma View conta o tempo **desde a última interação**. Cada voto reiniciaria o relógio e a enquete nunca terminaria no horário certo. Por isso, quem controla o fim é o comando, com `asyncio.sleep`.

Além disso, a mensagem original da interação só pode ser editada pelo *token da interação* durante **15 minutos**. Uma `PartialMessage` edita usando o token do bot, que não expira.

## 13. Fluxo de execução

```
clique no botão 2 ─► PollButton.callback
                      ├─ state.vote(user, 1)        → "added"
                      ├─ edit_message(build_embed()) → barras atualizadas
                      └─ followup "Voto registrado!" (só a pessoa vê)

fim do tempo ─► PollView.finish()
                 ├─ finished = True; stop()
                 ├─ desativa todos os botões
                 └─ message.edit(embed final, view desativada)
```

## 14. Exemplos práticos

A lógica funciona sem o Discord:

```python
from bot.views.poll import PollState, parse_poll_options

estado = PollState("Melhor linguagem?", parse_poll_options("Python; JS"))
estado.vote(1, 0)
estado.vote(2, 0)
estado.vote(3, 1)
print(estado.counts())          # [2, 1]
print("\n".join(estado.result_lines()))
```

## 15. Erros comuns

- **Votos somem quando o bot reinicia**: os votos ficam só na memória. Para guardá-los, seria necessário um banco de dados, como no [`/remind`](../database/reminders.md).
- **Botões "não funcionam" depois de reiniciar**: esta view não é persistente. Compare com o [`help_menu`](help_menu.md).
- **Mais de 25 botões**: o Discord limita uma view a 25 componentes (5 linhas de 5).

## 16. Como testar

```bash
python -m pytest tests/test_poll.py -v
```

## 17. Como modificar

- Para permitir até 10 opções, aumente `MAX_OPTIONS`, adicione mais emojis em `NUMBER_EMOJIS` e distribua os botões em duas linhas com `row=index // 5` no `PollButton`.
- Para mudar o desenho da barra, troque `"▓"` e `"░"` por `"🟩"` e `"⬜"`.

## 18. Desafio

Adicione um botão **"Encerrar"** que só o criador da enquete pode usar. Dicas: guarde o `author_id` na `PollView`, crie o botão com `@discord.ui.button` e, no callback, chame `await self.finish()`. Pense também em como avisar o comando `/poll`, que está esperando no `asyncio.sleep`, de que a enquete já acabou.
