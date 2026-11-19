# 10. Git e GitHub

## O que são?

- **Git** é um programa de **controle de versão**: ele guarda o histórico de todas as mudanças do seu código. Dá para voltar no tempo, ver o que mudou e trabalhar em equipe sem um sobrescrever o trabalho do outro.
- **GitHub** é um site que hospeda repositórios Git na internet. O ProgramaBot está em <https://github.com/TalissonDeevv/ProgramaBot>.

## Instalação

- Baixe em <https://git-scm.com/downloads> e instale com as opções padrão.
- Verifique com `git --version`.
- Configure seu nome e e-mail (aparecem nos seus commits):

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu-email@exemplo.com"
```

## Conceitos

| Termo | Significado |
|---|---|
| **Repositório** | A pasta do projeto com todo o histórico |
| **Commit** | Uma "foto" das mudanças, com uma mensagem explicando o que mudou |
| **Branch** | Uma linha de trabalho paralela (ex.: `feat/comando-coinflip`) |
| **Clone** | Baixar um repositório |
| **Fork** | Copiar um repositório do GitHub para a sua conta |
| **Push / Pull** | Enviar / receber commits do GitHub |
| **Pull request (PR)** | Pedir que suas mudanças sejam incorporadas a outro repositório |

## Fluxo do dia a dia

```bash
git status                       # o que mudou?
git switch -c feat/meu-comando   # cria e entra em uma branch nova
git add bot/commands/fun/coinflip.py education/code-explanation/commands/fun/coinflip.md
git commit -m "Adiciona o comando /coinflip"
git push -u origin feat/meu-comando
```

Antes de cada `git add`, rode `git status` e confira se o `.env` **não** aparece na lista. Ele deve estar sendo ignorado.

## Recebendo atualizações do ProgramaBot

Se você clonou o repositório original:

```bash
git pull
```

Se você trabalha em um fork, configure o repositório original como `upstream`:

```bash
git remote add upstream https://github.com/TalissonDeevv/ProgramaBot.git
git fetch upstream
git merge upstream/main
```

## Material para aprofundar

- Livro oficial *Pro Git*, gratuito e em português: <https://git-scm.com/book/pt-br/v2>
- Documentação do GitHub: <https://docs.github.com/pt>
- Playlists recomendadas: [resources/youtube-playlists.md](../../resources/youtube-playlists.md#git-e-github)

## Exercício

1. Faça um fork do ProgramaBot e clone o seu fork.
2. Crie a branch `estudo/minha-dica`, adicione uma dica em `STUDY_TIPS` (`bot/commands/general/hello.py`), faça o commit e o push.
3. Abra o seu fork no GitHub e veja o commit.
