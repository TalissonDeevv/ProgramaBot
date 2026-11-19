# `bot/commands/information/servericon.py`: o comando /servericon

## 1. Nome e localização

- **Arquivo:** `bot/commands/information/servericon.py`
- **Comando:** `/servericon` (só em servidores)

## 2. Finalidade

Mostrar o ícone do servidor em tamanho grande (1024 px), com um botão para abrir a imagem no navegador.

## 3. Por que foi criado

Para ensinar a tratar **dados que podem não existir**: nem todo servidor tem ícone. Nesse caso, `guild.icon` é `None`, e o código precisa lidar com isso.

## 4. Como se conecta ao restante do bot

Mesmo padrão do [`/avatar`](avatar.md); usa `base_embed` e `info_embed`.

## 5. Bibliotecas utilizadas

- [`discord.py`](../../../libraries/discord-py.md).

## 6. Importações

```python
import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import base_embed, info_embed
```

## 7. Conceitos de Python utilizados

- `None` e `is None`.
- Encadeamento de métodos (`guild.icon.with_size(1024).url`).
- Vários `return` antecipados (*guard clauses*).

## 8. Variáveis

- `guild`, `icon_url`, `embed`, `view`.

## 9. Funções

- `ServerIcon.servericon(interaction)` e `setup(bot)`.

## 10. Parâmetros

- Apenas `interaction`.

## 11. Métodos utilizados

| Método | Explicação |
|---|---|
| `guild.icon` | `discord.Asset` ou `None`. |
| `asset.with_size(1024)` | Nova versão do asset com outro tamanho (potência de 2 entre 16 e 4096). |
| `asset.url` | Endereço da imagem. |

## 12. Funcionamento do código

```python
if guild.icon is None:
    await interaction.response.send_message(embed=info_embed("Este servidor ainda não tem um ícone."), ephemeral=True)
    return

icon_url = guild.icon.with_size(1024).url
```

Usamos `is None` (e não `== None`) porque `None` é um objeto único em Python. `is` compara **identidade**, que é a forma recomendada pela PEP 8.

## 13. Fluxo de execução

```
/servericon
 ├─ sem servidor? → aviso → fim
 ├─ sem ícone?    → aviso ephemeral → fim
 └─ embed com imagem 1024px + botão de link
```

## 14. Exemplos práticos

```python
icon_url = guild.icon.with_size(4096).url  # máxima qualidade
```

## 15. Erros comuns

- **`AttributeError: 'NoneType' object has no attribute 'with_size'`**: acontece quando se esquece de verificar se o ícone existe.
- **`ValueError` em `with_size(1000)`**: o tamanho precisa ser uma potência de 2.

## 16. Como testar

Teste em um servidor com ícone e em outro sem ícone.

## 17. Como modificar

Mostre também o **banner** do servidor (`guild.banner`), que também pode ser `None`.

## 18. Desafio

Una os dois cenários em uma função auxiliar `build_image_response(title, asset) -> tuple[discord.Embed, discord.ui.View]` e use-a no `/avatar` e no `/servericon`. É uma refatoração: o comportamento continua igual, mas o código repetido some.
