# 06. Embeds

## O que são?

**Embeds** são mensagens formatadas, com barra colorida, título, descrição, campos, imagens e rodapé.

```
┃ Autor
┃ **Título**                         [miniatura]
┃ Descrição com **markdown**
┃ Campo 1        Campo 2
┃ valor          valor
┃ Campo inteiro
┃ valor
┃ [imagem grande]
┃ Rodapé • horário
```

## Criando

```python
embed = discord.Embed(title="Título", description="Texto", color=0x5865F2)
embed.add_field(name="Nome", value="Valor", inline=True)
embed.set_author(name="Autor", icon_url="https://...")
embed.set_thumbnail(url="https://...")
embed.set_image(url="https://...")
embed.set_footer(text="Rodapé")
await interaction.response.send_message(embed=embed)
```

## Limites do Discord

| Parte | Limite |
|---|---|
| Título | 256 caracteres |
| Descrição | 4096 caracteres |
| Campos | 25 por embed |
| Nome de campo | 256 caracteres |
| Valor de campo | 1024 caracteres (não pode ser vazio) |
| Rodapé | 2048 caracteres |
| Total do embed | 6000 caracteres |

Ultrapassar algum limite gera `HTTPException: Invalid Form Body`.

## Embeds no ProgramaBot

Todos os embeds passam por [`bot/utils/embeds.py`](../code-explanation/utils/embeds.md), que padroniza cores e rodapé:

```python
from bot.utils.embeds import success_embed, error_embed

await interaction.response.send_message(embed=success_embed("Feito!"))
await interaction.response.send_message(embed=error_embed("Ops!"), ephemeral=True)
```

Um modelo com **todos** os recursos está em [`examples/embeds/embed_completo.py`](../../examples/embeds/embed_completo.py).

## Datas em embeds

- `timestamp=datetime.now(timezone.utc)` mostra o horário no rodapé, no fuso de cada leitor.
- No texto, use `discord.utils.format_dt(data, "R")` para "há 5 minutos".

## Exercício

Resolva o [exercício 9](../exercises/02-basico.md#exercício-9--criar-um-embed).

Documentação: <https://discordpy.readthedocs.io/en/stable/api.html#discord.Embed>
