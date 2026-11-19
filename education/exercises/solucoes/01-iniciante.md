# Soluções: nível iniciante

> Tentou resolver antes de abrir? Existem várias soluções corretas. Se a sua funciona e é fácil de ler, ela está certa. Compare as ideias, não só o código.

## Solução do exercício 1

```python
nome = "Ana"
idade = 20
cidade = "Natal"

print(f"Olá! Meu nome é {nome}, tenho {idade} anos e moro em {cidade}.")
# A conta fica dentro das chaves: o Python calcula antes de montar o texto.
print(f"Daqui a 10 anos terei {idade + 10} anos.")
```

**Comentários:**
- `idade` não tem aspas porque é um número (`int`). Com aspas (`"20"`), `idade + 10` daria erro.
- A f-string aceita expressões dentro de `{}`.

## Solução do exercício 2

```python
primeiro = float(input("Primeiro número: "))
operacao = input("Operação (+ - * /): ").strip()
segundo = float(input("Segundo número: "))

if operacao == "+":
    resultado = primeiro + segundo
elif operacao == "-":
    resultado = primeiro - segundo
elif operacao == "*":
    resultado = primeiro * segundo
elif operacao == "/":
    if segundo == 0:
        resultado = None
        print("Erro: não é possível dividir por zero.")
    else:
        resultado = primeiro / segundo
else:
    resultado = None
    print("Erro: operação inválida.")

if resultado is not None:
    print(f"{primeiro} {operacao} {segundo} = {resultado}")
```

**Comentários:**
- `float(input(...))` converte o texto digitado. Se a pessoa digitar letras, o programa para com `ValueError`. Para tratar isso, veja [Exceções](../../python/08-excecoes.md).
- `None` marca "não há resultado", e o `print` final só acontece quando há um.
- Por que não `eval(f"{primeiro}{operacao}{segundo}")`? Porque `eval` executa qualquer código. Com `if/elif`, só as quatro operações previstas são possíveis.

## Solução do exercício 3

```python
def saudar(nome: str, saudacao: str = "Olá") -> str:
    return f"{saudacao}, {nome}!"


print(saudar("Ana"))
print(saudar("Bruno", "Bom dia"))
print(saudar(saudacao="Boa noite", nome="Carla"))
```

**Comentários:**
- A função **retorna** o texto; quem chama escolhe o que fazer com ele (imprimir, enviar no Discord, salvar...). Isso a torna reutilizável.
- Com argumentos nomeados, a ordem não importa.

## Solução do exercício 4

```python
def classificar_nota(nota: float) -> str:
    if nota < 0 or nota > 10:
        return "Nota inválida"
    if nota >= 9:
        return "Excelente"
    if nota >= 7:
        return "Aprovado"
    if nota >= 5:
        return "Recuperação"
    return "Reprovado"


for nota in (10, 9, 7.5, 5, 4.9, -1, 11):
    print(nota, "->", classificar_nota(nota))
```

**Comentários:**
- Verificar os inválidos primeiro simplifica o resto: depois do primeiro `if`, sabemos que a nota está entre 0 e 10.
- Como cada `if` termina com `return`, as condições seguintes só precisam do limite inferior (`>= 7`), porque os casos `>= 9` já saíram da função. É a mesma técnica de `greeting_for_hour` no `/hello`.
