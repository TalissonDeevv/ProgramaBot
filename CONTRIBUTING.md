# Como contribuir com o ProgramaBot

Obrigado pelo interesse! O ProgramaBot é um projeto **educacional**, e contribuições de quem está aprendendo são muito bem-vindas: correções de texto, explicações mais claras, exercícios, comandos novos, testes.

## Antes de começar

1. Leia o [Código de Conduta](CODE_OF_CONDUCT.md).
2. Procure nas [issues](https://github.com/TalissonDeevv/ProgramaBot/issues) se alguém já está trabalhando no mesmo assunto.
3. Para mudanças grandes (um comando novo, uma reorganização), **abra uma issue primeiro** para conversar sobre a ideia.

## Preparando o ambiente

```bash
# 1. Faça um fork pelo GitHub e clone o SEU fork
git clone https://github.com/<seu-usuario>/ProgramaBot.git
cd ProgramaBot

# 2. Ambiente virtual e dependências de desenvolvimento
python -m venv .venv
# ative o ambiente (veja education/getting-started/05-ambiente-virtual-e-dependencias.md)
pip install -r requirements-dev.txt

# 3. Confirme que tudo passa antes de mudar qualquer coisa
python -m pytest
```

## Fluxo de trabalho

```bash
git switch -c tipo/descricao-curta     # ex.: feat/comando-coinflip, docs/corrige-aula-05, fix/calculadora-virgula
# ... faça as mudanças ...
python -m pytest
git add <arquivos>
git commit -m "Adiciona o comando /coinflip"
git push -u origin tipo/descricao-curta
```

Depois, abra um **pull request** para a branch `main` do repositório original, explicando **o que** mudou e **por quê**.

Prefixos sugeridos para branches: `feat/` (funcionalidade), `fix/` (correção), `docs/` (documentação), `test/` (testes), `refactor/` (reorganização sem mudar o comportamento).

## ✅ Regra principal: código e documentação andam juntos

Toda contribuição que altera o bot precisa seguir o [checklist de novas funcionalidades](education/best-practices/05-checklist-de-novas-funcionalidades.md):

- [ ] Código real em `bot/` (sem pseudocódigo nem funcionalidades "anunciadas" que não existem)
- [ ] Explicação em `education/code-explanation/<mesmo caminho>.md`, com as 18 seções
- [ ] Bibliotecas novas documentadas em `education/libraries/`
- [ ] Exercício novo, quando fizer sentido (com a solução em arquivo separado)
- [ ] README atualizado, se a lista de funcionalidades mudou
- [ ] Entrada no `CHANGELOG.md`, na seção "Não lançado"
- [ ] Testes criados ou atualizados, com **`python -m pytest` passando**

Vários desses itens são verificados automaticamente pelos testes (`tests/test_project_structure.py` e `tests/test_extensions.py`).

Passo a passo para criar um comando: [Criando um novo comando](education/discord-development/10-criando-um-novo-comando.md).

## Padrões de código

- Python 3.10+; siga a [PEP 8](https://peps.python.org/pep-0008/).
- Nomes de variáveis, funções e classes em inglês; **parâmetros de comandos, mensagens ao usuário, comentários e docstrings em português**.
- Separe a lógica (testável) da parte do Discord.
- Use os embeds de `bot/utils/embeds.py`.
- Em comandos sensíveis: `default_permissions` + `checks.has_permissions` + `checks.bot_has_permissions`.
- Ao reenviar texto de usuários: `allowed_mentions=discord.AllowedMentions.none()`.
- Nunca use `eval`/`exec` com dados de usuários; nunca monte SQL com f-strings.
- Dependências novas precisam de versão fixa (`==`) e de justificativa no pull request.

## Padrões de documentação

- Português brasileiro, linguagem clara, didática e progressiva.
- Explique termos técnicos na primeira vez que aparecem.
- Mostre trechos **reais** do código e explique o **porquê**, não só o quê.
- Não copie conteúdo protegido de outras fontes; recomende o original com um link.

## Segurança

- **Nunca** inclua tokens, senhas ou o arquivo `.env` em commits, issues ou pull requests.
- Vulnerabilidades: siga o [SECURITY.md](SECURITY.md), e não abra uma issue pública.

## Versionamento

O projeto segue o [versionamento semântico](https://semver.org/lang/pt-BR/). Quem decide quando uma versão é lançada é o mantenedor; nos pull requests, registre as mudanças apenas em "Não lançado" no CHANGELOG.

## Dúvidas

Abra uma issue com a etiqueta de dúvida. Não existe pergunta boba: este projeto existe para ensinar.
