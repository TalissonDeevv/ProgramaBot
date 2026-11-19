# `bot/commands/moderation/kick.py`: o comando /kick

## 1. Nome e localização

- **Arquivo:** `bot/commands/moderation/kick.py`
- **Comando:** `/kick membro:<@membro> [motivo]` (requer "Expulsar membros")

## 2. Finalidade

Expulsar um membro do servidor depois de uma **confirmação por botão**. A pessoa expulsa pode voltar com um novo convite.

## 3. Por que foi criado

Para mostrar o fluxo completo de um comando de moderação responsável:

1. permissões do usuário **e** do bot;
2. regras de hierarquia de cargos;
3. confirmação antes da ação;
4. motivo registrado no Registro de Auditoria;
5. tratamento de falhas do Discord.

## 4. Como se conecta ao restante do bot

```
check_hierarchy, build_audit_reason → utils/moderation.py
ConfirmView                         → views/confirm.py
embeds                              → utils/embeds.py
```

O [`/ban`](ban.md) segue exatamente a mesma estrutura.

## 5. Bibliotecas utilizadas

- [`discord.py`](../../../libraries/discord-py.md).

## 6. Importações

```python
import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import error_embed, info_embed, success_embed, warning_embed
from bot.utils.moderation import MAX_REASON_LENGTH, build_audit_reason, check_hierarchy
from bot.views.confirm import ConfirmView
```

## 7. Conceitos de Python utilizados

- **Fluxo com vários pontos de saída** (`return`).
- **Esperar um evento** com `await view.wait()`.
- **Três estados** (`None`, `True`, `False`) e a diferença entre `is None` e `not`.
- **`try/except` em torno de uma chamada externa.**

## 8. Variáveis

- `guild`: o servidor.
- `problem`: mensagem de bloqueio ou `None`.
- `view`: a `ConfirmView`.

## 9. Funções

- `Kick.kick(interaction, membro, motivo=None)` e `setup(bot)`.

## 10. Parâmetros

- `membro: discord.Member`: obrigatório. O Discord mostra a lista de membros do servidor.
- `motivo: Range[str, 1, 400] | None = None`: opcional.

## 11. Métodos utilizados

| Método | Explicação |
|---|---|
| `guild.me` | O bot como membro, para conferir a posição do cargo. |
| `view.wait()` | Espera o clique ou o fim do tempo. |
| `interaction.edit_original_response(embed=, view=None)` | Troca a mensagem de confirmação pelo resultado. `view=None` remove os botões. |
| `membro.kick(reason=)` | Expulsa. Lança `discord.Forbidden` ou `discord.HTTPException` se falhar. |

## 12. Funcionamento do código

```python
if guild is None or not isinstance(interaction.user, discord.Member):
    return
```

Garante que estamos em um servidor e que `interaction.user` é um `Member` (com cargos).

```python
await view.wait()

if view.confirmed is None:      # ninguém clicou em 30 s
    ...
if not view.confirmed:          # clicou em Cancelar (False)
    ...
```

A ordem importa: `not None` também é `True`. Por isso verificamos `is None` **antes** de `not view.confirmed`.

```python
try:
    await membro.kick(reason=build_audit_reason(motivo, interaction.user, "kick"))
except discord.HTTPException:
    ...
```

Mesmo com todas as verificações, algo ainda pode dar errado (uma permissão removida no meio do processo, uma instabilidade do Discord). `discord.Forbidden` é uma subclasse de `HTTPException`, então este `except` cobre os dois casos.

## 13. Fluxo de execução

```
/kick membro:@João motivo:"spam"
 ├─ permissões ✔
 ├─ check_hierarchy ✔
 ├─ mensagem ephemeral "Tem certeza?" + [Confirmar] [Cancelar]
 ├─ await view.wait()
 │    ├─ Confirmar → membro.kick(reason="spam | por Maria via /kick")
 │    │               → "👢 João foi expulso(a)."
 │    ├─ Cancelar  → "Ação cancelada."
 │    └─ 30 s      → "Tempo esgotado."
```

## 14. Exemplos práticos

Avisar o membro por mensagem direta **antes** de expulsar (depois que ele sai, o bot não compartilha mais servidores com ele e pode não conseguir enviar DM):

```python
try:
    await membro.send(f"Você foi expulso de {guild.name}. Motivo: {motivo or 'não informado'}")
except discord.HTTPException:
    pass  # a pessoa pode ter DMs fechadas
```

## 15. Erros comuns

- **"Meu cargo está abaixo..."**: arraste o cargo do bot para cima na lista de cargos do servidor.
- **Comando invisível**: quem não tem "Expulsar membros" não vê o comando (`default_permissions`).

## 16. Como testar

Use um servidor de testes e uma conta secundária. Teste: confirmar, cancelar, esperar, tentar expulsar a si mesmo e um membro com cargo superior.

```bash
python -m pytest tests/test_moderation.py tests/test_extensions.py -k "hierarchy or moderation" -v
```

## 17. Como modificar

Implemente o aviso por DM do exemplo acima, logo depois da confirmação.

## 18. Desafio

Registre cada expulsão em um canal de logs: crie `MOD_LOG_CHANNEL_ID` no `.env` (seguindo o guia de [config.md](../../config.md#17-como-modificar)) e envie um embed com moderador, membro e motivo.
