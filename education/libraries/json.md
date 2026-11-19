# json

## O que é?

O módulo para ler e escrever **JSON** (*JavaScript Object Notation*), um formato de texto para guardar e trocar dados.

## Para que serve? Que problema resolve?

Programas precisam guardar dados em arquivos e trocar dados pela internet. O JSON é o formato mais usado para isso: legível por humanos e entendido por praticamente todas as linguagens. A própria API do Discord envia e recebe JSON (o discord.py faz essa conversão por você).

## Como funciona?

O JSON tem poucos tipos, e cada um corresponde a um tipo do Python:

| JSON | Python |
|---|---|
| `{"chave": valor}` (objeto) | `dict` |
| `[1, 2, 3]` (array) | `list` |
| `"texto"` | `str` |
| `10`, `2.5` | `int`, `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

Regras importantes: strings usam **aspas duplas**, não há vírgula depois do último item e não existem comentários.

## Nativa ou externa?

**Nativa.**

## Como importar

```python
import json
```

## Funções utilizadas no ProgramaBot

| Função | Onde | Explicação |
|---|---|---|
| `json.load(arquivo)` | `commands/fun/fact.py` | Lê um arquivo aberto e devolve os dados em Python. |
| `json.dumps(dados)` | `tests/test_command_helpers.py` | Converte dados Python em **texto** JSON. |

Funções relacionadas: `json.loads(texto)` (lê de um texto) e `json.dump(dados, arquivo)` (escreve em um arquivo). Uma forma de lembrar: o `s` no final significa *string*.

## Exemplo independente do ProgramaBot

```python
import json
from pathlib import Path

arquivo = Path("alunos.json")

dados = {"turma": "Python 1", "alunos": ["Ana", "Bruno"], "ativa": True}
with arquivo.open("w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

with arquivo.open(encoding="utf-8") as f:
    lidos = json.load(f)

print(lidos["alunos"][0])  # Ana
```

- `indent=2` deixa o arquivo formatado e legível.
- `ensure_ascii=False` grava acentos como `ã`, e não como `ã`.

## Documentação oficial

- <https://docs.python.org/pt-br/3/library/json.html>
- Especificação do formato: <https://www.json.org/json-pt.html>
