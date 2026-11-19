# `bot/commands/information/avatar.py`: o comando /avatar

## 1. Nome e localização

- **Arquivo:** `bot/commands/information/avatar.py`
- **Comando:** `/avatar [usuario]`

## 2. Finalidade

Mostrar a foto de perfil de um usuário (ou de quem usou o comando) em tamanho grande, com um botão para abrir a imagem no navegador.

## 3. Por que foi criado

Para mostrar como receber um **usuário do Discord como parâmetro**. O Discord exibe uma lista de pessoas para escolher, e o discord.py entrega um objeto pronto, com nome, ID, avatar etc.

## 4. Como se conecta ao restante do bot

Usa `base_embed` de [`utils/embeds.py`](../../utils/embeds.md). O padrão "embed com imagem + botão de link" se repete no [`/servericon`](servericon.md).

## 5. Bibliotecas utilizadas

- [`discord.py`](../../../libraries/discord-py.md).

## 6. Importações

```python
import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import base_embed
```

## 7. Conceitos de Python utilizados

- Parâmetro opcional com tipo de objeto (`discord.User | None = None`).
- `or` para valor padrão.
- Acesso a atributos encadeados (`target.display_avatar.url`).

## 8. Variáveis

- `target`: o usuário escolhido ou o autor.
- `avatar_url`: o endereço da imagem.
- `embed`, `view`: a resposta.

## 9. Funções

- `Avatar.avatar(interaction, usuario=None)` e `setup(bot)`.

## 10. Parâmetros

- `usuario: discord.User | None = None`: com o tipo `discord.User`, o Discord mostra um seletor de usuários. Dentro de servidores, o discord.py entrega um `discord.Member` (que tem tudo de `User` e mais informações do servidor). Por isso o comando funciona tanto em servidores quanto em mensagens diretas.

## 11. Métodos e atributos utilizados

| Atributo/método | Explicação |
|---|---|
| `user.display_avatar` | O avatar exibido: o do servidor (se a pessoa definiu um), o global ou o padrão do Discord. Nunca é `None`. |
| `user.avatar` | Só o avatar global; pode ser `None`. Por isso preferimos `display_avatar`. |
| `asset.url` | Endereço da imagem. |
| `user.display_name` | Nome exibido. |
| `embed.set_image(url=)` | Imagem grande no embed. |

## 12. Funcionamento do código

```python
target = usuario or interaction.user
avatar_url = target.display_avatar.url
```

Se ninguém for escolhido, `usuario` é `None` e usamos quem executou o comando.

```python
view = discord.ui.View()
view.add_item(discord.ui.Button(label="Abrir imagem no navegador", url=avatar_url))
```

O mesmo padrão de botão de link visto no [`/about`](../general/about.md).

## 13. Fluxo de execução

```
/avatar usuario:@Ana → target = Ana → embed com set_image(avatar) + botão → resposta
/avatar             → target = quem executou
```

## 14. Exemplos práticos

Para pedir um tamanho específico de imagem:

```python
avatar_url = target.display_avatar.with_size(256).url
```

O tamanho precisa ser uma potência de 2 entre 16 e 4096.

## 15. Erros comuns

- **`AttributeError: 'NoneType' object has no attribute 'url'`**: aparece quando se usa `user.avatar.url` com alguém sem foto. Use `display_avatar`.

## 16. Como testar

Use `/avatar` sem parâmetro, com outro membro e com um bot.

## 17. Como modificar

Mostre também o banner do perfil. Ele exige buscar o usuário completo com `await self.bot.fetch_user(target.id)`, e o atributo `.banner` pode ser `None`.

## 18. Desafio

Adicione um parâmetro `formato` com as escolhas `png`, `jpg` e `webp` e use `target.display_avatar.with_format(formato.value)`. Atenção: avatares animados (GIF) só aceitam alguns formatos. Leia a documentação de [`discord.Asset`](https://discordpy.readthedocs.io/en/stable/api.html#discord.Asset).
