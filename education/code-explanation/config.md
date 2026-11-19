# `bot/config.py`: configurações do bot

## 1. Nome e localização

- **Arquivo:** `bot/config.py`
- **Arquivos relacionados:** `.env.example` (modelo) e `.env` (seu arquivo real, que nunca vai para o GitHub)

## 2. Finalidade

Ler as configurações do arquivo `.env`, **validar** cada uma e entregar tudo pronto em um objeto `Settings`. Se algo estiver errado, o bot para logo no início com uma mensagem que explica o problema.

## 3. Por que foi criado

O token do bot é uma **senha**. Ele não pode ficar escrito no código, porque o código é público no GitHub. A solução é guardá-lo em uma *variável de ambiente*, carregada a partir do arquivo `.env`, que o `.gitignore` impede de ser enviado.

Além disso, variáveis de ambiente são sempre **texto**. O ID `123` chega como `"123"`, e `true` chega como `"true"`. Este arquivo converte tudo para o tipo certo (`int`, `bool`, `Path`) em um único lugar.

## 4. Como se conecta ao restante do bot

- [`main.py`](main.md) chama `load_settings()` e guarda o resultado em `bot.settings`.
- [`commands/utility/remind.py`](commands/utility/remind.md) usa `bot.settings.database_path`.
- [`events/member_join.py`](events/member_join.md) usa `bot.settings.welcome_channel_id`.
- [`events/message.py`](events/message.md) usa `bot.settings.prefix`.
- `PROJECT_ROOT` é usado pelo `main.py` para criar a pasta `logs/`.

## 5. Bibliotecas utilizadas

| Biblioteca | Tipo | Para quê |
|---|---|---|
| [`os`](../libraries/os.md) | nativa | `os.getenv` lê variáveis de ambiente |
| [`dataclasses`](../libraries/dataclasses.md) | nativa | cria a classe `Settings` sem escrever `__init__` à mão |
| [`pathlib`](../libraries/pathlib.md) | nativa | caminhos de arquivos (`Path`) |
| [`python-dotenv`](../libraries/python-dotenv.md) | externa | `load_dotenv` lê o arquivo `.env` |

## 6. Importações

```python
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
```

O pacote se instala como `python-dotenv`, mas é importado como `dotenv`. Esse tipo de diferença entre o nome de instalação e o de importação é comum. `discord.py` é outro exemplo: instala como `discord.py` e importa como `discord`.

## 7. Conceitos de Python utilizados

- **Exceções personalizadas**: `class ConfigError(Exception)` cria um tipo de erro próprio.
- **Dataclass**: `@dataclass(frozen=True)` gera `__init__`, `__repr__` e `__eq__` automaticamente.
- **Valores padrão**: `prefix: str = "!"`.
- **`None` e tipos opcionais**: `int | None` significa "um inteiro ou nada".
- **Conversão de tipos**: `int("123")`.
- **Tuplas e o operador `in`**: `if normalized in TRUE_VALUES`.
- **f-strings e `!r`**: `f"{value!r}"` mostra o valor com aspas, o que deixa espaços em branco visíveis.
- **`raise ... from None`**: lança um erro novo escondendo o erro original.

## 8. Variáveis e constantes

| Nome | Valor | Explicação |
|---|---|---|
| `PROJECT_ROOT` | `Path(__file__).resolve().parent.parent` | Pasta raiz do projeto (sobe de `bot/config.py` para `bot/` e depois para `ProgramaBot/`). |
| `TOKEN_PLACEHOLDER` | `"cole_seu_token_aqui"` | O texto que vem no `.env.example`. Detecta quem esqueceu de trocar. |
| `VALID_LOG_LEVELS` | tupla com 5 níveis | Valores aceitos em `LOG_LEVEL`. |
| `DEFAULT_DATABASE_PATH` | `PROJECT_ROOT / "data" / "programabot.db"` | Onde o banco fica se `DATABASE_PATH` estiver vazio. |
| `TRUE_VALUES` / `FALSE_VALUES` | tuplas de textos | Formas aceitas de escrever verdadeiro/falso (inclusive em português). |

Os campos de `Settings`:

| Campo | Variável no `.env` | Padrão |
|---|---|---|
| `token` | `DISCORD_TOKEN` | obrigatório |
| `prefix` | `BOT_PREFIX` | `!` |
| `guild_id` | `GUILD_ID` | `None` |
| `welcome_channel_id` | `WELCOME_CHANNEL_ID` | `None` |
| `log_level` | `LOG_LEVEL` | `INFO` |
| `database_path` | `DATABASE_PATH` | `data/programabot.db` |
| `enable_members_intent` | `ENABLE_MEMBERS_INTENT` | `True` |
| `enable_message_content_intent` | `ENABLE_MESSAGE_CONTENT_INTENT` | `True` |
| `sync_commands` | `SYNC_COMMANDS` | `True` |

## 9. Funções

- **`parse_optional_id(name, value)`**: converte texto em ID. Retorna `None` se estiver vazio e lança `ConfigError` se não for um número positivo.
- **`parse_bool(name, value, default)`**: converte `"true"`, `"sim"`, `"0"` etc. em `True`/`False`.
- **`load_settings(env_file=None)`**: a função principal, que lê, valida e devolve um `Settings`.

## 10. Parâmetros

- `name`: nome da variável (`"GUILD_ID"`). Só é usado para montar mensagens de erro úteis.
- `value`: o texto lido do ambiente. Pode ser `None` se a variável não existir.
- `default`: valor usado quando a variável está vazia.
- `env_file`: caminho de um `.env` alternativo. Os testes usam isso para não ler o seu `.env` real.

## 11. Métodos utilizados

| Método | Explicação |
|---|---|
| `load_dotenv(caminho)` | Lê o arquivo e coloca cada `CHAVE=valor` nas variáveis de ambiente. **Não sobrescreve** variáveis que já existem. |
| `os.getenv("NOME", "padrão")` | Lê uma variável; devolve o padrão se ela não existir. |
| `str.strip()` | Remove espaços e quebras de linha do começo e do fim. |
| `str.lower()` / `str.upper()` | Converte para minúsculas/maiúsculas. |
| `Path.is_absolute()` | Diz se o caminho é completo (`C:\...`) ou relativo (`data/...`). |

## 12. Funcionamento do código

### A dataclass imutável

```python
@dataclass(frozen=True)
class Settings:
    token: str
    prefix: str = "!"
    guild_id: int | None = None
```

O decorator `@dataclass` lê as anotações da classe e cria o `__init__` sozinho. Com isso, dá para escrever `Settings(token="abc", prefix="?")`. O `frozen=True` faz `settings.prefix = "x"` lançar um erro, o que protege as configurações de mudanças acidentais.

### Validação do token

```python
token = os.getenv("DISCORD_TOKEN", "").strip()
if not token or token == TOKEN_PLACEHOLDER:
    raise ConfigError("O token do bot não foi configurado. ...")
```

`not token` é `True` quando o texto está vazio. A mensagem diz exatamente qual arquivo ler para resolver o problema.

### Conversão segura de números

```python
try:
    number = int(value.strip())
except ValueError:
    raise ConfigError(f"A variável {name} deve conter apenas números ...") from None
```

`int("abc")` lança `ValueError`. Nós capturamos esse erro e lançamos um `ConfigError` com uma explicação melhor.

### Caminhos relativos

```python
if not database_path.is_absolute():
    database_path = PROJECT_ROOT / database_path
```

Assim, `DATABASE_PATH=data/programabot.db` funciona independentemente da pasta em que o terminal está aberto.

## 13. Fluxo de execução

```
load_settings()
 ├─ load_dotenv(.env)          → variáveis passam a existir em os.environ
 ├─ DISCORD_TOKEN              → vazio? ConfigError
 ├─ BOT_PREFIX                 → espaço ou > 5 caracteres? ConfigError
 ├─ LOG_LEVEL                  → fora da lista? ConfigError
 ├─ DATABASE_PATH              → relativo? junta com PROJECT_ROOT
 ├─ GUILD_ID, WELCOME_...      → parse_optional_id
 ├─ ENABLE_..., SYNC_...       → parse_bool
 └─ return Settings(...)
```

## 14. Exemplos práticos

```bash
python -c "from bot.config import load_settings; s = load_settings(); print(s.prefix, s.guild_id, s.database_path)"
```

Atenção: **não imprima `s.token`**. Se ele aparecer no terminal, alguém pode vê-lo em um print de tela.

## 15. Erros comuns

- **O arquivo se chama `.env.txt`**: o Windows pode esconder extensões. No VS Code, confira se o nome é exatamente `.env`.
- **Aspas no valor**: `DISCORD_TOKEN="abc"` funciona (o python-dotenv remove as aspas), mas não deixe espaços antes do `=`.
- **ID com texto**: `GUILD_ID=meu servidor` gera erro. O ID é um número longo, copiado com o Modo Desenvolvedor.
- **Mudou o `.env` e nada mudou**: reinicie o bot, porque as configurações só são lidas na inicialização.

## 16. Como testar

```bash
python -m pytest tests/test_config.py -v
```

Os testes usam `monkeypatch.setenv` para simular variáveis de ambiente sem tocar no seu `.env`.

## 17. Como modificar

Para adicionar uma configuração nova, como `BOT_COLOR`:

1. Adicione o campo em `Settings` (`color: int = 0x5865F2`).
2. Leia e valide a variável em `load_settings` e passe o valor para `Settings(...)`.
3. Documente a variável no `.env.example`.
4. Crie um teste em `tests/test_config.py`.
5. Atualize esta página.

## 18. Desafio

Adicione a configuração `OWNER_ID` (o ID do dono do bot), validada com `parse_optional_id`. Depois, crie um comando que só responde se `interaction.user.id == bot.settings.owner_id`.
