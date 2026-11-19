# sqlite3

## O que é?

O módulo do Python para usar o **SQLite**, um banco de dados relacional que guarda tudo em **um único arquivo**.

## Para que serve? Que problema resolve?

Variáveis desaparecem quando o programa fecha. Arquivos de texto ou JSON funcionam para poucos dados, mas ficam difíceis quando você precisa **buscar** ("lembretes vencidos"), **contar** ("quantos lembretes este usuário tem?") ou **alterar** um item sem reescrever tudo. Bancos de dados resolvem isso com a linguagem **SQL**.

O SQLite é a forma mais simples de começar: não precisa instalar servidor nem configurar usuário e senha.

## Como funciona?

Os dados ficam em **tabelas**, como planilhas:

```
reminders
| id | user_id | channel_id | message      | remind_at  | created_at |
|----|---------|------------|--------------|------------|------------|
| 1  | 111     | 999        | Beber água   | 1795000000 | 1794999400 |
```

O fluxo com o `sqlite3` é:

1. `connect` → abre o arquivo;
2. `execute` → envia um comando SQL;
3. `fetchall` → lê os resultados (em consultas);
4. `commit` → confirma as alterações;
5. `close` → fecha.

### SQL básico usado no projeto

```sql
CREATE TABLE IF NOT EXISTS reminders (...);          -- cria a tabela
INSERT INTO reminders (colunas) VALUES (?, ?, ...);  -- adiciona uma linha
SELECT colunas FROM reminders WHERE remind_at <= ?;  -- busca linhas
SELECT COUNT(*) FROM reminders WHERE user_id = ?;    -- conta linhas
DELETE FROM reminders WHERE id = ?;                  -- apaga uma linha
```

## Nativa ou externa?

**Nativa.** O SQLite já vem embutido no Python.

## Como importar

```python
import sqlite3
```

## Funções e métodos utilizados no ProgramaBot

| Item | Explicação |
|---|---|
| `sqlite3.connect(caminho)` | Abre (ou cria) o banco. |
| `conexao.row_factory = sqlite3.Row` | Permite ler colunas pelo nome: `linha["message"]`. |
| `with conexao:` | Transação: `commit` automático se der certo e `rollback` se der erro. **Não fecha** a conexão. |
| `conexao.execute(sql, parametros)` | Executa SQL com parâmetros seguros (`?`). |
| `cursor.fetchall()` | Lista de linhas do resultado. |
| `cursor.lastrowid` | ID gerado no último `INSERT`. |
| `conexao.close()` | Fecha a conexão. |

Tudo isso está em [`bot/database/reminders.py`](../code-explanation/database/reminders.md).

## ⚠️ Segurança: nunca monte SQL com f-strings

```python
# ❌ PERIGOSO (SQL injection)
conexao.execute(f"SELECT * FROM usuarios WHERE nome = '{nome}'")

# ✅ SEGURO
conexao.execute("SELECT * FROM usuarios WHERE nome = ?", (nome,))
```

Se alguém digitar `' OR '1'='1` como nome, a primeira versão devolveria **todos** os usuários. Com `?`, o valor é tratado sempre como dado.

## Exemplo independente do ProgramaBot

```python
import sqlite3

conexao = sqlite3.connect("escola.db")
try:
    with conexao:
        conexao.execute("CREATE TABLE IF NOT EXISTS alunos (id INTEGER PRIMARY KEY, nome TEXT, nota REAL)")
        conexao.execute("INSERT INTO alunos (nome, nota) VALUES (?, ?)", ("Ana", 9.5))
        conexao.execute("INSERT INTO alunos (nome, nota) VALUES (?, ?)", ("Bruno", 7.0))

    for nome, nota in conexao.execute("SELECT nome, nota FROM alunos WHERE nota >= ?", (8,)):
        print(nome, nota)
finally:
    conexao.close()
```

## Ferramenta recomendada

[DB Browser for SQLite](https://sqlitebrowser.org/) é um programa gratuito para abrir arquivos `.db` e ver as tabelas.

## Documentação oficial

- Módulo: <https://docs.python.org/pt-br/3/library/sqlite3.html>
- SQLite: <https://www.sqlite.org/docs.html>
