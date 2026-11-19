# 10. Decorators

## Explicação

Um **decorator** é uma função que recebe outra função e devolve uma versão "decorada" dela, com algum comportamento a mais. A sintaxe `@` é um atalho:

```python
@meu_decorator
def ola():
    ...

# é exatamente o mesmo que:
def ola():
    ...
ola = meu_decorator(ola)
```

Isso funciona porque, em Python, **funções são objetos**: podem ser guardadas em variáveis, passadas como argumento e retornadas.

### Criando um decorator

```python
import functools


def anunciar(funcao):
    @functools.wraps(funcao)            # preserva o nome e a docstring originais
    def nova_funcao(*args, **kwargs):
        print(f"Chamando {funcao.__name__}...")
        resultado = funcao(*args, **kwargs)
        print("Pronto!")
        return resultado
    return nova_funcao


@anunciar
def somar(a, b):
    return a + b


print(somar(2, 3))
```

### Decorators com argumentos

`@app_commands.command(name="ping")` tem parênteses: `command(name="ping")` **devolve** um decorator, que então é aplicado à função. É uma "fábrica de decorators".

### Empilhando decorators

São aplicados **de baixo para cima** (o mais próximo da função primeiro).

## Exemplo simples

```python
def gritar(funcao):
    def nova():
        return funcao().upper()
    return nova


@gritar
def saudacao():
    return "olá"


print(saudacao())  # OLÁ
```

## Código executável

[`examples/python-basics/10_decorators_e_context_managers.py`](../../examples/python-basics/10_decorators_e_context_managers.py)

## Aplicação no ProgramaBot

Decorators são a forma principal de "conversar" com o discord.py:

| Decorator | Efeito |
|---|---|
| `@app_commands.command(...)` | Registra um slash command |
| `@app_commands.describe(...)` | Adiciona descrições aos parâmetros |
| `@app_commands.guild_only()` | Restringe a servidores |
| `@app_commands.checks.has_permissions(...)` | Adiciona uma verificação |
| `@commands.Cog.listener()` | Registra um evento |
| `@commands.command(...)` | Registra um comando de prefixo |
| `@soma.error` | Registra um tratador de erro |
| `@discord.ui.button(...)` | Cria um botão |
| `@tasks.loop(seconds=30)` | Transforma em tarefa repetitiva |
| `@dataclass` | Gera métodos da classe |
| `@property`, `@staticmethod` | Tipos especiais de método |

Exemplo empilhado em [`clear.py`](../code-explanation/commands/moderation/clear.md):

```python
@app_commands.command(name="clear", ...)
@app_commands.describe(quantidade="...")
@app_commands.guild_only()
@app_commands.default_permissions(manage_messages=True)
@app_commands.checks.has_permissions(manage_messages=True)
@app_commands.checks.bot_has_permissions(manage_messages=True, read_message_history=True)
async def clear(self, interaction, quantidade): ...
```

## Exercício

1. Crie um decorator `@cronometrar` que mostre quanto tempo uma função levou para executar (use `time.perf_counter()`).
2. Crie um decorator `@repetir(vezes)` (com argumento) que execute a função várias vezes.
3. No ProgramaBot, encontre um arquivo com **cinco ou mais** decorators empilhados e explique cada um.
