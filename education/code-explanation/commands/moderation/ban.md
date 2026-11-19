# `bot/commands/moderation/ban.py`: o comando /ban

## 1. Nome e localização

- **Arquivo:** `bot/commands/moderation/ban.py`
- **Comando:** `/ban membro:<@membro> [motivo] [apagar_mensagens_dias:0-7]` (requer "Banir membros")

## 2. Finalidade

Banir um membro depois de uma confirmação por botão, com a opção de apagar as mensagens dele dos últimos dias. O banimento só é desfeito com [`/unban`](unban.md).

## 3. Por que foi criado

Para mostrar como **reaproveitar uma estrutura** que já funciona (a do [`/kick`](kick.md)) e para apresentar um parâmetro numérico com intervalo e valor padrão.

## 4. Como se conecta ao restante do bot

Idêntico ao `/kick`: usa `check_hierarchy`, `build_audit_reason` e `ConfirmView`.

## 5. Bibliotecas utilizadas

- [`discord.py`](../../../libraries/discord-py.md).

## 6. Importações

As mesmas do `/kick`.

## 7. Conceitos de Python utilizados

Os mesmos do `/kick`, mais a **conversão de unidades** com uma constante (`dias * SECONDS_PER_DAY`).

## 8. Variáveis e constantes

- `SECONDS_PER_DAY = 86_400` (24 × 60 × 60).

## 9. Funções

- `Ban.ban(interaction, membro, motivo=None, apagar_mensagens_dias=0)` e `setup(bot)`.

## 10. Parâmetros

- `membro: discord.Member`.
- `motivo: Range[str, 1, 400] | None = None`.
- `apagar_mensagens_dias: Range[int, 0, 7] = 0`: o Discord permite apagar no máximo 7 dias de mensagens ao banir.

## 11. Métodos utilizados

| Método | Explicação |
|---|---|
| `guild.ban(user, reason=, delete_message_seconds=)` | Bane o usuário. `delete_message_seconds` aceita de 0 a 604800 (7 dias). |

O parâmetro antigo `delete_message_days` está **depreciado** no discord.py 2.x. Por isso usamos `delete_message_seconds`.

## 12. Funcionamento do código

```python
await guild.ban(
    membro,
    reason=build_audit_reason(motivo, interaction.user, "ban"),
    delete_message_seconds=apagar_mensagens_dias * SECONDS_PER_DAY,
)
```

Usamos `guild.ban(membro)`, mas `membro.ban()` também existiria. As duas formas fazem a mesma coisa.

## 13. Fluxo de execução

Igual ao do `/kick`, trocando a ação final por `guild.ban(...)`.

## 14. Exemplos práticos

`/ban membro:@Spammer motivo:Divulgação apagar_mensagens_dias:1`

## 15. Erros comuns

- **Querer banir quem não está no servidor**: com o tipo `discord.Member`, só aparecem membros atuais. Para banir por ID, seria preciso um parâmetro de texto, como no `/unban`.

## 16. Como testar

Em um servidor de testes, bana uma conta secundária e desfaça com `/unban`.

## 17. Como modificar

Note como `kick.py` e `ban.py` são quase iguais. Uma melhoria seria criar uma função auxiliar `confirm_action(interaction, texto) -> bool | None` em `views/confirm.py`, que envia a confirmação e devolve o resultado.

## 18. Desafio

Faça a refatoração acima: crie `confirm_action` e use-a no `/kick` e no `/ban`, reduzindo o código repetido. Todos os testes devem continuar passando.
