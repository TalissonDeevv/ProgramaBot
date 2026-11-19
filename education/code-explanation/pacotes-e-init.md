# Os arquivos `__init__.py`

## 1. Nome e localização

Existe um `__init__.py` em cada pasta de código:

```
bot/__init__.py
bot/commands/__init__.py
bot/commands/general/__init__.py
bot/commands/information/__init__.py
bot/commands/utility/__init__.py
bot/commands/moderation/__init__.py
bot/commands/fun/__init__.py
bot/events/__init__.py
bot/views/__init__.py
bot/database/__init__.py
bot/utils/__init__.py
```

## 2. Finalidade

Um `__init__.py` diz ao Python: **"esta pasta é um pacote"**. Um *pacote* é uma pasta que agrupa vários módulos (arquivos `.py`). É por causa deles que podemos escrever:

```python
from bot.utils.embeds import success_embed
```

O Python lê isso como: dentro do pacote `bot`, entre no pacote `utils`, abra o módulo `embeds` e pegue a função `success_embed`.

## 3. Por que foram criados

Desde o Python 3.3 existem os *namespace packages*, pastas que funcionam como pacote mesmo sem `__init__.py`. Mesmo assim, nós usamos esses arquivos porque:

- deixam claro, para quem lê, quais pastas são código;
- evitam comportamentos confusos quando duas pastas têm o mesmo nome;
- são um bom lugar para uma *docstring* que explica o conteúdo da pasta.

## 4. Como se conectam ao restante do bot

- `bot/__init__.py` guarda `__version__`, `__maintainer__` e `REPOSITORY_URL`. O comando [`/about`](commands/general/about.md) importa esses valores.
- Os outros `__init__.py` têm só uma docstring.
- A função `discover_extensions` em [`main.py`](main.md) **ignora** arquivos que começam com `_`. Por isso os `__init__.py` dentro de `commands/` e `events/` não são carregados como extensões.

## 5. Bibliotecas utilizadas

Nenhuma.

## 6. Importações

Nenhuma. Os arquivos não importam nada.

## 7. Conceitos de Python utilizados

- **Módulo**: um arquivo `.py`.
- **Pacote**: uma pasta com módulos (e, aqui, um `__init__.py`).
- **Docstring**: o texto entre `"""` no início do arquivo. Ferramentas como `help()` e o VS Code o exibem.
- **Variáveis "dunder"** (*double underscore*): nomes como `__version__` são uma convenção da comunidade para metadados do pacote.

## 8. Variáveis e constantes (só em `bot/__init__.py`)

```python
__version__ = "1.0.0-dev"
__maintainer__ = "Talisson Souza"

REPOSITORY_URL = "https://github.com/TalissonDeevv/ProgramaBot"
```

- `__version__`: versão atual, seguindo o [versionamento semântico](../../CHANGELOG.md). O sufixo `-dev` indica que a versão 1.0.0 ainda está em desenvolvimento.
- `__maintainer__`: nome do mantenedor do projeto.
- `REPOSITORY_URL`: endereço do repositório. Está em MAIÚSCULAS porque é uma **constante**, um valor que não deve mudar enquanto o programa roda.

## 9 a 11. Funções, parâmetros e métodos

Esses arquivos não têm funções nem métodos.

## 12. Funcionamento do código

Na primeira vez que alguém importa `bot` ou qualquer submódulo (`bot.config`, por exemplo), o Python executa `bot/__init__.py` **uma única vez** e guarda o resultado em memória. As importações seguintes reaproveitam esse resultado.

## 13. Fluxo de execução

```
python -m bot.main
  └─ importa o pacote bot        → executa bot/__init__.py
      └─ importa bot.main        → executa bot/main.py
          └─ from bot.config ... → bot/config.py
          └─ from bot.utils...   → executa bot/utils/__init__.py e depois bot/utils/logger.py
```

## 14. Exemplos práticos

Teste no terminal, com o ambiente virtual ativado, dentro da pasta do projeto:

```bash
python -c "import bot; print(bot.__version__, bot.REPOSITORY_URL)"
python -c "import bot.utils; help(bot.utils)"
```

## 15. Erros comuns

- **`ModuleNotFoundError: No module named 'bot'`**: você executou o comando fora da pasta do projeto, ou usou `python bot/main.py` em vez de `python -m bot.main`. O `-m` faz o Python tratar `bot` como pacote.
- **Pasta nova não é encontrada**: se você criar `bot/commands/musica/`, crie também um `__init__.py` nela, seguindo o padrão do projeto.

## 16. Como testar

Os testes em `tests/test_extensions.py` importam todos os módulos. Se algum `__init__.py` tiver erro de sintaxe, eles falham:

```bash
python -m pytest tests/test_extensions.py
```

## 17. Como modificar

- Para lançar uma nova versão, altere `__version__` e registre a mudança no [CHANGELOG](../../CHANGELOG.md).
- Ao criar uma nova categoria de comandos, crie `bot/commands/<categoria>/__init__.py` com uma docstring descrevendo a categoria.

## 18. Desafio

Crie a pasta `bot/commands/estudos/` com um `__init__.py`. Depois, siga o guia [Criando um novo comando](../discord-development/10-criando-um-novo-comando.md) para colocar nela um comando `/pomodoro`.
