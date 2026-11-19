# 03. Decisões (condicionais) e repetições (laços)

## Condicionais

### Explicação

Programas precisam **tomar decisões**: "se o usuário tiver permissão, execute; senão, avise". Isso é uma **estrutura condicional**.

Em português estruturado (pseudocódigo):

```
SE nota >= 7 ENTÃO
    mostrar "Aprovado"
SENÃO SE nota >= 5 ENTÃO
    mostrar "Recuperação"
SENÃO
    mostrar "Reprovado"
```

Em Python:

```python
nota = 6
if nota >= 7:
    print("Aprovado")
elif nota >= 5:
    print("Recuperação")
else:
    print("Reprovado")
```

- `if` = se; `elif` = senão, se; `else` = senão.
- Os dois-pontos `:` abrem um bloco.
- O **recuo** (4 espaços) define o que está dentro do bloco. Em Python, isso é obrigatório.

## Repetições

### Explicação

Quando algo precisa acontecer várias vezes, usamos um **laço** (*loop*).

**`for`**: repete para cada item de uma sequência (ou um número conhecido de vezes):

```python
for numero in range(1, 4):   # 1, 2, 3
    print("Volta", numero)
```

**`while`**: repete **enquanto** uma condição for verdadeira:

```python
tentativas = 3
while tentativas > 0:
    print("Tentativas restantes:", tentativas)
    tentativas = tentativas - 1
```

> ⚠️ Se a condição do `while` nunca ficar falsa, o laço é **infinito**. Para parar um programa travado no terminal, pressione `Ctrl+C`.

Controles úteis: `break` sai do laço; `continue` pula para a próxima volta.

## Código executável

```python
# Tabuada com destaque para resultados pares
numero = 7

for multiplicador in range(1, 11):
    resultado = numero * multiplicador
    if resultado % 2 == 0:
        print(f"{numero} x {multiplicador} = {resultado}  (par)")
    else:
        print(f"{numero} x {multiplicador} = {resultado}")

# Contagem regressiva
contador = 5
while contador > 0:
    print(contador)
    contador -= 1      # o mesmo que contador = contador - 1
print("Lançar!")
```

## Aplicação prática no ProgramaBot

- **Condicional**: [`/hello`](../code-explanation/commands/general/hello.md) escolhe "Bom dia", "Boa tarde" ou "Boa noite" com `if`.
- **`for`**: [`main.py`](../code-explanation/main.md) percorre todos os arquivos de comandos para carregá-los.
- **Laço infinito controlado**: a tarefa de lembretes ([`/remind`](../code-explanation/commands/utility/remind.md)) se repete a cada 30 segundos enquanto o bot estiver ligado.

## Exercício

1. Escreva um programa que receba uma idade em uma variável e mostre "criança" (até 11), "adolescente" (12 a 17) ou "adulto" (18 ou mais).
2. Use `for` para mostrar todos os números de 1 a 50 que são múltiplos de 3.
3. Use `while` para somar os números de 1 a 100 e mostrar o total (resposta: 5050).
