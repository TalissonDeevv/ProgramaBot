# 07. Configurando o arquivo `.env`

O `.env` guarda as configurações do **seu** bot, inclusive o token. Ele **não** vai para o GitHub (está no `.gitignore`).

## 1. Crie o arquivo a partir do modelo

Na pasta raiz do projeto:

| Sistema | Comando |
|---|---|
| Windows (PowerShell ou cmd) | `copy .env.example .env` |
| Linux / macOS | `cp .env.example .env` |

Ou, no VS Code: clique com o botão direito em `.env.example` > *Copiar*, cole na mesma pasta e renomeie a cópia para `.env`.

> O nome é exatamente **`.env`**: começa com ponto e não tem nada antes dele. Cuidado com o Windows, que pode criar `.env.txt` sem mostrar a extensão.

## 2. Preencha os valores

Abra o `.env` no VS Code:

```ini
DISCORD_TOKEN=cole_o_token_que_você_copiou
GUILD_ID=123456789012345678
```

| Variável | Obrigatória? | O que colocar |
|---|---|---|
| `DISCORD_TOKEN` | ✅ sim | O token do bot ([passo 6](06-criando-o-bot-no-discord.md#3-configure-o-bot)) |
| `GUILD_ID` | recomendado | O ID do seu servidor de testes. Com ele, os slash commands aparecem na hora. |
| `BOT_PREFIX` | não | Prefixo dos comandos de exemplo (padrão `!`) |
| `WELCOME_CHANNEL_ID` | não | ID do canal de boas-vindas. Vazio = canal de mensagens do sistema. |
| `LOG_LEVEL` | não | `DEBUG`, `INFO` (padrão), `WARNING`, `ERROR`, `CRITICAL` |
| `DATABASE_PATH` | não | Onde salvar o banco dos lembretes (padrão `data/programabot.db`) |
| `ENABLE_MEMBERS_INTENT` | não | `true`/`false`, conforme o Developer Portal |
| `ENABLE_MESSAGE_CONTENT_INTENT` | não | `true`/`false`, conforme o Developer Portal |
| `SYNC_COMMANDS` | não | `true` (padrão) sincroniza os slash commands ao iniciar |

Regras do formato: uma variável por linha, sem espaços ao redor do `=`; linhas começando com `#` são comentários.

## 3. Proteja o arquivo

- ✅ O `.env` está no `.gitignore`; confira com `git status`, em que ele **não** deve aparecer.
- ❌ Não envie o `.env` para ninguém.
- ❌ Não mostre o `.env` em prints ou transmissões ao vivo.
- 🔁 Se o token vazar: Developer Portal > Bot > **Reset Token**, e atualize o `.env`.

## Como o bot lê esse arquivo?

O arquivo [`bot/config.py`](../code-explanation/config.md) usa a biblioteca [python-dotenv](../libraries/python-dotenv.md) para carregar o `.env` e valida cada valor. Se algo estiver errado, o bot para e explica o problema.

Próximo passo: [Executando e testando](08-executando-e-testando.md).
