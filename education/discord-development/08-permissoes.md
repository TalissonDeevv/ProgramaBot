# 08. Permissões e segurança

## Duas pessoas, duas permissões

Em todo comando sensível, verifique **duas** coisas:

1. **Quem usou o comando** pode fazer isso?
2. **O bot** pode fazer isso?

```python
@app_commands.checks.has_permissions(kick_members=True)      # usuário
@app_commands.checks.bot_has_permissions(kick_members=True)  # bot
```

## `default_permissions` vs. `checks.has_permissions`

| | `@app_commands.default_permissions(...)` | `@app_commands.checks.has_permissions(...)` |
|---|---|---|
| Onde age | No Discord: **esconde** o comando | No bot: **verifica** a cada uso |
| Pode ser alterado por | Administradores do servidor (*Integrações*) | Só pelo código |
| Função | Conforto (o menu fica limpo) | Segurança |

Use **os dois** juntos, como em todos os comandos de moderação do ProgramaBot.

## Hierarquia de cargos

Mesmo com a permissão "Banir membros", ninguém pode banir alguém com um cargo **igual ou superior** ao seu, e o bot precisa ter um cargo **acima** do cargo do alvo. O dono do servidor está acima de todos.

O ProgramaBot verifica isso antes de agir, em [`utils/moderation.py`](../code-explanation/utils/moderation.md), para dar mensagens claras.

## Permissões do convite

Ao gerar o link de convite (ver [Criando o bot no Discord](../getting-started/06-criando-o-bot-no-discord.md)), escolha só as permissões necessárias. O ProgramaBot usa:

| Permissão | Para |
|---|---|
| View Channels / Send Messages / Embed Links | Responder |
| Read Message History | `/clear` |
| Manage Messages | `/clear` |
| Add Reactions | exemplos de eventos |
| Kick Members | `/kick` |
| Ban Members | `/ban`, `/unban` |
| Moderate Members | `/timeout` |

> Evite marcar "Administrator". Seguir o **princípio do menor privilégio** limita o estrago caso o token vaze.

## Menções seguras

Qualquer texto vindo de usuários pode conter `@everyone`. Ao reenviar esse texto, bloqueie menções:

```python
await channel.send(texto, allowed_mentions=discord.AllowedMentions.none())
```

Usado em `/say`, `/embed`, `/poll`, `/hello` e outros.

## Outras regras de segurança do projeto

- Nunca usar `eval()` com texto de usuários (veja a [calculadora](../code-explanation/utils/calculator.md)).
- Usar `?` no SQL, nunca f-strings (veja o [banco de dados](../code-explanation/database/reminders.md)).
- Confirmar ações destrutivas (`/kick`, `/ban`).
- Limitar tamanhos (`Range[str, 1, 300]`) e quantidades (10 lembretes por pessoa).
- Guardar o token só no `.env`. Veja [Boas práticas: segurança](../best-practices/01-seguranca.md).

## Exercício

Resolva o [exercício 12](../exercises/03-intermediario.md#exercício-12--criar-um-comando-com-permissões).

Documentação: <https://discordpy.readthedocs.io/en/stable/interactions/api.html#checks> e <https://discord.com/developers/docs/topics/permissions>
