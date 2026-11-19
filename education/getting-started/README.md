# 🚀 Primeiros passos

Ao final deste módulo, **o seu próprio ProgramaBot estará online** no seu servidor do Discord. Não é preciso saber programar.

| Passo | Guia | Tempo |
|---|---|---|
| 1 | [Instalando o Python](01-instalando-o-python.md) | 10 min |
| 2 | [Instalando o Visual Studio Code](02-instalando-o-vscode.md) | 10 min |
| 3 | [Usando o terminal](03-usando-o-terminal.md) | 15 min |
| 4 | [Baixando o projeto](04-baixando-o-projeto.md) | 5 min |
| 5 | [Ambiente virtual e dependências](05-ambiente-virtual-e-dependencias.md) | 10 min |
| 6 | [Criando o bot no Discord](06-criando-o-bot-no-discord.md) | 15 min |
| 7 | [Configurando o arquivo .env](07-configurando-o-env.md) | 5 min |
| 8 | [Executando e testando](08-executando-e-testando.md) | 10 min |
| 9 | [Problemas comuns](09-problemas-comuns.md) | consulta |
| 10 | [Git e GitHub](10-git-e-github.md) | 20 min |

## Resumo rápido (para quem já tem experiência)

```bash
git clone https://github.com/TalissonDeevv/ProgramaBot.git
cd ProgramaBot
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1   |   Linux/macOS: source .venv/bin/activate
pip install -r requirements-dev.txt
copy .env.example .env        # Linux/macOS: cp .env.example .env
# edite o .env: DISCORD_TOKEN e GUILD_ID
python -m pytest
python -m bot.main
```

## ⚠️ Regra de ouro

O **token** do bot é uma senha. Nunca coloque o token em prints de tela, mensagens, issues, commits ou vídeos. Se ele vazar, gere outro imediatamente no Developer Portal (*Bot > Reset Token*).
