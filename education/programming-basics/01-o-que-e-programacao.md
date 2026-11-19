# 01. O que é programação?

## O que é um programa?

Um **programa** é uma lista de instruções que um computador segue para realizar uma tarefa. O navegador, o Discord e o próprio ProgramaBot são programas.

O computador é extremamente rápido, mas não "pensa": ele faz **exatamente** o que mandam, na ordem em que mandam. Se a instrução estiver errada, ele vai executar o erro com perfeição.

## O que é programação?

**Programar** é escrever essas instruções. É a atividade de pegar um problema ("quero um bot que dê boas-vindas aos membros") e descrevê-lo em passos tão precisos que uma máquina consiga executá-los.

## O que é um algoritmo?

Um **algoritmo** é uma sequência finita de passos bem definidos para resolver um problema. Algoritmos existem fora da computação: uma receita de bolo é um algoritmo.

**Algoritmo para fazer café:**

1. Encher a chaleira com água.
2. Ligar o fogo.
3. Esperar a água ferver.
4. Colocar o pó no filtro.
5. Despejar a água sobre o pó.
6. Servir.

Um bom algoritmo é **claro** (cada passo tem um único significado), **finito** (termina) e **ordenado**.

## O que é lógica de programação?

É a habilidade de **organizar o raciocínio** em passos que resolvem um problema: decidir a ordem, as condições ("se a água ferver...") e as repetições ("enquanto houver xícaras vazias..."). A lógica é a mesma em qualquer linguagem; só a forma de escrever muda.

## O que é código-fonte?

É o **texto** do programa, escrito por pessoas em uma linguagem de programação. Todos os arquivos `.py` da pasta `bot/` são o código-fonte do ProgramaBot. "Código aberto" (*open source*) significa que esse texto é público, para qualquer pessoa ler, estudar e modificar.

## O que são linguagens de programação?

São idiomas criados para escrever instruções de forma precisa. O computador, no nível mais baixo, só entende números binários (0 e 1). As linguagens ficam no meio do caminho: são legíveis para pessoas e podem ser traduzidas para a máquina.

Exemplos: Python, JavaScript, Java, C, C#, Go, Rust. O ProgramaBot usa **Python**, conhecida pela sintaxe simples e muito usada em automação, ciência de dados, web e ensino.

## Compilação e interpretação

Existem duas formas principais de traduzir código-fonte para algo que o computador executa:

| | Compilação | Interpretação |
|---|---|---|
| Como funciona | Traduz o programa **inteiro** antes, gerando um executável | Traduz e executa **durante** a execução |
| Analogia | Traduzir um livro inteiro e depois entregá-lo | Um intérprete traduzindo uma conversa em tempo real |
| Exemplos | C, Rust, Go | Python, JavaScript |

O Python é chamado de linguagem **interpretada**. Tecnicamente, ele primeiro compila seu código para um formato intermediário (*bytecode*, os arquivos da pasta `__pycache__`) e depois o interpreta. Para quem está começando, basta saber que você escreve o código e o executa com `python arquivo.py`, sem um passo separado de compilação.

## Exemplo simples

Um programa de uma linha:

```python
print("Olá, mundo!")
```

`print` é uma instrução que mostra um texto na tela.

## Código executável

Salve como `ola.py` e execute com `python ola.py`:

```python
# Tudo depois de # é um comentário: o Python ignora.
print("Olá! Este é o meu primeiro programa.")
print("Programas executam as instruções em ordem.")
print("Primeiro esta linha, depois esta.")
```

## Aplicação prática no ProgramaBot

Quando você digita `/ping` no Discord, o ProgramaBot executa um algoritmo:

1. Receber o pedido do Discord.
2. Ler a latência atual.
3. Converter de segundos para milissegundos.
4. Classificar como "Excelente", "Boa" ou "Alta".
5. Montar a mensagem.
6. Enviar a resposta.

Veja esses passos no código real: [`bot/commands/general/ping.py`](../code-explanation/commands/general/ping.md).

## Exercício

1. Escreva, em português, um algoritmo de **5 a 8 passos** para "trocar a lâmpada de um quarto". Seja preciso: o que acontece se a lâmpada nova também não acender?
2. Crie um arquivo `apresentacao.py` que mostre três linhas: seu nome, sua cidade e por que você quer aprender a programar.

Mais exercícios em [exercises/01-iniciante.md](../exercises/01-iniciante.md).
