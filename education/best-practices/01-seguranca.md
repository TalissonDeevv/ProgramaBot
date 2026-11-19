# 01. Segurança

## 1. O token é uma senha

- Fica **só** no `.env` (ou nas variáveis de ambiente do servidor).
- O `.env` está no `.gitignore`. Confira com `git status` antes de cada commit.
- Nunca o coloque em código, prints, vídeos, issues, mensagens ou capturas de tela do terminal.
- Vazou? **Reset Token** no Developer Portal imediatamente. O GitHub e o Discord fazem varreduras automáticas e podem invalidar tokens publicados, mas não conte com isso.
- O teste `test_no_discord_tokens_in_repository` procura textos com formato de token nos arquivos do projeto.

### Já enviei o token em um commit. E agora?

Apagar o arquivo em um commit novo **não basta**: o token continua no histórico do Git. A única solução segura é **gerar um token novo**. Depois, se quiser, limpe o histórico com ferramentas próprias para isso.

## 2. Nunca confie na entrada do usuário

Tudo o que vem do Discord (textos, IDs, nomes) pode ter sido escrito para atacar o bot.

| Risco | Exemplo | Como o ProgramaBot se protege |
|---|---|---|
| Execução de código | `__import__('os').system(...)` na calculadora | sem `eval()`; análise com `ast` ([calculator](../code-explanation/utils/calculator.md)) |
| SQL injection | `'); DROP TABLE reminders; --` | parâmetros `?` ([reminders](../code-explanation/database/reminders.md)) |
| Menções em massa | `@everyone` em `/say` | `AllowedMentions.none()` |
| Abuso de recursos | 1 milhão de lembretes; `2 ** 99999999` | limites (`Range`, `MAX_REMINDERS_PER_USER`, `MAX_EXPONENT`) |
| Spam | `/embed` repetido | `cooldown` |

## 3. Menor privilégio

- Convide o bot com **só** as permissões necessárias, nunca "Administrator".
- Verifique as permissões do **usuário** e do **bot** em comandos sensíveis.
- Respeite a hierarquia de cargos.

Detalhes em [Permissões](../discord-development/08-permissoes.md).

## 4. Dependências

- Versões fixadas no `requirements.txt` (todos usam o mesmo código).
- Instale pacotes apenas do PyPI oficial e confira o nome com atenção. Existem pacotes falsos com nomes parecidos (*typosquatting*).
- Atualize as dependências periodicamente, rodando os testes depois.

## 5. Dados pessoais

- Guarde só o necessário (o ProgramaBot guarda IDs e o texto dos lembretes, e apaga cada lembrete depois de entregá-lo).
- Não registre no log conteúdo de mensagens ou dados sensíveis.

## 6. Relatando vulnerabilidades

Encontrou uma falha de segurança no ProgramaBot? Siga o [SECURITY.md](../../SECURITY.md). Não abra uma issue pública com os detalhes.
