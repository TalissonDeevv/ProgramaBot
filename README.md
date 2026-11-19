# 🤖 ProgramaBot

**Aprenda programação na prática, explorando, modificando e desenvolvendo seu próprio bot para Discord.**

O ProgramaBot é um projeto **educacional e open source**: um bot de Discord real e funcional, com **todo o código-fonte aberto** e uma documentação que explica, arquivo por arquivo, cada linha que existe nele.

> 💡 **Você não precisa saber programar para começar.** A trilha começa do zero: o que é programação, como instalar o Python e como colocar o seu bot online.

---

## 🎯 Objetivo educacional

Não queremos apenas disponibilizar um bot pronto. Queremos disponibilizar **o conhecimento necessário para que você construa os seus próprios bots**.

Aqui, o próprio código do bot é o material de estudo. Ao encontrar uma biblioteca, você descobre o que ela é. Ao encontrar uma função, entende como ela funciona. Ao querer criar algo novo, encontra exemplos e exercícios.

## 👥 Para quem é

- Pessoas que nunca programaram
- Quem está começando em Python
- Estudantes de lógica de programação
- Quem tem interesse em bots para Discord
- Pessoas desenvolvedoras iniciantes que querem praticar com um projeto real

## 📦 O que o projeto oferece

| | |
|---|---|
| 🤖 **Um bot funcional** | 20 slash commands, 3 comandos de prefixo, 5 eventos, botões, menus, modais e banco de dados |
| 🔬 **Código explicado** | Uma página para **cada** arquivo Python em [`education/code-explanation/`](education/code-explanation/README.md) |
| 🎓 **Trilha do zero** | [Lógica](education/programming-basics/README.md), [Python básico e intermediário](education/python/README.md), [Discord](education/discord-development/README.md) |
| 📦 **Bibliotecas explicadas** | [Cada biblioteca](education/libraries/README.md) usada no projeto |
| 🏋️ **Exercícios** | [Do iniciante aos desafios](education/exercises/README.md), com soluções separadas |
| 🎬 **Recursos** | [Playlists gratuitas](resources/youtube-playlists.md), [glossário](resources/glossary.md), [documentação oficial](resources/official-documentation.md) |
| ✅ **Testes** | Mais de 200 testes automatizados que rodam sem conectar ao Discord |

## ✨ Funcionalidades do bot

| Categoria | Comandos |
|---|---|
| **Gerais** | `/ping` · `/help` · `/about` · `/hello` · `/calculator` |
| **Informações** | `/avatar` · `/userinfo` · `/serverinfo` · `/servericon` |
| **Utilidades** | `/embed` (modal) · `/poll` (botões) · `/say` · `/remind` (SQLite + tarefa em segundo plano) |
| **Moderação** | `/clear` · `/kick` · `/ban` (com confirmação) · `/timeout` · `/unban` |
| **Diversão** | `/dice` · `/fact` (dados em JSON) |
| **Prefixo (exemplos)** | `!ping` · `!hello` · `!soma` |
| **Eventos** | `on_ready` · `on_member_join` · `on_member_remove` · `on_message` · tratamento central de erros |
| **Interações** | botões, menu de seleção, modal, respostas ephemeral, view persistente |

Cada comando tem validação de parâmetros, verificação de permissões quando necessária, tratamento de erros e respostas adequadas. A calculadora **não usa `eval()`**.

## 🛠️ Tecnologias

| Tecnologia | Versão |
|---|---|
| [Python](https://www.python.org/) | **3.12 recomendado** (mínimo 3.10) |
| [discord.py](https://discordpy.readthedocs.io/en/stable/) | 2.7.1 |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | 1.2.4 |
| SQLite (`sqlite3`, nativo do Python) | — |
| [pytest](https://docs.pytest.org/) + pytest-asyncio (desenvolvimento) | 9.2.0 / 1.4.1 |

## 🚀 Como começar

Primeira vez? Siga o guia completo e ilustrado: **[Primeiros passos](education/getting-started/README.md)**.

Resumo para quem já tem Python e Git:

### 1. Instalação

```bash
git clone https://github.com/TalissonDeevv/ProgramaBot.git
cd ProgramaBot
python -m venv .venv
```

Ative o ambiente virtual:

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Linux / macOS
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements-dev.txt
```

### 2. Configuração

1. Crie uma aplicação no [Discord Developer Portal](https://discord.com/developers/applications), gere o token e ative as intents **Server Members** e **Message Content** ([guia](education/getting-started/06-criando-o-bot-no-discord.md)).
2. Copie `.env.example` para `.env` e preencha `DISCORD_TOKEN` e `GUILD_ID` ([guia](education/getting-started/07-configurando-o-env.md)).

> ⚠️ O token é uma senha. Nunca o publique em commits, prints ou mensagens.

### 3. Execução

```bash
python -m pytest      # testes (opcional)
python -m bot.main    # inicia o bot
```

Depois, use `/help` no seu servidor. Algo deu errado? Veja os [problemas comuns](education/getting-started/09-problemas-comuns.md).

## 🗂️ Estrutura do repositório

```
ProgramaBot/
├── bot/                    # código do bot
│   ├── main.py             # ponto de entrada
│   ├── config.py           # leitura e validação do .env
│   ├── commands/           # um comando por arquivo, por categoria
│   ├── events/             # eventos e tratamento de erros
│   ├── views/              # botões, menus e modais
│   ├── database/           # SQLite (lembretes)
│   ├── utils/              # embeds, calculadora, tempo, logs, moderação
│   └── data/               # dados em JSON
├── education/              # a trilha de aprendizado
│   ├── getting-started/    # instalação e configuração
│   ├── programming-basics/ # lógica de programação
│   ├── python/             # Python do básico ao intermediário
│   ├── libraries/          # cada biblioteca usada
│   ├── discord-development/# como bots funcionam
│   ├── code-explanation/   # cada arquivo do bot explicado
│   ├── exercises/          # exercícios + soluções
│   └── best-practices/     # segurança, organização, testes
├── examples/               # exemplos executáveis e modelos
├── resources/              # playlists, glossário, links
└── tests/                  # testes automatizados
```

## 🎓 Trilha de aprendizado

1. [Primeiros passos](education/getting-started/README.md): coloque o bot online
2. [Fundamentos de programação](education/programming-basics/README.md)
3. [Python](education/python/README.md)
4. [Desenvolvimento para Discord](education/discord-development/README.md)
5. [Explicação do código](education/code-explanation/README.md)
6. [Exercícios](education/exercises/README.md)
7. [Boas práticas](education/best-practices/README.md)

Mapa completo: [`education/README.md`](education/README.md).

## 🎬 Playlists

Destaque para o **Curso em Vídeo**, do professor Gustavo Guanabara ([canal](https://www.youtube.com/@CursoemVideo) · [site](https://www.cursoemvideo.com/)), e outras recomendações organizadas por tema em [`resources/youtube-playlists.md`](resources/youtube-playlists.md).

## 🤝 Como contribuir

Contribuições são bem-vindas, inclusive de quem está aprendendo! Leia o [CONTRIBUTING.md](CONTRIBUTING.md). A regra principal: **todo código novo vem com documentação e testes**.

Ao participar, siga o [Código de Conduta](CODE_OF_CONDUCT.md). Para relatar falhas de segurança, veja o [SECURITY.md](SECURITY.md).

## 🗺️ Roadmap e changelog

- Ideias futuras: [ROADMAP.md](ROADMAP.md)
- Histórico de mudanças: [CHANGELOG.md](CHANGELOG.md)

O projeto segue o [versionamento semântico](https://semver.org/lang/pt-BR/) (`MAJOR.MINOR.PATCH`).

## 📄 Licença

Distribuído sob a [licença MIT](LICENSE). Você pode usar, estudar, modificar e redistribuir o código, mantendo o aviso de copyright.

Os materiais externos recomendados (vídeos, cursos, sites) pertencem aos seus autores e **não** estão incluídos nesta licença.

## 🙌 Créditos

- **Projeto:** ProgramaBot
- **Mantenedor:** Talisson Souza
- **Repositório:** <https://github.com/TalissonDeevv/ProgramaBot>

Construído com [discord.py](https://github.com/Rapptz/discord.py). O ProgramaBot é um projeto independente, sem afiliação com o Discord Inc.
