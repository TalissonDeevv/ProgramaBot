# dataclasses

## O que é?

Um módulo que oferece o decorator `@dataclass`, que cria automaticamente o código repetitivo de classes feitas para **guardar dados**.

## Para que serve? Que problema resolve?

Sem dataclass, uma classe simples de dados exige bastante código repetido:

```python
class Lembrete:
    def __init__(self, id, mensagem):
        self.id = id
        self.mensagem = mensagem

    def __repr__(self):
        return f"Lembrete(id={self.id!r}, mensagem={self.mensagem!r})"

    def __eq__(self, outro):
        return (self.id, self.mensagem) == (outro.id, outro.mensagem)
```

Com dataclass:

```python
from dataclasses import dataclass

@dataclass
class Lembrete:
    id: int
    mensagem: str
```

O resultado é o mesmo: `__init__`, `__repr__` (texto ao imprimir) e `__eq__` (comparação com `==`) são gerados automaticamente.

## Como funciona?

O decorator lê as **anotações de tipo** da classe (`id: int`) e, a partir delas, gera os métodos. As anotações **não** são verificadas em tempo de execução: `Lembrete(id="abc", ...)` funciona. Elas servem como documentação e para ferramentas como o VS Code.

## Nativa ou externa?

**Nativa** (desde o Python 3.7).

## Como importar

```python
from dataclasses import dataclass, field
```

## Recursos utilizados no ProgramaBot

| Recurso | Onde | Explicação |
|---|---|---|
| `@dataclass(frozen=True)` | `config.py` (`Settings`), `reminders.py` (`Reminder`) | Objetos **imutáveis**: tentar alterar um campo lança `FrozenInstanceError`. |
| `@dataclass` | `views/poll.py` (`PollState`) | Objeto que pode mudar (os votos mudam). |
| Valores padrão (`prefix: str = "!"`) | `config.py` | Campo opcional ao criar o objeto. |
| `field(default_factory=dict)` | `views/poll.py` | Cria um dicionário **novo** para cada objeto. |

### Por que `default_factory`?

```python
@dataclass
class Enquete:
    votos: dict = {}                            # ❌ ValueError: o Python não permite
    votos: dict = field(default_factory=dict)   # ✅ cada enquete tem o próprio dict
```

Valores mutáveis (listas, dicionários) como padrão seriam **compartilhados** por todos os objetos. O módulo bloqueia esse erro clássico e oferece o `default_factory` como alternativa.

## Exemplo independente do ProgramaBot

```python
from dataclasses import dataclass, field


@dataclass
class Aluno:
    nome: str
    notas: list[float] = field(default_factory=list)

    def media(self) -> float:
        return sum(self.notas) / len(self.notas) if self.notas else 0.0


ana = Aluno("Ana")
ana.notas.append(9.0)
ana.notas.append(8.0)
print(ana)          # Aluno(nome='Ana', notas=[9.0, 8.0])
print(ana.media())  # 8.5
print(ana == Aluno("Ana", [9.0, 8.0]))  # True
```

## Documentação oficial

- <https://docs.python.org/pt-br/3/library/dataclasses.html>
