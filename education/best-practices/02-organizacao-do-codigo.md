# 02. Organização do código

## Estrutura de pastas por responsabilidade

```
bot/
├── main.py, config.py   ← inicialização e configuração
├── commands/<categoria>/ ← um comando por arquivo
├── events/              ← um evento por arquivo
├── views/               ← componentes visuais (botões, menus, modais)
├── database/            ← acesso a dados (SQL só aqui)
└── utils/               ← funções reutilizáveis e sem estado
```

Pergunta-guia: **"se eu quiser mudar X, em quantos arquivos preciso mexer?"** O ideal é um.

## Separe a lógica do Discord

A regra mais útil do projeto. Compare:

```python
# ❌ Lógica misturada com o Discord: só dá para testar usando o Discord
async def dice(self, interaction, lados: int):
    resultados = [random.randint(1, lados) for _ in range(3)]
    await interaction.response.send_message(str(resultados))

# ✅ Lógica separada: roll_dice pode ser testada com pytest
def roll_dice(sides: int, amount: int) -> list[int]: ...

async def dice(self, interaction, lados: int, quantidade: int):
    results = roll_dice(lados, quantidade)
    await interaction.response.send_message(...)
```

Exemplos no projeto: `calculate`, `parse_duration`, `check_hierarchy`, `parse_poll_options`, `PollState`, `greeting_for_hour`, `ReminderRepository`.

## Nomes

- Nomes descritivos: `remind_at` em vez de `t`; `MAX_REMINDERS_PER_USER` em vez de `10` solto no código.
- Siga a [PEP 8](https://peps.python.org/pep-0008/): `snake_case` para funções e variáveis, `PascalCase` para classes, `MAIUSCULAS` para constantes.
- No ProgramaBot, o código usa nomes em inglês (padrão da indústria), enquanto **parâmetros dos comandos**, mensagens, comentários e docstrings ficam em português, para quem usa e estuda o bot.

## Funções pequenas e cláusulas de guarda

Prefira várias verificações que saem cedo (`if problema: return`) a muitos `if` aninhados. Veja [`check_hierarchy`](../code-explanation/utils/moderation.md).

## Sem números mágicos

```python
# ❌
if delay > timedelta(days=7): ...

# ✅
MAX_DURATION = timedelta(days=7)
if delay > MAX_DURATION: ...
```

## Docstrings e comentários

- **Docstring** (`"""..."""`): diz **o que** a função faz e o que ela recebe e devolve.
- **Comentário** (`#`): explica **por que** algo é feito de um jeito não óbvio.
- Não comente o óbvio (`x = x + 1  # soma 1 em x`).

## Imports organizados

Biblioteca padrão → externos → projeto, com uma linha em branco entre os grupos.

## Não repita (DRY), mas sem exagero

Repetiu o mesmo código três vezes? Crie uma função. Mas uma abstração ruim é pior que um pouco de repetição: o `/kick` e o `/ban` repetem a estrutura de propósito, para que cada arquivo seja fácil de ler sozinho (e a refatoração fica como [desafio](../code-explanation/commands/moderation/ban.md#18-desafio)).
