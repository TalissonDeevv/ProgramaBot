# 📖 Glossário

Termos técnicos em ordem alfabética, explicados de forma simples e, sempre que possível, com um exemplo do ProgramaBot.

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [L](#l) · [M](#m) · [O](#o) · [P](#p) · [R](#r) · [S](#s) · [T](#t) · [V](#v) · [W](#w)

---

## A

**API** (*Application Programming Interface*): um conjunto de regras para um programa conversar com outro. O Discord oferece uma API que o bot usa para enviar mensagens, banir membros etc. O discord.py "traduz" chamadas como `channel.send()` em requisições para essa API.

**Argumento**: o valor passado a uma função quando ela é chamada. Em `latency_status(87)`, `87` é o argumento. Compare com *parâmetro*.

**Assíncrono**: código que pode pausar enquanto espera algo (uma resposta da internet, um temporizador) e deixar outras tarefas rodarem nesse meio-tempo. Todo o ProgramaBot é assíncrono. Veja [Programação assíncrona](../education/python/13-programacao-assincrona.md).

**async**: palavra-chave que cria uma função assíncrona (*corrotina*): `async def ping(self, interaction)`.

**Atributo**: uma variável que pertence a um objeto. Em `self.bot = bot`, `bot` é um atributo do Cog. Em `member.display_name`, `display_name` é um atributo do membro.

**await**: espera o resultado de uma operação assíncrona sem travar o programa: `await interaction.response.send_message(...)`.

## B

**Backend**: a parte de um sistema que roda "nos bastidores", fora da tela do usuário: servidores, bancos de dados, lógica. Um bot é um programa de backend.

**Banco de dados**: um sistema para guardar e consultar dados de forma organizada. O ProgramaBot usa SQLite para os lembretes (`data/programabot.db`).

**Biblioteca**: código pronto, escrito por outras pessoas, que você usa no seu programa. Ex.: `discord.py`, `python-dotenv`. Veja [a diferença entre biblioteca, módulo, pacote e framework](../education/libraries/README.md).

**Booleano** (`bool`): tipo com só dois valores, `True` (verdadeiro) e `False` (falso).

**Bot**: um programa que usa uma conta especial para interagir automaticamente em uma plataforma. O ProgramaBot é um bot do Discord.

**Branch**: uma linha de desenvolvimento paralela no Git, para trabalhar sem afetar a versão principal (`main`).

## C

**Cache**: dados guardados na memória para acesso rápido. O discord.py guarda servidores, canais e membros em cache. `bot.get_channel()` consulta o cache; `bot.fetch_channel()` consulta a API.

**Callback**: uma função que você entrega para ser chamada **depois**, quando algo acontecer. O método `callback` de um botão é executado quando alguém clica ([views/poll.py](../education/code-explanation/views/poll.md)).

**Classe**: um molde para criar objetos. `class Ping(commands.Cog)` define a classe do Cog do `/ping`.

**Código-fonte**: o texto do programa, escrito por pessoas. Os arquivos `.py` em `bot/`.

**Cog**: no discord.py, uma classe que agrupa comandos e eventos relacionados. Cada arquivo de `bot/commands/` tem um Cog. Veja [Cogs e extensões](../education/discord-development/04-cogs-e-extensoes.md).

**Comando**: uma ação que o usuário pede ao bot. Pode ser um *slash command* (`/ping`) ou um comando de *prefixo* (`!ping`).

**Commit**: um registro de alterações no Git, com uma mensagem descrevendo o que mudou.

**Compilação**: tradução do código-fonte inteiro para outra forma (como um executável) antes da execução.

**Constante**: valor que não deve mudar durante o programa. Por convenção, em maiúsculas: `MAX_REMINDERS_PER_USER = 10`.

**Context manager**: um objeto usado com `with`, que garante preparação e limpeza automáticas (ex.: fechar um arquivo). Veja [Context managers](../education/python/12-context-managers.md).

**Corrotina** (*coroutine*): uma função definida com `async def`. Ela pode ser pausada com `await` e retomada depois.

## D

**Dataclass**: uma classe criada com o decorator `@dataclass`, que gera automaticamente o `__init__` e outros métodos. Ex.: `Settings` em [config.py](../education/code-explanation/config.md).

**Decorator**: uma função que modifica outra função, usada com `@`. Ex.: `@app_commands.command(...)` transforma um método em slash command. Veja [Decorators](../education/python/10-decorators.md).

**Defer**: no Discord, avisar que a resposta vai demorar ("pensando..."), ganhando até 15 minutos. Usado no `/clear`.

**Dependência**: uma biblioteca de que o projeto precisa para funcionar. Listadas em `requirements.txt`.

**Dicionário** (`dict`): coleção de pares chave → valor: `{"nome": "Ana"}`.

## E

**Embed**: mensagem formatada do Discord, com título, cor, campos e imagens. Veja [utils/embeds.py](../education/code-explanation/utils/embeds.md).

**Endpoint**: um "endereço" específico de uma API, que realiza uma operação. Ex.: a API do Discord tem um endpoint para criar mensagens em um canal. O discord.py chama esses endpoints por você.

**Ephemeral**: mensagem que só quem usou o comando consegue ver. `send_message(..., ephemeral=True)`.

**Evento**: algo que acontece e que o bot pode "ouvir": uma mensagem nova (`on_message`), um membro entrando (`on_member_join`), o bot ficando pronto (`on_ready`).

**Event loop**: o mecanismo do `asyncio` que alterna entre tarefas assíncronas.

**Exceção**: um erro que acontece durante a execução e pode ser tratado com `try/except`. Ex.: `CalculatorError`.

**Extensão**: no discord.py, um módulo com uma função `setup(bot)`, carregado com `bot.load_extension(...)`.

## F

**f-string**: texto com valores embutidos: `f"Olá, {nome}"`.

**Fixture**: no pytest, uma função que prepara algo para os testes. Ex.: `loaded_bot` em `tests/conftest.py`.

**Fork**: cópia de um repositório do GitHub na sua conta.

**Framework**: uma estrutura que organiza o programa e **chama o seu código** nos momentos certos. O `discord.ext.commands` é um framework: você escreve o comando, e ele decide quando executá-lo.

**Função**: bloco de código com nome, reutilizável, que pode receber parâmetros e retornar um valor: `def roll_dice(sides, amount): ...`.

## G

**Gateway**: a conexão permanente (*WebSocket*) pela qual o Discord envia eventos em tempo real para o bot.

**Git / GitHub**: o Git controla versões do código; o GitHub hospeda repositórios Git na internet.

**Guild**: o nome técnico de "servidor" na API do Discord. Por isso existem `interaction.guild` e `GUILD_ID`.

## H

**Herança**: quando uma classe reaproveita outra. `class ProgramaBot(commands.Bot)` herda tudo de `commands.Bot`.

**Hierarquia de cargos**: a ordem dos cargos de um servidor. Define quem pode moderar quem. Veja [utils/moderation.py](../education/code-explanation/utils/moderation.md).

## I

**Importação**: trazer código de outro módulo: `from bot.utils.embeds import success_embed`.

**Indentação**: os espaços no início da linha. Em Python, ela define os blocos de código.

**Instância**: um objeto criado a partir de uma classe. `Ping(bot)` cria uma instância de `Ping`.

**Intent**: tipo de evento que o bot pede para receber. Algumas são privilegiadas (`members`, `message_content`). Veja [Intents](../education/discord-development/02-intents.md).

**Interação**: o que o Discord envia quando alguém usa um slash command, clica em um botão, escolhe uma opção ou envia um modal (`discord.Interaction`).

**Interpretador**: programa que lê e executa o código. O comando `python` inicia o interpretador.

## J

**JSON**: formato de texto para guardar e trocar dados: `{"facts": ["..."]}`. Usado em `bot/data/facts.json`. Veja [json](../education/libraries/json.md).

## L

**Latência**: tempo de ida e volta de uma comunicação. O `/ping` mostra a latência do bot.

**Lista** (`list`): coleção ordenada e modificável: `["Python", "Java"]`.

**Log**: registro do que o programa fez, com data e nível. Salvo em `logs/programabot.log`.

**Loop** (laço): repetição de um bloco de código (`for`, `while`). Também se refere ao *event loop*.

## M

**Método**: uma função que pertence a uma classe. `interaction.response.send_message()` é um método.

**Modal**: janela de formulário do Discord. Veja [views/embed_modal.py](../education/code-explanation/views/embed_modal.md).

**Módulo**: um arquivo `.py` que pode ser importado.

## O

**Objeto**: algo criado a partir de uma classe, com atributos e métodos. No Python, praticamente tudo é objeto: números, textos, funções.

**Open source** (código aberto): software cujo código-fonte é público e pode ser estudado, modificado e redistribuído, conforme a licença. O ProgramaBot usa a licença MIT.

## P

**Pacote**: pasta com módulos e um `__init__.py`. Ex.: `bot/utils/`.

**Parâmetro**: a variável declarada na definição de uma função, que recebe um argumento. Em `def latency_status(latency_ms)`, `latency_ms` é o parâmetro. Nos slash commands, parâmetros viram campos no Discord.

**Permissão**: autorização para fazer algo em um servidor (expulsar, banir, apagar mensagens). Veja [Permissões](../education/discord-development/08-permissoes.md).

**pip**: o instalador de pacotes do Python: `pip install -r requirements.txt`.

**Prefixo**: caractere que inicia um comando de texto, como o `!` em `!ping`.

**Pull request**: pedido para incorporar suas alterações a um repositório no GitHub.

## R

**Rate limit**: limite de requisições por período imposto pelo Discord. O discord.py o respeita automaticamente.

**Repositório**: a pasta de um projeto controlada pelo Git, com todo o histórico.

**Retorno**: o valor que uma função devolve com `return`.

## S

**Set** (conjunto): coleção sem itens repetidos: `{"a", "b"}`.

**Sintaxe**: as regras de escrita de uma linguagem. Um `SyntaxError` indica que alguma regra foi quebrada.

**Slash command**: comando do Discord que começa com `/`, registrado pelo bot e mostrado em um menu com autocompletar.

**SQL**: linguagem para consultar e modificar bancos de dados: `SELECT * FROM reminders`.

**String** (`str`): texto: `"Olá"`.

**Sync** (sincronização): enviar a lista de slash commands do bot para o Discord (`bot.tree.sync()`).

## T

**Tarefa em segundo plano**: código que roda periodicamente, sem depender de comandos. Ex.: `check_reminders` com `@tasks.loop`.

**Teste automatizado**: código que verifica se outro código funciona. Rode com `python -m pytest`.

**Token**: a "senha" do bot. Quem tem o token controla o bot. Fica só no `.env`. **Nunca compartilhe.**

**Traceback**: o relatório que o Python mostra quando ocorre um erro, indicando arquivos e linhas.

**Tupla** (`tuple`): coleção ordenada que não pode ser alterada: `("Cara", "Coroa")`.

**Type hint**: anotação de tipo: `def dobro(n: int) -> int`. Documenta o código e ajuda o editor.

## V

**Variável**: um nome que guarda um valor: `latency_ms = 87`.

**Variável de ambiente**: configuração fornecida ao programa pelo sistema operacional. O `.env` define as do ProgramaBot.

**venv** (ambiente virtual): uma instalação isolada do Python para um projeto (pasta `.venv/`).

**View**: no discord.py, o contêiner de componentes interativos (botões, menus). Veja [Componentes](../education/discord-development/07-componentes.md).

## W

**WebSocket**: tipo de conexão que fica aberta nos dois sentidos, usada pelo gateway do Discord para enviar eventos em tempo real.
