# Exercícios: nível iniciante

## Exercício 1 — Criar uma variável com o seu nome

- **Objetivo:** escrever e executar o primeiro programa com variáveis.
- **Nível:** iniciante
- **Conteúdos necessários:** [variáveis](../programming-basics/02-logica-de-programacao.md), `print`, [f-strings](../python/01-sintaxe-e-variaveis.md)
- **Arquivos envolvidos:** crie `estudos/ex01.py` (a pasta `estudos/` é sua; ela pode ficar fora do Git)

**Enunciado:** crie as variáveis `nome`, `idade` e `cidade` com os seus dados e mostre a frase: `Olá! Meu nome é ___, tenho ___ anos e moro em ___.` Depois, mostre quantos anos você terá daqui a 10 anos.

**Dicas:**
- Texto vai entre aspas; números, não.
- Use uma f-string: `f"Olá, {nome}"`.

**Resultado esperado:**

```
Olá! Meu nome é Ana, tenho 20 anos e moro em Natal.
Daqui a 10 anos terei 30 anos.
```

➡️ [Solução](solucoes/01-iniciante.md#solução-do-exercício-1)

---

## Exercício 2 — Calculadora simples

- **Objetivo:** usar entrada, conversão de tipos e operadores.
- **Nível:** iniciante
- **Conteúdos necessários:** [entrada e saída](../programming-basics/04-funcoes-entrada-e-saida.md), [tipos](../python/02-tipos-de-dados.md), [condicionais](../python/04-condicionais.md)
- **Arquivos envolvidos:** `estudos/ex02.py`

**Enunciado:** peça dois números e uma operação (`+`, `-`, `*` ou `/`) ao usuário. Mostre o resultado. Se a operação for inválida, ou se houver divisão por zero, mostre uma mensagem de erro.

**Regra:** **não use `eval()`**. Entenda o motivo em [utils/calculator](../code-explanation/utils/calculator.md#3-por-que-foi-criado).

**Dicas:**
- `input()` devolve texto: converta com `float()`.
- Use `if`/`elif` para cada operação.

**Resultado esperado:**

```
Primeiro número: 10
Operação (+ - * /): /
Segundo número: 4
10.0 / 4.0 = 2.5
```

➡️ [Solução](solucoes/01-iniciante.md#solução-do-exercício-2)

---

## Exercício 3 — Função de saudação

- **Objetivo:** criar e chamar funções com parâmetros, valor padrão e retorno.
- **Nível:** iniciante
- **Conteúdos necessários:** [funções](../python/06-funcoes.md)
- **Arquivos envolvidos:** `estudos/ex03.py`

**Enunciado:** crie `saudar(nome, saudacao="Olá")`, que **retorne** (e não imprima) a frase `"<saudacao>, <nome>!"`. Chame-a três vezes: só com o nome, com uma saudação personalizada e usando argumentos nomeados.

**Dicas:**
- `return` devolve o valor; quem chama decide se vai imprimir.

**Resultado esperado:**

```
Olá, Ana!
Bom dia, Bruno!
Boa noite, Carla!
```

➡️ [Solução](solucoes/01-iniciante.md#solução-do-exercício-3)

---

## Exercício 4 — Estrutura condicional

- **Objetivo:** usar `if`, `elif` e `else` com faixas de valores.
- **Nível:** iniciante
- **Conteúdos necessários:** [condicionais](../python/04-condicionais.md)
- **Arquivos envolvidos:** `estudos/ex04.py`; para comparar, [`bot/commands/general/hello.py`](../../bot/commands/general/hello.py)

**Enunciado:** crie a função `classificar_nota(nota)`, que retorne:

| Nota | Resultado |
|---|---|
| menor que 0 ou maior que 10 | `"Nota inválida"` |
| 9 a 10 | `"Excelente"` |
| 7 a 8.9 | `"Aprovado"` |
| 5 a 6.9 | `"Recuperação"` |
| abaixo de 5 | `"Reprovado"` |

Teste com: `10, 9, 7.5, 5, 4.9, -1, 11`.

**Dicas:**
- Verifique os valores inválidos **primeiro**.
- Compare com a função `greeting_for_hour` do `/hello`, que resolve um problema muito parecido.

**Resultado esperado:** `Excelente, Excelente, Aprovado, Recuperação, Reprovado, Nota inválida, Nota inválida`.

➡️ [Solução](solucoes/01-iniciante.md#solução-do-exercício-4)
