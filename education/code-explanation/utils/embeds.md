# `bot/utils/embeds.py`: embeds padronizados

## 1. Nome e localização

- **Arquivo:** `bot/utils/embeds.py`

## 2. Finalidade

Oferecer funções prontas para criar **embeds**, as caixas formatadas que os bots enviam no Discord, com aparência padronizada: cor por tipo de mensagem, rodapé "ProgramaBot • aprenda programando" e horário.

## 3. Por que foi criado

Sem ele, cada comando repetiria o mesmo código:

```python
embed = discord.Embed(title="...", description="...", color=0x57F287, timestamp=...)
embed.set_footer(text="ProgramaBot • aprenda programando")
```

Esse é o princípio **DRY** (*Don't Repeat Yourself*, "não se repita"). Se um dia o rodapé mudar, você altera um único lugar.

## 4. Como se conecta ao restante do bot

Quase todos os comandos importam funções daqui:

- `success_embed`: `/calculator`, `/say`, `/remind`, moderação
- `error_embed`: mensagens de erro em vários comandos e em [`events/errors.py`](../events/errors.md)
- `warning_embed`: confirmação do `/kick` e do `/ban`
- `info_embed`: `/ping`, `/fact`, lembretes
- `parse_hex_color`: o formulário do [`/embed`](../views/embed_modal.md)

## 5. Bibliotecas utilizadas

- [`discord.py`](../../libraries/discord-py.md): a classe `discord.Embed`.
- [`datetime`](../../libraries/datetime.md): o horário do embed.

## 6. Importações

```python
from datetime import datetime, timezone

import discord
```

`timezone.utc` é usado para criar um horário **com fuso definido**. O Discord exibe esse horário convertido para o fuso de quem está lendo.

## 7. Conceitos de Python utilizados

- Funções que retornam objetos.
- Parâmetros com valor padrão (`title: str = "✅ Tudo certo!"`).
- Funções que chamam outras funções (`success_embed` chama `base_embed`).
- Números hexadecimais (`0x5865F2`).
- `str.removeprefix`, `any()` e expressões geradoras.
- Conversão de base: `int("FF0000", 16)`.

## 8. Variáveis e constantes

| Constante | Valor | Uso |
|---|---|---|
| `PRIMARY_COLOR` | `0x5865F2` | Azul do Discord (padrão) |
| `SUCCESS_COLOR` | `0x57F287` | Verde |
| `WARNING_COLOR` | `0xFEE75C` | Amarelo |
| `ERROR_COLOR` | `0xED4245` | Vermelho |
| `INFO_COLOR` | `0x3498DB` | Azul claro |
| `FOOTER_TEXT` | `"ProgramaBot • aprenda programando"` | Rodapé |
| `HEX_DIGITS` | `"0123456789abcdefABCDEF"` | Caracteres válidos em uma cor |

`0x` indica um número em **base 16** (hexadecimal). `0x5865F2` é o mesmo número que `5793266`; só está escrito no formato usado para cores na web (`#5865F2`).

## 9. Funções

| Função | Retorna |
|---|---|
| `base_embed(title, description=None, color=PRIMARY_COLOR)` | Embed com rodapé e horário |
| `success_embed(description, title="✅ Tudo certo!")` | Embed verde |
| `error_embed(description, title="❌ Algo deu errado")` | Embed vermelho |
| `warning_embed(description, title="⚠️ Atenção")` | Embed amarelo |
| `info_embed(description, title="ℹ️ Informação")` | Embed azul |
| `parse_hex_color(value, default=PRIMARY_COLOR)` | Número da cor ou `ValueError` |

## 10. Parâmetros

- `title`: título (até 256 caracteres no Discord).
- `description`: texto principal (até 4096 caracteres). Aceita **markdown** do Discord, como `**negrito**`.
- `color`: um número inteiro.
- `value` (em `parse_hex_color`): texto digitado pelo usuário, como `"#FF0000"`.

## 11. Métodos utilizados

| Método | Explicação |
|---|---|
| `discord.Embed(title=, description=, color=, timestamp=)` | Cria o embed. |
| `embed.set_footer(text=)` | Define o rodapé. |
| `datetime.now(timezone.utc)` | Data e hora atual em UTC. |
| `str.strip()` / `str.removeprefix("#")` | Limpa o texto e remove o `#` do começo, se houver. |
| `int(texto, 16)` | Converte texto hexadecimal em número. |

## 12. Funcionamento do código

```python
def success_embed(description: str, title: str = "✅ Tudo certo!") -> discord.Embed:
    return base_embed(title, description, SUCCESS_COLOR)
```

As funções específicas são "atalhos" para `base_embed` com uma cor fixa.

```python
def parse_hex_color(value: str, default: int = PRIMARY_COLOR) -> int:
    cleaned = value.strip().removeprefix("#")
    if cleaned == "":
        return default
    if len(cleaned) != 6 or any(character not in HEX_DIGITS for character in cleaned):
        raise ValueError("Cor inválida. ...")
    return int(cleaned, 16)
```

`any(...)` devolve `True` se **pelo menos um** caractere não for hexadecimal. Validamos antes de converter para dar uma mensagem clara, em vez de deixar o `int()` falhar.

## 13. Fluxo de execução

```
Comando → success_embed("Mensagem enviada!")
           └─ base_embed("✅ Tudo certo!", "Mensagem enviada!", SUCCESS_COLOR)
               ├─ discord.Embed(...)
               └─ set_footer(...)
         ← embed pronto → interaction.response.send_message(embed=embed)
```

## 14. Exemplos práticos

```python
from bot.utils.embeds import base_embed, error_embed

embed = base_embed("Minha lista", "Itens:")
embed.add_field(name="1", value="Estudar Python", inline=False)
embed.set_thumbnail(url="https://exemplo.com/imagem.png")

aviso = error_embed("Você esqueceu um parâmetro.")
```

## 15. Erros comuns

- **`HTTPException: Invalid Form Body`**: algum limite do Discord foi ultrapassado (título com mais de 256 caracteres, mais de 25 campos, campo com `value` vazio...).
- **Passar a cor como texto**: `color="#FF0000"` não funciona. Use `parse_hex_color` ou `0xFF0000`.
- **Esquecer o `embed=`**: `send_message(embed)` envia o embed como se fosse texto. O correto é `send_message(embed=embed)`.

## 16. Como testar

```bash
python -m pytest tests/test_embeds.py -v
```

Embeds são objetos comuns do Python e podem ser criados sem conexão com o Discord.

## 17. Como modificar

- Mude `FOOTER_TEXT` para personalizar o rodapé do seu bot.
- Crie uma função `study_embed(...)` com uma cor nova para mensagens de estudo.

## 18. Desafio

Altere `base_embed` para aceitar um parâmetro opcional `image_url: str | None = None`. Quando ele for informado, chame `embed.set_image(url=image_url)`. Depois, crie um teste para isso em `tests/test_embeds.py`.

Mais sobre embeds: [discord-development/06-embeds.md](../../discord-development/06-embeds.md).
