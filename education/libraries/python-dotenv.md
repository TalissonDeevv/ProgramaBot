# python-dotenv

## O que é?

Uma biblioteca pequena que lê um arquivo chamado `.env` e transforma cada linha `CHAVE=valor` em uma **variável de ambiente** do programa.

## Para que serve? Que problema resolve?

Senhas, tokens e chaves de API **não podem** ficar escritos no código, porque o código vai para o GitHub. A prática recomendada é guardá-los em variáveis de ambiente. Configurá-las manualmente no terminal a cada execução, porém, é trabalhoso. O `python-dotenv` resolve isso: você escreve os valores uma vez no `.env`, e o `.gitignore` impede que esse arquivo seja publicado.

## Como funciona?

```
.env                         seu programa
DISCORD_TOKEN=abc   ──load_dotenv()──►  os.environ["DISCORD_TOKEN"] == "abc"
```

Por padrão, `load_dotenv` **não sobrescreve** variáveis que já existem no sistema. Isso permite, por exemplo, que um servidor de hospedagem defina o token de outra forma.

## Nativa ou externa?

**Externa.**

## Como instalar

```bash
pip install python-dotenv==1.2.4
```

(Já incluído no `requirements.txt`.)

## Como importar

```python
from dotenv import load_dotenv
```

Instala-se como `python-dotenv`, mas importa-se como `dotenv`.

## Funções utilizadas no ProgramaBot

| Função | Explicação |
|---|---|
| `load_dotenv(caminho)` | Lê o arquivo e define as variáveis. Retorna `True` se encontrou alguma variável e `False` caso contrário (por exemplo, se o arquivo não existir). Não lança erro se o arquivo estiver ausente. |

## Onde aparece

- [`bot/config.py`](../code-explanation/config.md): `load_dotenv(env_file or PROJECT_ROOT / ".env")`.

## Como é aplicado no projeto

1. O repositório traz o `.env.example`, um modelo **sem segredos**.
2. O estudante copia o arquivo para `.env` e preenche o token.
3. `load_settings()` chama `load_dotenv` e depois lê os valores com `os.getenv`.

## Formato do arquivo `.env`

```ini
# Comentários começam com #
DISCORD_TOKEN=abc123
BOT_PREFIX=!
GUILD_ID=
FRASE="valores com espaço podem ficar entre aspas"
```

- Não coloque espaços ao redor do `=`.
- Uma variável por linha.

## Exemplo independente do ProgramaBot

```python
# arquivo: app.py   |   arquivo .env na mesma pasta: NOME=Maria
import os
from dotenv import load_dotenv

load_dotenv()                      # sem argumento, procura um .env a partir da pasta atual
nome = os.getenv("NOME", "visitante")
print(f"Olá, {nome}!")
```

## Documentação oficial

- PyPI: <https://pypi.org/project/python-dotenv/>
- Repositório: <https://github.com/theskumar/python-dotenv>
