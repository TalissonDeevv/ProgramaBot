# 🔬 Explicação do código-fonte

Esta pasta explica **cada arquivo Python** da pasta [`bot/`](../../bot). A estrutura aqui é um espelho da estrutura do código:

| Arquivo de código | Explicação |
|---|---|
| `bot/main.py` | [main.md](main.md) |
| `bot/config.py` | [config.md](config.md) |
| `bot/commands/general/ping.py` | [commands/general/ping.md](commands/general/ping.md) |
| `bot/events/member_join.py` | [events/member_join.md](events/member_join.md) |
| `bot/utils/embeds.py` | [utils/embeds.md](utils/embeds.md) |

> Regra do projeto: **nenhum arquivo Python fica sem explicação**. O teste `tests/test_project_structure.py` falha se alguém criar um arquivo em `bot/` sem criar o `.md` correspondente aqui.

## Como cada explicação está organizada

Todas as páginas seguem as mesmas 18 seções, então você sempre sabe onde procurar:

1. Nome e localização · 2. Finalidade · 3. Por que foi criado · 4. Como se conecta ao restante do bot · 5. Bibliotecas utilizadas · 6. Importações · 7. Conceitos de Python · 8. Variáveis e constantes · 9. Funções · 10. Parâmetros · 11. Métodos utilizados · 12. Funcionamento do código · 13. Fluxo de execução · 14. Exemplos práticos · 15. Erros comuns · 16. Como testar · 17. Como modificar · 18. Desafio

## Ordem de leitura sugerida

Se você está começando, leia nesta ordem. Cada arquivo usa ideias dos anteriores.

1. **Fundação**
   - [pacotes-e-init.md](pacotes-e-init.md): o que são os arquivos `__init__.py`
   - [config.md](config.md): como o bot lê o `.env`
   - [utils/logger.md](utils/logger.md): como os logs funcionam
   - [main.md](main.md): como o bot liga e carrega tudo
2. **Primeiros comandos**
   - [utils/embeds.md](utils/embeds.md)
   - [commands/general/ping.md](commands/general/ping.md): o comando mais simples
   - [commands/general/hello.md](commands/general/hello.md): parâmetros opcionais e condicionais
   - [commands/general/about.md](commands/general/about.md): botões de link
   - [commands/general/prefix_examples.md](commands/general/prefix_examples.md): comandos de prefixo
3. **Lógica separada do Discord**
   - [utils/calculator.md](utils/calculator.md) → [commands/general/calculator.md](commands/general/calculator.md)
   - [utils/time_parser.md](utils/time_parser.md)
   - [commands/fun/dice.md](commands/fun/dice.md) e [commands/fun/fact.md](commands/fun/fact.md)
4. **Informações do Discord**
   - [commands/information/avatar.md](commands/information/avatar.md)
   - [commands/information/userinfo.md](commands/information/userinfo.md)
   - [commands/information/serverinfo.md](commands/information/serverinfo.md)
   - [commands/information/servericon.md](commands/information/servericon.md)
5. **Componentes interativos**
   - [views/help_menu.md](views/help_menu.md) → [commands/general/help.md](commands/general/help.md)
   - [views/embed_modal.md](views/embed_modal.md) → [commands/utility/embed.md](commands/utility/embed.md)
   - [views/poll.md](views/poll.md) → [commands/utility/poll.md](commands/utility/poll.md)
   - [views/confirm.md](views/confirm.md)
6. **Eventos**
   - [events/ready.md](events/ready.md)
   - [events/member_join.md](events/member_join.md) e [events/member_remove.md](events/member_remove.md)
   - [events/message.md](events/message.md)
   - [events/errors.md](events/errors.md)
7. **Permissões e moderação**
   - [commands/utility/say.md](commands/utility/say.md)
   - [utils/moderation.md](utils/moderation.md)
   - [commands/moderation/clear.md](commands/moderation/clear.md)
   - [commands/moderation/kick.md](commands/moderation/kick.md) e [commands/moderation/ban.md](commands/moderation/ban.md)
   - [commands/moderation/timeout.md](commands/moderation/timeout.md) e [commands/moderation/unban.md](commands/moderation/unban.md)
8. **Banco de dados e tarefas em segundo plano**
   - [database/reminders.md](database/reminders.md) → [commands/utility/remind.md](commands/utility/remind.md)

Antes de ler as explicações, é bom ter visto pelo menos o básico de Python em [`education/python/`](../python).
