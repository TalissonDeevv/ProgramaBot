# Changelog

Todas as mudanças relevantes do ProgramaBot são registradas neste arquivo.

O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/), e o projeto adota o [Versionamento Semântico](https://semver.org/lang/pt-BR/):

- **MAJOR** (`2.0.0`): mudanças incompatíveis (ex.: renomear uma variável do `.env`, remover um comando);
- **MINOR** (`1.1.0`): funcionalidades novas e compatíveis;
- **PATCH** (`1.1.1`): correções.

Categorias usadas em cada versão: **Adicionado**, **Alterado**, **Corrigido**, **Removido**, **Documentação**, **Segurança** e **Mudanças incompatíveis**.

Novas mudanças entram primeiro em **[Não lançado]**. Quando o mantenedor publica uma versão, os itens são movidos para uma seção com o número e a data.

## [Não lançado]

Conteúdo previsto para a primeira versão estável, **1.0.0**. A versão atual do código é `1.0.0-dev` (`bot/__init__.py`).

### Adicionado

- Estrutura modular do bot: `bot/main.py` (com carregamento automático de extensões), `bot/config.py` (leitura e validação do `.env`), `commands/`, `events/`, `views/`, `database/` e `utils/`.
- Slash commands gerais: `/ping`, `/help` (menu de seleção persistente), `/about` (botões de link), `/hello`, `/calculator` (calculadora segura com `ast`, sem `eval`).
- Comandos de informação: `/avatar`, `/userinfo`, `/serverinfo`, `/servericon`.
- Utilidades: `/embed` (modal), `/poll` (enquete com botões), `/say` e `/remind` (lembretes em SQLite, entregues por tarefa em segundo plano).
- Moderação básica: `/clear`, `/kick` e `/ban` (com confirmação), `/timeout`, `/unban`, com verificação de permissões e de hierarquia de cargos.
- Diversão: `/dice` e `/fact` (curiosidades em `bot/data/facts.json`).
- Comandos de prefixo educacionais: `!ping`, `!hello`, `!soma`.
- Eventos: `on_ready`, `on_member_join`, `on_member_remove`, `on_message` e tratamento central de erros.
- Logs no terminal e em arquivo rotativo (`logs/programabot.log`).
- Testes automatizados com pytest (lógica, configuração, banco de dados, carregamento das extensões e estrutura do projeto) e workflow de integração contínua no GitHub Actions.

### Documentação

- Trilha educacional completa em `education/`: primeiros passos, fundamentos de programação, Python (13 aulas), bibliotecas, desenvolvimento para Discord, boas práticas.
- Explicação de cada arquivo Python do bot em `education/code-explanation/`.
- Exercícios progressivos (iniciante, básico, intermediário e desafios) com soluções em arquivos separados.
- Recursos: playlists gratuitas recomendadas, documentação oficial, sites úteis e glossário.
- Exemplos executáveis em `examples/`.
- README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, ROADMAP e licença MIT.
- README reescrito apenas com texto, sem emojis.
