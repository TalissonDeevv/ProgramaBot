# `bot/commands/general/calculator.py`: o comando /calculator

## 1. Nome e localização

- **Arquivo:** `bot/commands/general/calculator.py`
- **Comando:** `/calculator expressao:<texto>`

## 2. Finalidade

Receber uma expressão matemática, calculá-la com segurança e mostrar o resultado em um embed verde (ou o erro, em um embed vermelho visível só para quem errou).

## 3. Por que foi criado

Para ensinar **separação de responsabilidades**. Este arquivo cuida só da parte do Discord (receber o texto e responder). A matemática e a segurança ficam em [`utils/calculator.py`](../../utils/calculator.md), que pode ser testado sem o Discord.

## 4. Como se conecta ao restante do bot

```
/calculator → calculate() e format_result() (utils/calculator.py)
            → success_embed / error_embed (utils/embeds.py)
```

## 5. Bibliotecas utilizadas

- [`discord.py`](../../../libraries/discord-py.md).

## 6. Importações

```python
from bot.utils.calculator import MAX_EXPRESSION_LENGTH, CalculatorError, calculate, format_result
from bot.utils.embeds import error_embed, success_embed
```

Importamos também a **constante** `MAX_EXPRESSION_LENGTH`, para que o limite do Discord e o limite da calculadora sejam sempre o mesmo número.

## 7. Conceitos de Python utilizados

- **`try / except` com exceção personalizada.**
- **`return` antecipado** depois de tratar o erro.
- **Blocos de código no markdown do Discord** (três crases).

## 8. Variáveis

- `result`: o número calculado.
- `embed`: a resposta.

## 9. Funções

- `Calculator.calculator(interaction, expressao)`: o comando.
- `setup(bot)`.

## 10. Parâmetros

- `expressao: app_commands.Range[str, 1, MAX_EXPRESSION_LENGTH]`: o Discord impede textos vazios ou maiores que 100 caracteres antes mesmo de o bot recebê-los.

## 11. Métodos utilizados

| Método | Explicação |
|---|---|
| `calculate(texto)` | Calcula ou lança `CalculatorError`. |
| `format_result(numero)` | Formata para exibição. |
| `str(error)` | A mensagem da exceção. |

## 12. Funcionamento do código

```python
try:
    result = calculate(expressao)
except CalculatorError as error:
    await interaction.response.send_message(embed=error_embed(str(error)), ephemeral=True)
    return
```

Só capturamos `CalculatorError`, os erros que **esperamos**. Qualquer outro erro, como um bug, segue para o tratador central em [`events/errors.py`](../../events/errors.md), que registra o problema no log. Capturar `Exception` aqui esconderia bugs.

```python
embed = success_embed(f"```\n{expressao}\n= {format_result(result)}\n```", title="🧮 Calculadora")
```

## 13. Fluxo de execução

```
/calculator expressao:"2^10"
 ├─ calculate("2^10") → 1024
 └─ embed:  2^10
            = 1024

/calculator expressao:"print(1)"
 └─ CalculatorError → embed vermelho ephemeral
```

## 14. Exemplos práticos

Teste no Discord: `(5 + 5) * 3`, `10 / 3`, `2 ** 0.5`, `7 // 2`, `7 % 2`, `abc`.

## 15. Erros comuns

- **Expressão com `x` para multiplicar** (`2x3`): use `*` ou `×`.
- **Expressão com `=`**: digite só o lado esquerdo.

## 16. Como testar

```bash
python -m pytest tests/test_calculator.py -v
```

## 17. Como modificar

Mostre o tipo do resultado (`int` ou `float`) em um campo do embed: `embed.add_field(name="Tipo", value=type(result).__name__)`.

## 18. Desafio

Crie o comando de prefixo `!calc <expressão>` em [`prefix_examples.py`](prefix_examples.md), reutilizando `calculate`. Dica: use `*, expressao: str` para receber o texto com espaços.
