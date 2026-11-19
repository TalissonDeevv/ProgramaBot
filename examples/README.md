# 🧪 Exemplos

Códigos pequenos e independentes para praticar. Eles **não fazem parte do bot**: servem para você estudar e copiar ideias.

| Pasta | Conteúdo | Como executar |
|---|---|---|
| [`python-basics/`](python-basics) | Um arquivo por aula de Python | `python examples/python-basics/01_variaveis.py` |
| [`minimal-bot/`](minimal-bot) | O menor bot possível, em um único arquivo | veja as instruções no arquivo |
| [`commands/`](commands) | Modelo para criar um comando novo no ProgramaBot | copie para `bot/commands/<categoria>/` |
| [`events/`](events) | Modelo de evento (reações) | copie para `bot/events/` |
| [`embeds/`](embeds) | Todos os recursos de um embed | modelo de comando |

Todos os exemplos de `python-basics/` rodam sem interação (sem `input()`), para que o teste `tests/test_project_structure.py` possa executá-los automaticamente. Quando quiser praticar entrada de dados, descomente as linhas com `input()` indicadas nos arquivos.
