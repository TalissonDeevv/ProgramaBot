# 09. Problemas comuns de instalação e configuração

Procure a mensagem que apareceu no seu terminal.

## Python e ambiente

| Mensagem / sintoma | Causa | Solução |
|---|---|---|
| `'python' não é reconhecido...` | Python fora do PATH | [Reinstale](01-instalando-o-python.md) marcando "Add python.exe to PATH", ou use `py` |
| `...Activate.ps1 não pode ser carregado...` | Política de execução do PowerShell | Veja as [opções](05-ambiente-virtual-e-dependencias.md#erro-no-powershell-a-execução-de-scripts-foi-desabilitada) |
| `ModuleNotFoundError: No module named 'discord'` | Dependências não instaladas, ou ambiente não ativado | Ative o `.venv` e rode `pip install -r requirements-dev.txt` |
| `ModuleNotFoundError: No module named 'bot'` | Rodou fora da raiz ou usou `python bot/main.py` | Vá para a pasta raiz e use `python -m bot.main` |
| `ERROR: Could not find a version that satisfies the requirement ...` | Python antigo demais | Use Python 3.10 ou superior (recomendado: 3.12) |
| Imports sublinhados em vermelho no VS Code | Interpretador errado | `Ctrl+Shift+P` → "Python: Select Interpreter" → escolha o `.venv` |

## Configuração

| Mensagem | Causa | Solução |
|---|---|---|
| `[Erro de configuração] O token do bot não foi configurado` | `.env` ausente, com outro nome ou com o texto de exemplo | [Configure o .env](07-configurando-o-env.md) |
| `[Erro de configuração] A variável GUILD_ID deve conter apenas números` | Algo além de números no ID | Copie o ID com o Modo Desenvolvedor |
| `O Discord recusou o token` | Token errado, incompleto ou resetado | Gere outro token (Bot > Reset Token) e cole no `.env` |
| `As intents privilegiadas não estão ativadas` | Intents ligadas no `.env`, mas desligadas no Portal | Ative-as no Developer Portal (Bot > Privileged Gateway Intents) |

## No Discord

| Sintoma | Causa provável | Solução |
|---|---|---|
| Slash commands não aparecem | Sincronização global ainda em andamento | Configure `GUILD_ID` e reinicie; recarregue o Discord (`Ctrl+R`) |
| Comandos aparecem duplicados | Comandos globais e do servidor ao mesmo tempo | Veja [Slash vs. prefixo](../discord-development/03-slash-vs-prefixo.md#sincronização-de-slash-commands) |
| "O aplicativo não respondeu" | O bot está offline ou o comando deu erro | Veja o terminal do bot |
| Bot offline | O programa não está rodando | Execute `python -m bot.main` e deixe o terminal aberto |
| `!ping` não responde | Message Content Intent desligada | Ative no Portal e no `.env` |
| Sem boas-vindas | Server Members Intent desligada, ou sem canal configurado | Ative a intent; configure `WELCOME_CHANNEL_ID` ou o canal do sistema |
| "Meu cargo está abaixo..." | Hierarquia de cargos | Arraste o cargo do bot para cima |
| "Eu preciso da permissão: ..." | O bot não tem a permissão | Ajuste os cargos ou as permissões do canal |
| Comando de moderação invisível | Você não tem a permissão (`default_permissions`) | Use uma conta com a permissão |

## Ainda com problemas?

1. Leia o log em `logs/programabot.log`.
2. Rode com `LOG_LEVEL=DEBUG` no `.env` para ver mais detalhes.
3. Procure a mensagem de erro nas [issues do repositório](https://github.com/TalissonDeevv/ProgramaBot/issues).
4. Abra uma issue nova descrevendo o problema, **sem** incluir o token.
