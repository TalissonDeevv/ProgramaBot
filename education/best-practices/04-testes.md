# 04. Testes

## Por que testar?

- Você descobre bugs **antes** dos usuários.
- Você pode mudar o código com confiança: se algo quebrar, um teste avisa.
- Testes documentam como o código deve se comportar.

## Como rodar

```bash
python -m pytest            # todos
python -m pytest -v         # com o nome de cada teste
python -m pytest -k remind  # só os que contêm "remind" no nome
```

## O que o ProgramaBot testa

| Arquivo | Verifica |
|---|---|
| `test_calculator.py` | contas, limites e **bloqueio de código malicioso** |
| `test_time_parser.py` | interpretação e formatação de durações |
| `test_config.py` | leitura e validação do `.env` (sem tocar no seu `.env`) |
| `test_moderation.py` | regras de hierarquia com objetos falsos |
| `test_embeds.py` | cores, rodapé, validação de cor |
| `test_poll.py` | votos, opções, view da enquete |
| `test_reminders.py` | banco de dados em pasta temporária, incluindo SQL injection |
| `test_command_helpers.py` | funções auxiliares dos comandos e eventos; tradução de erros |
| `test_extensions.py` | **todas** as extensões carregam; comandos registrados; descrições; permissões; catálogo do `/help` |
| `test_project_structure.py` | documentação de cada arquivo, links, ausência de tokens, exemplos executáveis |

## Como testar código de bot sem o Discord

1. **Separe a lógica** em funções puras (veja [Organização do código](02-organizacao-do-codigo.md)).
2. **Use objetos falsos** com os atributos necessários:

   ```python
   from types import SimpleNamespace
   membro = SimpleNamespace(id=1, top_role=10)
   ```

3. **Crie o bot sem conectar**: `tests/conftest.py` cria um `ProgramaBot` dentro de `async with bot:`, carrega todas as extensões e inspeciona `bot.tree.get_commands()`. Nada é enviado ao Discord.
4. **Use recursos temporários**: a fixture `tmp_path` dá uma pasta que é apagada no fim do teste.
5. **Isole o ambiente**: `monkeypatch.setenv` altera variáveis só durante o teste.

## O que não é testado automaticamente

A comunicação real com o Discord (enviar mensagens, banir, clicar em botões). Isso exige um bot conectado e é verificado **manualmente**, seguindo o roteiro de [Executando e testando](../getting-started/08-executando-e-testando.md#4-teste-os-comandos).

## Estrutura de um bom teste

```python
def test_vote_changes_option():
    # Preparar
    state = PollState("?", ["A", "B"])
    state.vote(1, 0)
    # Agir
    status = state.vote(1, 1)
    # Verificar
    assert status == "changed"
    assert state.counts() == [0, 1]
```

Um teste deve verificar **uma ideia**, ter um nome que descreva essa ideia e não depender da ordem de execução.

## Integração contínua

O arquivo `.github/workflows/tests.yml` roda os testes automaticamente no GitHub a cada push e pull request.
