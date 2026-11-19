# 07. Módulos, pacotes e importações

## Explicação

- **Módulo**: um arquivo `.py`.
- **Pacote**: uma pasta de módulos (com `__init__.py`).
- **Importar**: usar, em um arquivo, o código que está em outro.

### Formas de importar

```python
import random                         # importa o módulo inteiro → random.choice(...)
from random import choice             # importa só o nome → choice(...)
from datetime import datetime, timedelta  # vários nomes
import discord as dc                  # apelido (evite, a não ser por convenção)
```

### Importando do próprio projeto

```python
from bot.utils.embeds import success_embed
#    └─pacote─┘└módulo┘        └─nome─┘
```

Para isso funcionar, o Python precisa encontrar a pasta `bot`. Por isso executamos o bot com `python -m bot.main` a partir da raiz do projeto.

### Biblioteca padrão vs. pacotes externos

- **Biblioteca padrão**: já vem com o Python (`random`, `json`, `sqlite3`...).
- **Externos**: instalados com **pip**, o gerenciador de pacotes do Python:

```bash
pip install discord.py==2.7.1
pip install -r requirements.txt   # instala tudo que está listado no arquivo
pip list                          # mostra o que está instalado
```

Pacotes externos são instalados no **ambiente virtual** do projeto. Veja [Ambiente virtual](../getting-started/05-ambiente-virtual-e-dependencias.md).

### Ordem dos imports (PEP 8)

1. biblioteca padrão; 2. externos; 3. do projeto. Com uma linha em branco entre os grupos.

### `if __name__ == "__main__":`

Quando um arquivo é **executado**, `__name__` vale `"__main__"`. Quando é **importado**, vale o nome do módulo. Assim, o bloco só roda na execução direta.

## Exemplo simples

```python
# arquivo: matematica.py
def dobro(n):
    return n * 2

# arquivo: app.py (na mesma pasta)
from matematica import dobro
print(dobro(4))
```

## Código executável

Crie os dois arquivos acima na mesma pasta e execute `python app.py`.

## Aplicação no ProgramaBot

Abra qualquer arquivo de comando e veja os três blocos de import. Em [`main.py`](../code-explanation/main.md):

```python
import asyncio                                   # padrão
import logging
from pathlib import Path

import discord                                   # externo
from discord.ext import commands

from bot import __version__                      # projeto
from bot.config import PROJECT_ROOT, ConfigError, Settings, load_settings
```

Veja também [os arquivos `__init__.py`](../code-explanation/pacotes-e-init.md) e a diferença entre [módulo, pacote, biblioteca e framework](../libraries/README.md).

## Exercício

1. Crie um módulo `saudacoes.py` com as funções `ola(nome)` e `tchau(nome)` e use-as em outro arquivo.
2. Rode `pip list` com o ambiente virtual ativado. Encontre `discord.py` e veja a versão.
3. Por que `python bot/main.py` dá `ModuleNotFoundError: No module named 'bot'`, mas `python -m bot.main` funciona?
