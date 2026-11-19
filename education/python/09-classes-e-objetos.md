# 09. Classes, objetos, métodos e orientação a objetos

## Explicação

Uma **classe** é um molde. Um **objeto** (ou **instância**) é algo criado a partir desse molde. A classe `Cachorro` descreve o que todo cachorro tem e faz; `rex` e `bolt` são objetos dessa classe.

- **Atributos**: os dados do objeto (`nome`, `idade`).
- **Métodos**: funções que pertencem à classe (`latir()`).
- **`self`**: o próprio objeto. É o primeiro parâmetro de todo método.
- **`__init__`**: o método que prepara o objeto quando ele é criado (o "construtor").

```python
class Cachorro:
    especie = "Canis familiaris"        # atributo de CLASSE (compartilhado)

    def __init__(self, nome: str, idade: int) -> None:
        self.nome = nome                # atributos de INSTÂNCIA
        self.idade = idade

    def latir(self) -> str:             # método
        return f"{self.nome}: Au au!"


rex = Cachorro("Rex", 3)
print(rex.latir())
```

### Orientação a objetos: os quatro pilares

| Pilar | Ideia | No ProgramaBot |
|---|---|---|
| **Encapsulamento** | Juntar dados e comportamento; esconder detalhes | `ReminderRepository` esconde o SQL; o resto do bot só chama `add()` |
| **Herança** | Uma classe reaproveita outra | `class ProgramaBot(commands.Bot)`, `class Ping(commands.Cog)` |
| **Polimorfismo** | Classes diferentes respondem ao mesmo método | Todo Cog tem `cog_load`; cada um faz o seu trabalho |
| **Abstração** | Expor só o essencial | `discord.abc.Messageable`: "qualquer coisa que tenha `.send()`" |

### Herança e `super()`

```python
class Animal:
    def __init__(self, nome):
        self.nome = nome

    def falar(self):
        return "..."


class Gato(Animal):                    # Gato herda de Animal
    def falar(self):                   # sobrescreve o método
        return f"{self.nome}: Miau"
```

`super().__init__(...)` chama o `__init__` da classe-mãe. É o que o `ProgramaBot` faz para configurar o `commands.Bot`.

### Métodos especiais

`__init__`, `__repr__` e `__eq__` são chamados pelo próprio Python em situações específicas. Veja [dataclasses](../libraries/dataclasses.md), que os gera automaticamente.

### `@property` e `@staticmethod`

```python
class Retangulo:
    def __init__(self, base, altura):
        self.base, self.altura = base, altura

    @property
    def area(self):            # acessado como atributo: r.area
        return self.base * self.altura

    @staticmethod
    def unidade():             # não usa self
        return "cm²"
```

## Exemplo simples

```python
class Contador:
    def __init__(self):
        self.valor = 0

    def incrementar(self):
        self.valor += 1


c = Contador()
c.incrementar()
c.incrementar()
print(c.valor)  # 2
```

## Código executável

[`examples/python-basics/08_classes.py`](../../examples/python-basics/08_classes.py)

## Aplicação no ProgramaBot

Quase tudo é uma classe:

```python
class Ping(commands.Cog):                     # herança
    def __init__(self, bot: commands.Bot):    # construtor
        self.bot = bot                        # atributo

    @app_commands.command(name="ping", ...)
    async def ping(self, interaction):        # método
        latency_ms = round(self.bot.latency * 1000)   # usa o atributo
```

Outros exemplos: `PollState` com `@property total_votes` ([`views/poll.py`](../code-explanation/views/poll.md)), `ReminderRepository` com `@staticmethod` ([`reminders.py`](../code-explanation/database/reminders.md)) e `ConfirmView` sobrescrevendo `interaction_check` ([`confirm.py`](../code-explanation/views/confirm.md)).

## Exercício

1. Crie a classe `ContaBancaria` com `titular` e `saldo`, e os métodos `depositar(valor)` e `sacar(valor)` (lançando erro se faltar saldo).
2. Crie `ContaPoupanca(ContaBancaria)` com o método `render(taxa)`, que aumenta o saldo.
3. Abra [`bot/views/confirm.py`](../../bot/views/confirm.py) e identifique: a classe-mãe, os atributos, os métodos e onde o `super()` é usado.
