# Exercícios: nível básico

## Exercício 5 — Criar um loop

- **Objetivo:** usar `for`, `while` e acumuladores.
- **Nível:** básico
- **Conteúdos necessários:** [repetições](../python/05-repeticoes.md)
- **Arquivos envolvidos:** `estudos/ex05.py`

**Enunciado:**
1. Com `for`, mostre a tabuada de 1 a 10 de um número.
2. Com `while`, simule uma contagem regressiva de 10 até 1 e mostre "Bot online!" no final.
3. Some todos os números pares de 1 a 100 (resposta: 2550).

**Dicas:** `range(início, fim, passo)`; o `fim` não é incluído.

**Resultado esperado:** a tabuada, a contagem, `Bot online!` e `Soma dos pares: 2550`.

➡️ [Solução](solucoes/02-basico.md#solução-do-exercício-5)

---

## Exercício 6 — Criar uma lista de usuários

- **Objetivo:** manipular listas e dicionários.
- **Nível:** básico
- **Conteúdos necessários:** [coleções](../python/03-colecoes.md), [compreensões](../python/11-iteradores-e-compreensoes.md)
- **Arquivos envolvidos:** `estudos/ex06.py`

**Enunciado:** crie uma lista de dicionários representando usuários de um servidor:

```python
usuarios = [
    {"nome": "Ana", "cargo": "Moderador", "mensagens": 120},
    {"nome": "Bruno", "cargo": "Membro", "mensagens": 45},
    {"nome": "Carla", "cargo": "Membro", "mensagens": 300},
]
```

Então:
1. adicione um novo usuário;
2. mostre o nome de todos os usuários;
3. mostre apenas os que têm mais de 100 mensagens;
4. mostre o total de mensagens;
5. mostre o usuário mais ativo.

**Dicas:** `lista.append(...)`; `max(usuarios, key=lambda u: u["mensagens"])`.

**Resultado esperado (com Diego, 80 mensagens):** nomes `Ana, Bruno, Carla, Diego`; ativos `Ana, Carla`; total `545`; mais ativo `Carla`.

➡️ [Solução](solucoes/02-basico.md#solução-do-exercício-6)

---

## Exercício 7 — Criar o comando /hello do zero

- **Objetivo:** criar o primeiro slash command completo.
- **Nível:** básico
- **Conteúdos necessários:** [Cogs e extensões](../discord-development/04-cogs-e-extensoes.md), [interações](../discord-development/05-interacoes-e-respostas.md), [criando um comando](../discord-development/10-criando-um-novo-comando.md)
- **Arquivos envolvidos:** novo `bot/commands/fun/ola.py`; `bot/views/help_menu.py`; nova `education/code-explanation/commands/fun/ola.md`; `tests/test_extensions.py`

**Enunciado:** sem copiar o `hello.py`, crie o comando `/ola` com um parâmetro opcional `nome`. Ele deve responder `Olá, <nome>!`, ou `Olá, <nome de exibição>!` se o nome não for informado. Bloqueie menções na resposta.

**Dicas:**
- A estrutura mínima é: imports → classe Cog → `@app_commands.command` → `async def` → `setup`.
- Parâmetro opcional: `nome: str | None = None`.
- Não esqueça o `@app_commands.describe(nome=...)`.
- Rode `python -m pytest` e leia **todas** as falhas: elas dizem o que falta.

**Resultado esperado:** `/ola` → `Olá, Ana!`; `/ola nome:@everyone` → mostra o texto sem notificar ninguém; todos os testes passando.

➡️ [Solução](solucoes/02-basico.md#solução-do-exercício-7)

---

## Exercício 8 — Modificar o comando /ping

- **Objetivo:** alterar um comando existente e editar uma resposta.
- **Nível:** básico
- **Conteúdos necessários:** [interações e respostas](../discord-development/05-interacoes-e-respostas.md)
- **Arquivos envolvidos:** `bot/commands/general/ping.py` e `education/code-explanation/commands/general/ping.md`

**Enunciado:** faça o `/ping` mostrar **duas** medidas:
1. a latência do gateway (a atual);
2. o tempo que a API levou para receber a resposta.

**Dicas:**
- `import time`; `inicio = time.perf_counter()`.
- Envie a resposta, calcule `(time.perf_counter() - inicio) * 1000`, adicione um campo ao embed e use `await interaction.edit_original_response(embed=embed)`.
- Atualize a documentação do arquivo!

**Resultado esperado:** um embed com "Gateway: 85 ms" e "API: 140 ms" (os valores variam).

➡️ [Solução](solucoes/02-basico.md#solução-do-exercício-8)

---

## Exercício 9 — Criar um embed

- **Objetivo:** montar um embed completo com dados do Discord.
- **Nível:** básico
- **Conteúdos necessários:** [embeds](../discord-development/06-embeds.md), [utils/embeds](../code-explanation/utils/embeds.md)
- **Arquivos envolvidos:** novo `bot/commands/fun/perfil.py` + documentação, catálogo do `/help` e testes

**Enunciado:** crie `/perfil`, que mostre um embed "cartão de estudante" de quem usou o comando, com:
- título `Cartão de estudante de <nome>`;
- avatar como miniatura;
- campos: "Membro desde" (data relativa da conta), "Linguagem favorita" (parâmetro opcional, padrão "Python") e "Nível" (parâmetro com as escolhas Iniciante, Básico e Intermediário).

**Dicas:**
- Use `base_embed`.
- Escolhas fixas: `@app_commands.choices(nivel=[app_commands.Choice(name="Iniciante", value="iniciante"), ...])` e o tipo `nivel: app_commands.Choice[str]`.
- Data: `discord.utils.format_dt(interaction.user.created_at, "R")`.

**Resultado esperado:** um embed com miniatura e três campos.

➡️ [Solução](solucoes/02-basico.md#solução-do-exercício-9)
