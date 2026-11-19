# `bot/utils/moderation.py`: regras de hierarquia da moderação

## 1. Nome e localização

- **Arquivo:** `bot/utils/moderation.py`
- **Usado por:** [`/kick`](../commands/moderation/kick.md), [`/ban`](../commands/moderation/ban.md), [`/timeout`](../commands/moderation/timeout.md) e [`/unban`](../commands/moderation/unban.md)

## 2. Finalidade

Verificar, **antes** de executar uma ação de moderação, se ela é permitida pelas regras de cargos do Discord, e montar o texto que vai para o Registro de Auditoria.

## 3. Por que foi criado

No Discord, cargos (*roles*) têm posições. Mesmo quem tem a permissão "Expulsar membros" não pode expulsar alguém com um cargo igual ou superior ao seu. O bot também está sujeito a essa regra: ele precisa ter um cargo **acima** do cargo do alvo.

Se o bot simplesmente tentasse a ação, o Discord devolveria um erro genérico (`403 Forbidden`). Verificando antes, conseguimos dizer **exatamente** qual foi o problema.

## 4. Como se conecta ao restante do bot

```python
problem = check_hierarchy(interaction.user, membro, guild.me, guild.owner_id)
if problem:
    await interaction.response.send_message(embed=error_embed(problem), ephemeral=True)
    return
```

Esse trecho aparece em `kick.py`, `ban.py` e `timeout.py`. A função `build_audit_reason` é usada nesses três arquivos e também em `unban.py`.

## 5. Bibliotecas utilizadas

- [`discord.py`](../../libraries/discord-py.md): usado apenas nas *type hints* (`discord.Member`).

## 6. Importações

```python
import discord
```

## 7. Conceitos de Python utilizados

- **Retorno "erro ou `None`"**: a função devolve um texto explicando o problema, ou `None` se estiver tudo certo. O tipo `str | None` documenta isso.
- **Cláusulas de guarda**: vários `if ... return` seguidos, cada um tratando um caso. É mais legível que `if/elif` aninhados.
- **Comparação de objetos**: `actor.top_role <= target.top_role`. A classe `discord.Role` implementa os operadores de comparação a partir da posição do cargo.
- **Fatiamento de strings**: `texto[:400]` pega até 400 caracteres.
- **Operador `or` com valor padrão**: `reason or DEFAULT_REASON`.
- **Duck typing**: a função só usa `.id` e `.top_role`. Qualquer objeto com esses atributos funciona, e é isso que os testes aproveitam.

## 8. Variáveis e constantes

- `MAX_REASON_LENGTH = 400`: o Discord aceita motivos de até 512 caracteres. Reservamos o restante para o sufixo `| por ... via /...`.
- `DEFAULT_REASON = "Nenhum motivo informado."`

## 9. Funções

### `check_hierarchy(actor, target, bot_member, guild_owner_id) -> str | None`

Verifica, nesta ordem:

1. O alvo é a própria pessoa? → bloqueia.
2. O alvo é o bot? → bloqueia.
3. O alvo é o dono do servidor? → bloqueia (ninguém pode moderar o dono).
4. Quem executou **não** é o dono e tem cargo menor ou igual ao do alvo? → bloqueia.
5. O cargo do bot é menor ou igual ao do alvo? → bloqueia, explicando como corrigir.
6. Se passou por tudo → `None` (permitido).

### `build_audit_reason(reason, moderator, command_name) -> str`

Monta, por exemplo: `Spam no chat | por Maria via /kick`.

## 10. Parâmetros

- `actor`: quem executou o comando (`interaction.user`).
- `target`: o membro que vai sofrer a ação.
- `bot_member`: o bot como membro do servidor (`guild.me`), necessário para saber o cargo dele.
- `guild_owner_id`: ID do dono (`guild.owner_id`).
- `reason`: motivo digitado (pode ser `None`).
- `moderator`: quem executou. Convertido em texto com f-string.
- `command_name`: nome do comando, sem a barra.

## 11. Métodos e atributos utilizados

| Atributo | Explicação |
|---|---|
| `member.id` | ID único do usuário. |
| `member.top_role` | O cargo mais alto do membro. |
| `guild.me` | O próprio bot como `Member` daquele servidor. |
| `guild.owner_id` | ID do dono do servidor. |
| `str.strip()` | Remove espaços extras do motivo. |

## 12. Funcionamento do código

```python
if actor.id != guild_owner_id and actor.top_role <= target.top_role:
    return "Você não pode moderar alguém com cargo igual ou superior ao seu."
```

O operador `and` só avalia a segunda parte se a primeira for verdadeira. Se o autor for o dono, ele pode moderar qualquer pessoa, então a comparação de cargos nem acontece.

```python
text = (reason or DEFAULT_REASON).strip()[:MAX_REASON_LENGTH]
return f"{text} | por {moderator} via /{command_name}"
```

Se `reason` for `None` ou vazio, `or` escolhe `DEFAULT_REASON`.

## 13. Fluxo de execução

```
/kick membro:@João
 └─ check_hierarchy(Maria, João, Bot, dono_id)
     ├─ João é Maria?               não
     ├─ João é o bot?               não
     ├─ João é o dono?              não
     ├─ cargo Maria <= cargo João?  não
     ├─ cargo Bot <= cargo João?    não
     └─ None → pode prosseguir
```

## 14. Exemplos práticos

Os testes usam objetos simples em vez de membros reais:

```python
from types import SimpleNamespace
from bot.utils.moderation import check_hierarchy

maria = SimpleNamespace(id=2, top_role=30)
joao = SimpleNamespace(id=3, top_role=10)
bot = SimpleNamespace(id=99, top_role=50)

print(check_hierarchy(maria, joao, bot, guild_owner_id=1))  # None
print(check_hierarchy(joao, maria, bot, guild_owner_id=1))  # mensagem de bloqueio
```

## 15. Erros comuns

- **"Meu cargo está abaixo..."** mesmo com permissão de administrador: nas configurações do servidor, em *Cargos*, arraste o cargo do bot para **cima** do cargo dos membros que ele precisa moderar.
- **Esquecer de verificar o retorno**: `check_hierarchy` apenas **informa**; quem chama precisa interromper o comando com `return`.

## 16. Como testar

```bash
python -m pytest tests/test_moderation.py -v
```

## 17. Como modificar

Para impedir também a moderação de **outros bots**, adicione no início da função:

```python
if target.bot:
    return "Não é permitido moderar bots com este comando."
```

Lembre-se de atualizar os testes, porque os objetos falsos precisarão do atributo `bot`.

## 18. Desafio

Crie a função `can_receive_timeout(target) -> str | None`, que bloqueie castigos em membros com a permissão de administrador (`target.guild_permissions.administrator`). Use-a no `/timeout` para mostrar uma mensagem específica.
