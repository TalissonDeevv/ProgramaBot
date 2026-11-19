# re (expressões regulares)

## O que é?

O módulo de **expressões regulares** (*regex*): uma mini-linguagem para descrever **padrões de texto**.

## Para que serve? Que problema resolve?

Verificar se um texto "tem o formato certo" com `if`s e laços fica longo e confuso. Validar um CEP, extrair números de uma frase ou interpretar `1h30m` vira uma linha com regex.

## Como funciona?

Você escreve um padrão e pede ao `re` para procurá-lo em um texto. Símbolos mais comuns:

| Símbolo | Significa | Exemplo |
|---|---|---|
| `\d` | um dígito (0–9) | `\d\d` casa com `42` |
| `+` | uma ou mais vezes | `\d+` casa com `2026` |
| `*` | zero ou mais vezes | `a*` |
| `?` | opcional | `colou?r` |
| `[abc]` | um dos caracteres | `[dhms]` casa com `h` |
| `( )` | grupo que **captura** | `(\d+)` |
| `(?: )` | grupo que **não** captura | `(?:\d+[dhms])+` |
| `^` / `$` | início / fim do texto | `^\d+$` |
| `\s` | espaço em branco | |
| `.` | qualquer caractere | |

Use sempre *raw strings* (`r"..."`) para escrever padrões; senão o Python interpreta `\d` antes do `re`.

## Nativa ou externa?

**Nativa.**

## Como importar

```python
import re
```

## Funções utilizadas no ProgramaBot

| Função | Onde | Explicação |
|---|---|---|
| `re.compile(padrão, flags)` | `time_parser.py`, `test_project_structure.py` | Compila o padrão uma vez para reutilizá-lo. |
| `padrão.fullmatch(texto)` | `time_parser.py` | O texto **inteiro** precisa casar. Retorna um objeto `Match` ou `None`. |
| `padrão.findall(texto)` | `time_parser.py`, testes | Lista de todas as ocorrências (ou dos grupos capturados). |
| `padrão.search(texto)` | `test_project_structure.py` | Procura a primeira ocorrência em qualquer posição. |

### Os padrões do `time_parser`

```python
FULL_PATTERN = re.compile(r"(?:\d+[dhms])+")   # "1h30m" ✔   "abc" ✘   "10" ✘
PART_PATTERN = re.compile(r"(\d+)([dhms])")    # findall("1h30m") → [("1","h"), ("30","m")]
```

## Exemplo independente do ProgramaBot

```python
import re

texto = "Pedidos: #123 (R$ 45), #456 (R$ 10) e #789 (R$ 99)"

numeros = re.findall(r"#(\d+)", texto)
print(numeros)                     # ['123', '456', '789']

cep = re.compile(r"\d{5}-?\d{3}")  # {5} = exatamente 5 vezes
print(bool(cep.fullmatch("01310-100")))  # True
print(bool(cep.fullmatch("1234")))       # False
```

## Dica

Teste seus padrões em <https://regex101.com/> (escolha o *flavor* "Python"). O site explica cada parte do padrão.

## Documentação oficial

- Referência: <https://docs.python.org/pt-br/3/library/re.html>
- Tutorial: <https://docs.python.org/pt-br/3/howto/regex.html>
