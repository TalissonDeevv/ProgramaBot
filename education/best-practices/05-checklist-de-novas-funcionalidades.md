# 05. Checklist de novas funcionalidades

O ProgramaBot é atualizado continuamente. Para que **documentação e código nunca fiquem desalinhados**, toda mudança segue estas regras.

## Para toda funcionalidade nova ou alterada

1. **Código real**: crie ou atualize o código em `bot/`. Nada de pseudocódigo ou funcionalidade "anunciada" que não existe.
2. **Documentação do arquivo**: crie ou atualize `education/code-explanation/<mesmo caminho>.md`, com as 18 seções.
3. **Bibliotecas**: se usou um módulo novo, crie `education/libraries/<modulo>.md` e atualize o índice em `education/libraries/README.md`.
4. **Exercícios**: quando fizer sentido, adicione um exercício (com a solução em arquivo separado).
5. **README**: atualize a lista de funcionalidades, se ela mudou.
6. **CHANGELOG**: registre a mudança em "Não lançado".
7. **Testes**: crie ou atualize os testes. Rode `python -m pytest` e confirme que **todos** passam.

## Atalhos que os testes já verificam

- arquivo Python sem documentação → `test_every_python_file_has_documentation`
- documentação de arquivo que não existe mais → `test_documentation_has_no_orphan_files`
- comando fora do `/help` → `test_help_catalog_matches_registered_commands`
- parâmetro sem descrição → `test_commands_have_descriptions`
- link interno quebrado → `test_relative_markdown_links_point_to_existing_files`
- dependência sem versão fixa → `test_requirements_are_pinned`

## Versionamento semântico

O projeto usa `MAJOR.MINOR.PATCH` ([semver.org](https://semver.org/lang/pt-BR/)):

| Mudança | Incrementa | Exemplo |
|---|---|---|
| Correção que não muda o comportamento esperado | PATCH | 1.1.0 → 1.1.1 |
| Funcionalidade nova, compatível | MINOR | 1.1.1 → 1.2.0 |
| Mudança incompatível (ex.: renomear uma variável do `.env`, remover um comando) | MAJOR | 1.2.0 → 2.0.0 |

A versão fica em `bot/__init__.py` (`__version__`). Ao lançar uma versão, o mantenedor move os itens de "Não lançado" para uma seção com o número e a data no [CHANGELOG](../../CHANGELOG.md).
