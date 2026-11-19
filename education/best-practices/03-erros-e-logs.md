# 03. Erros e logs

## Capture só o que você sabe tratar

```python
# ❌ Esconde qualquer bug: o comando "funciona", mas ninguém sabe que algo deu errado
try:
    result = calculate(expressao)
except Exception:
    result = 0

# ✅ Trata o erro esperado; bugs seguem para o tratador central e vão para o log
try:
    result = calculate(expressao)
except CalculatorError as error:
    await interaction.response.send_message(embed=error_embed(str(error)), ephemeral=True)
    return
```

**Quando capturar `Exception` é correto:** em pontos onde um erro não pode parar todo o resto, **registrando** o erro. Exemplo: a tarefa de lembretes, que não pode parar por causa de um único lembrete com problema ([remind.py](../code-explanation/commands/utility/remind.md)).

## Exceções específicas primeiro

```python
except discord.NotFound:       # mais específica
    ...
except discord.HTTPException:  # mais genérica
    ...
```

## Mensagens para o usuário vs. mensagens para o log

| Para o usuário | Para o log |
|---|---|
| Claras, sem termos técnicos | Técnicas, com traceback |
| "Você precisa da permissão Expulsar membros." | `MissingPermissions(['kick_members'])` |
| Geralmente *ephemeral* | Com nível adequado |

O [tratador central](../code-explanation/events/errors.md) faz exatamente essa separação.

## Níveis de log

| Nível | Use para | Exemplo no projeto |
|---|---|---|
| `DEBUG` | detalhes para investigar problemas | — |
| `INFO` | eventos normais importantes | "Extensão carregada", "Conectado como..." |
| `WARNING` | algo inesperado, mas o bot continua | "Intent 'members' desativada" |
| `ERROR` | uma operação falhou | "Erro inesperado no comando /..." |
| `CRITICAL` | o bot não consegue continuar | — |

## Regras para logs

- Use `logger = logging.getLogger(__name__)` em cada arquivo.
- Use `logger.exception(...)` dentro de `except` para incluir o traceback.
- Use `%s` em vez de f-string: `logger.info("Usuário %s", user_id)`.
- **Nunca** registre tokens, senhas ou conteúdo privado de mensagens.

## Falhe cedo e com clareza

Configuração errada deve impedir o bot de iniciar, com uma mensagem que diga **como resolver**. Veja [config.py](../code-explanation/config.md): é melhor parar na inicialização do que falhar de forma misteriosa horas depois.
