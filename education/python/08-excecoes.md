# 08. Exceções

## Explicação

Uma **exceção** é um erro que acontece durante a execução: dividir por zero, converter `"abc"` para número, abrir um arquivo que não existe. Sem tratamento, o programa para e mostra um *traceback*.

### Tratando

```python
try:
    numero = int(input("Número: "))
    print(100 / numero)
except ValueError:
    print("Isso não é um número.")
except ZeroDivisionError:
    print("Não dá para dividir por zero.")
else:
    print("Deu tudo certo!")      # só se não houver erro
finally:
    print("Fim.")                 # sempre executa
```

### Lançando

```python
def sacar(saldo, valor):
    if valor > saldo:
        raise ValueError("Saldo insuficiente")
    return saldo - valor
```

### Criando exceções próprias

```python
class SaldoInsuficiente(Exception):
    """Lançada quando o saque é maior que o saldo."""
```

### Hierarquia

Exceções são classes e herdam umas das outras. `except ValueError` também captura subclasses de `ValueError`. Por isso, **trate as mais específicas primeiro**.

### Boas práticas

- Capture **só** os erros que você sabe tratar. `except Exception:` em todo lugar esconde bugs.
- Nunca use `except:` sozinho, sem tipo.
- Use `raise ... from None` para trocar um erro técnico por um erro mais claro.

## Exemplo simples

```python
try:
    idade = int("vinte")
except ValueError as erro:
    print("Erro:", erro)
```

## Código executável

[`examples/python-basics/07_excecoes.py`](../../examples/python-basics/07_excecoes.py)

## Aplicação no ProgramaBot

| Situação | Onde |
|---|---|
| Exceções próprias | `ConfigError`, `CalculatorError`, `TimeParseError`, `PollError` |
| Trocar o erro técnico por um claro | `raise ConfigError(...) from None` em [`config.py`](../code-explanation/config.md) |
| Mais específica antes da genérica | `except discord.NotFound` antes de `except discord.HTTPException` em [`unban.py`](../code-explanation/commands/moderation/unban.md) |
| `finally` | fechar o banco em [`reminders.py`](../code-explanation/database/reminders.md) |
| Quando capturar `Exception` é certo | a tarefa de lembretes, que não pode parar ([`remind.py`](../code-explanation/commands/utility/remind.md)) |
| Tratamento central | [`events/errors.py`](../code-explanation/events/errors.md) |

## Exercício

1. Escreva `ler_inteiro(mensagem)` que repita o `input` até o usuário digitar um inteiro válido.
2. Crie `class IdadeInvalida(Exception)` e uma função que a lance para idades negativas.
3. Por que `except Exception:` antes de `except ValueError:` é um problema? Teste.
