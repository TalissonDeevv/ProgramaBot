# 02. Lógica de programação: sequência, variáveis, constantes e operadores

## Sequência lógica

### Explicação

Instruções são executadas **de cima para baixo**, uma de cada vez. A ordem muda o resultado: "colocar o pó e despejar a água" é diferente de "despejar a água e colocar o pó".

### Exemplo simples

```python
print("1. Acordar")
print("2. Tomar café")
print("3. Estudar Python")
```

## Variáveis

### Explicação

Uma **variável** é um nome que guarda um valor na memória, como uma caixa com etiqueta. O valor pode mudar ao longo do programa (por isso "variável").

```python
nome = "Ana"   # cria a caixa "nome" com o valor "Ana"
idade = 17
idade = 18     # o valor mudou
```

O sinal `=` em programação **não** significa "igual" como na matemática. Ele significa **atribuição**: "guarde o valor da direita no nome da esquerda".

Regras para nomes em Python:

- podem ter letras, números e `_`, mas não podem começar com número;
- não podem ter espaços (use `nome_completo`);
- diferenciam maiúsculas de minúsculas (`nome` ≠ `Nome`);
- prefira nomes que expliquem o conteúdo: `quantidade_de_alunos` em vez de `q`.

## Constantes

### Explicação

Uma **constante** é um valor que **não deve mudar** durante o programa. O Python não impede a alteração, mas existe uma convenção: nomes em MAIÚSCULAS indicam constantes.

```python
LIMITE_DE_ALUNOS = 30
PI = 3.14159
```

## Operadores

### Explicação

**Aritméticos** (contas):

| Operador | Significado | Exemplo | Resultado |
|---|---|---|---|
| `+` | soma | `5 + 2` | `7` |
| `-` | subtração | `5 - 2` | `3` |
| `*` | multiplicação | `5 * 2` | `10` |
| `/` | divisão | `5 / 2` | `2.5` |
| `//` | divisão inteira | `5 // 2` | `2` |
| `%` | resto da divisão | `5 % 2` | `1` |
| `**` | potência | `5 ** 2` | `25` |

**Relacionais** (comparações, resultam em `True` ou `False`):

`==` igual · `!=` diferente · `>` maior · `<` menor · `>=` maior ou igual · `<=` menor ou igual

**Lógicos** (combinam condições):

| Operador | Verdadeiro quando... | Exemplo |
|---|---|---|
| `and` | as duas condições são verdadeiras | `idade >= 18 and tem_documento` |
| `or` | pelo menos uma é verdadeira | `e_feriado or e_domingo` |
| `not` | inverte | `not chovendo` |

## Código executável

```python
# Calculadora de média
NOTA_MINIMA = 7.0          # constante

nota1 = 8.5                # variáveis
nota2 = 6.0
media = (nota1 + nota2) / 2

print("Média:", media)
print("Aprovado?", media >= NOTA_MINIMA)
print("Resto de 10 dividido por 3:", 10 % 3)
print("Par?", 10 % 2 == 0)
```

## Aplicação prática no ProgramaBot

- **Constantes**: em [`bot/commands/utility/remind.py`](../code-explanation/commands/utility/remind.md), `MAX_REMINDERS_PER_USER = 10`.
- **Operadores**: o `/ping` usa `round(self.bot.latency * 1000)` para converter segundos em milissegundos.
- **Operadores lógicos**: em [`bot/utils/moderation.py`](../code-explanation/utils/moderation.md), `actor.id != guild_owner_id and actor.top_role <= target.top_role`.
- **Resto da divisão**: a calculadora (`/calculator`) aceita `%`. Experimente `/calculator expressao:17 % 5`.

## Exercício

1. Crie as variáveis `produto`, `preco` e `quantidade`. Calcule e mostre o total.
2. Crie a constante `DESCONTO = 0.1` (10%) e mostre o total com desconto.
3. Usando `%`, mostre se o número `27` é par ou ímpar (o resultado deve ser `True` ou `False`).
4. Descubra o resultado de `True and False`, `True or False` e `not True` antes de executar. Depois, confira.
