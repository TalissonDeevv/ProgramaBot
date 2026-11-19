# 01. Sintaxe e variáveis

## Explicação

**Sintaxe** são as regras de escrita de uma linguagem. As principais do Python:

- uma instrução por linha;
- blocos definidos por **recuo de 4 espaços** depois de `:`;
- comentários começam com `#`;
- maiúsculas e minúsculas fazem diferença.

**Variáveis** guardam valores. Em Python, não é preciso declarar o tipo: ele é descoberto pelo valor atribuído.

```python
nome = "Ana"        # texto
idade = 20          # número inteiro
```

### Convenções de nomes (PEP 8)

| Tipo | Estilo | Exemplo |
|---|---|---|
| variáveis e funções | `snake_case` | `latency_ms`, `parse_duration` |
| constantes | `MAIUSCULAS` | `MAX_DURATION` |
| classes | `PascalCase` | `ReminderRepository` |

### `print` e f-strings

```python
nome = "Ana"
idade = 20
print("Nome:", nome)                          # vários valores separados por vírgula
print(f"{nome} tem {idade} anos")             # f-string: valores dentro de {}
print(f"Daqui a 5 anos: {idade + 5}")         # expressões também
```

## Exemplo simples

```python
cidade = "Recife"
print(f"Eu moro em {cidade}.")
```

## Código executável

[`examples/python-basics/01_variaveis.py`](../../examples/python-basics/01_variaveis.py)

## Aplicação no ProgramaBot

Em [`ping.py`](../code-explanation/commands/general/ping.md):

```python
latency_ms = round(self.bot.latency * 1000)
embed = info_embed(f"🏓 Pong! Latência: **{latency_ms} ms**", title="Ping")
```

Uma variável (`latency_ms`) e uma f-string montando o texto.

## Exercício

1. Crie as variáveis `nome`, `linguagem_favorita` e `anos_estudando` e mostre uma frase com f-string.
2. Troque o valor de `anos_estudando` e mostre a frase de novo.
3. O código `Print("oi")` funciona? Por quê?
