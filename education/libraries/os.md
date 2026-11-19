# os

## O que é?

O módulo `os` (de *operating system*, sistema operacional) dá acesso a recursos do sistema: variáveis de ambiente, processos, pastas, arquivos.

## Para que serve? Que problema resolve?

No ProgramaBot, ele é usado para uma única coisa: **ler variáveis de ambiente**, como `DISCORD_TOKEN`. Variáveis de ambiente são pares nome/valor que o sistema operacional entrega a cada programa. Elas permitem configurar um programa sem alterar o código.

## Como funciona?

Todo processo recebe uma cópia das variáveis de ambiente de quem o iniciou (o terminal, por exemplo). Em Python, elas ficam disponíveis em `os.environ`, um objeto que funciona como um dicionário.

## Nativa ou externa?

**Nativa.**

## Como importar

```python
import os
```

## Funções utilizadas no ProgramaBot

| Função | Onde | Explicação |
|---|---|---|
| `os.getenv(nome, padrão)` | `config.py` | Devolve o valor da variável, ou `padrão` se ela não existir. **Sempre retorna texto** (`str`) ou o padrão. |

```python
token = os.getenv("DISCORD_TOKEN", "").strip()
```

## `os.getenv` vs. `os.environ[...]`

```python
os.environ["NAO_EXISTE"]        # ❌ KeyError
os.getenv("NAO_EXISTE")         # ✅ None
os.getenv("NAO_EXISTE", "abc")  # ✅ "abc"
```

## Exemplo independente do ProgramaBot

```python
import os

usuario = os.getenv("USERNAME") or os.getenv("USER")  # Windows usa USERNAME; Linux/macOS, USER
print("Usuário do sistema:", usuario)
print("Pasta atual:", os.getcwd())
```

Definindo uma variável só para um comando:

```powershell
# PowerShell (Windows)
$env:NOME="Ana"; python app.py
```

```bash
# Linux / macOS
NOME=Ana python app.py
```

## Por que o ProgramaBot usa `pathlib` em vez de `os.path`?

O `os` também tem funções de caminho (`os.path.join`, `os.path.exists`). O módulo [`pathlib`](pathlib.md) faz o mesmo com uma sintaxe mais moderna e legível, e por isso é o recomendado para código novo.

## Documentação oficial

- <https://docs.python.org/pt-br/3/library/os.html>
