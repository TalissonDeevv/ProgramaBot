# `bot/commands/fun/fact.py`: o comando /fact

## 1. Nome e localização

- **Arquivo:** `bot/commands/fun/fact.py`
- **Dados:** `bot/data/facts.json`
- **Comando:** `/fact`

## 2. Finalidade

Mostrar uma curiosidade aleatória sobre programação, lida de um arquivo JSON.

## 3. Por que foi criado

Para ensinar a **separar dados de código**. As curiosidades ficam em um arquivo `.json`. Para adicionar uma nova, você edita só o JSON, sem mexer em Python. O arquivo também ensina a ler arquivos com `pathlib` e `json`.

## 4. Como se conecta ao restante do bot

Usa `info_embed`. O teste `test_facts_file_is_valid` garante que o JSON continue no formato correto.

## 5. Bibliotecas utilizadas

- [`json`](../../../libraries/json.md): lê o arquivo.
- [`pathlib`](../../../libraries/pathlib.md): monta o caminho e abre o arquivo.
- [`random`](../../../libraries/random.md): `random.choice`.
- [`discord.py`](../../../libraries/discord-py.md).

## 6. Importações

```python
import json
import random
from pathlib import Path
```

## 7. Conceitos de Python utilizados

- **Leitura de arquivo** com `with` (context manager).
- **`isinstance`** para validar o conteúdo.
- **`all()`** com expressão geradora.
- **Atributos de instância** carregados no `__init__` (`self.facts`).
- **Chaves duplas em f-string** (`{{` → `{`) para escrever chaves literais.

## 8. Variáveis e constantes

- `FACTS_FILE = Path(__file__).resolve().parents[2] / "data" / "facts.json"`
  - `parents[0]` = `fun/`, `parents[1]` = `commands/`, `parents[2]` = `bot/`.
- `self.facts`: a lista de curiosidades.

## 9. Funções

- **`load_facts(path=FACTS_FILE) -> list[str]`**: lê e valida o JSON.
- `Fact.fact(interaction)` e `setup(bot)`.

## 10. Parâmetros

- `path`: caminho do JSON. Os testes passam um arquivo temporário com formato errado para conferir a validação.

## 11. Métodos utilizados

| Método | Explicação |
|---|---|
| `path.open(encoding="utf-8")` | Abre o arquivo para leitura. O `encoding` garante a leitura correta dos acentos. |
| `json.load(arquivo)` | Converte o JSON em objetos Python (`dict`, `list`, `str`...). |
| `data.get("facts")` | Lê a chave sem erro se ela não existir (retorna `None`). |
| `random.choice(lista)` | Item aleatório. |

## 12. Funcionamento do código

O formato esperado do arquivo:

```json
{
  "facts": [
    "O nome Python vem do grupo Monty Python.",
    "..."
  ]
}
```

```python
with path.open(encoding="utf-8") as file:
    data = json.load(file)

facts = data.get("facts") if isinstance(data, dict) else None
if not isinstance(facts, list) or not facts or not all(isinstance(fact, str) for fact in facts):
    raise ValueError(...)
```

Validamos três coisas: é uma lista, não está vazia e todos os itens são textos. Se o JSON estiver errado, o erro aparece **ao carregar a extensão**, com uma mensagem clara, e não no meio de um comando.

O arquivo é lido **uma única vez**, no `__init__`. Ler o disco a cada `/fact` seria desnecessário.

## 13. Fluxo de execução

```
carregar extensão → Fact.__init__ → load_facts() → self.facts (14 itens)
/fact → random.choice(self.facts) → embed "💡 Você sabia?"
```

## 14. Exemplos práticos

```bash
python -c "from bot.commands.fun.fact import load_facts; print(len(load_facts()))"
```

## 15. Erros comuns

- **`json.decoder.JSONDecodeError`**: vírgula sobrando depois do último item, ou aspas simples. JSON só aceita aspas **duplas**.
- **Nova curiosidade não aparece**: reinicie o bot, porque o arquivo é lido só na inicialização.

## 16. Como testar

```bash
python -m pytest tests/test_command_helpers.py -k facts -v
```

## 17. Como modificar

Adicione suas próprias curiosidades no `facts.json`. Confira a informação em fontes confiáveis antes!

## 18. Desafio

Transforme cada curiosidade em um objeto com texto e fonte: `{"text": "...", "source": "https://..."}`. Atualize `load_facts`, o comando (mostre a fonte no rodapé) e o teste.
