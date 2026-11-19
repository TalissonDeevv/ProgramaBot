# 05. Resolução de problemas

## Explicação

Saber os comandos de uma linguagem é metade do caminho. A outra metade é saber **o que fazer diante de um problema novo**. Use este método de 5 passos:

### 1. Entenda o problema

Releia o enunciado e responda: quais são as **entradas**? Qual é a **saída** esperada? Há casos especiais (zero, vazio, negativo)?

### 2. Resolva à mão

Faça o exemplo no papel, sem código. Se você não consegue resolver à mão, ainda não consegue explicar a solução para o computador.

### 3. Escreva os passos em português (pseudocódigo)

### 4. Traduza para código, aos poucos

Escreva um pedaço, execute e confira. Não escreva 50 linhas para testar tudo no final.

### 5. Teste com vários casos

Inclusive os estranhos: zero, número negativo, texto vazio.

## Exemplo simples: "o maior de três números"

**1. Entender:** entradas = 3 números; saída = o maior.

**2. À mão:** entre 4, 9 e 2, olho cada um e guardo o maior que vi até agora: 4 → 9 → 9.

**3. Pseudocódigo:**

```
maior ← primeiro número
para cada número restante:
    se número > maior: maior ← número
mostrar maior
```

**4 e 5. Código e testes:**

```python
def maior_de_tres(a, b, c):
    maior = a
    for numero in (b, c):
        if numero > maior:
            maior = numero
    return maior


print(maior_de_tres(4, 9, 2))    # 9
print(maior_de_tres(-1, -5, -3)) # -1
print(maior_de_tres(7, 7, 7))    # 7
```

(O Python já tem `max(4, 9, 2)`, mas construir a lógica é o objetivo do treino.)

## Quando o código dá erro

1. **Leia a mensagem de erro inteira**, de baixo para cima. A última linha diz o tipo do erro; as de cima mostram o arquivo e a linha.
2. **Coloque `print()`** para ver o valor das variáveis no meio do caminho.
3. **Explique o código em voz alta**, linha por linha (a técnica do "pato de borracha"). Muitas vezes você percebe o erro no meio da explicação.
4. **Pesquise a mensagem de erro** na internet. Quase sempre alguém já passou pelo mesmo problema.

Erros comuns de iniciantes:

| Erro | Causa provável |
|---|---|
| `SyntaxError` | Faltou `:`, parêntese ou aspas |
| `IndentationError` | Recuo errado |
| `NameError: name 'x' is not defined` | Nome digitado errado, ou variável usada antes de ser criada |
| `TypeError: can only concatenate str (not "int") to str` | Somou texto com número; use f-string ou `str()` |
| `ValueError: invalid literal for int()` | Tentou converter um texto que não é número |

## Aplicação prática no ProgramaBot

O comando [`/remind`](../code-explanation/commands/utility/remind.md) foi construído assim:

1. **Entender:** entrada = um tempo (`10m`) e uma mensagem; saída = um aviso no horário certo, mesmo que o bot reinicie.
2. **Dividir:** interpretar o tempo ([`time_parser.py`](../code-explanation/utils/time_parser.md)) → salvar ([`reminders.py`](../code-explanation/database/reminders.md)) → verificar periodicamente → entregar.
3. **Testar cada parte separadamente:** veja `tests/test_time_parser.py` e `tests/test_reminders.py`.

## Exercício

Use o método de 5 passos (escreva os passos 1 a 3 em comentários antes do código):

1. Dada uma lista de notas, mostre quantas estão acima da média da turma.
2. Dado um texto, conte quantas vogais ele tem.
3. Dado um número, diga se ele é primo (divisível só por 1 e por ele mesmo).
