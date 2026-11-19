# 05. Ambiente virtual e dependências

## O que é um ambiente virtual?

Um **ambiente virtual** (`venv`) é uma "cópia isolada" do Python só para um projeto. As bibliotecas instaladas nele não se misturam com as de outros projetos. Assim, o ProgramaBot pode usar `discord.py 2.7.1` enquanto outro projeto seu usa outra versão.

## 1. Criar

No terminal, **na pasta raiz do projeto**:

```bash
python -m venv .venv
```

Isso cria a pasta `.venv/` (já ignorada pelo Git). Só é preciso fazer isso uma vez.

## 2. Ativar

Faça isso **toda vez** que abrir um terminal novo para trabalhar no projeto.

| Sistema | Comando |
|---|---|
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| Windows (Prompt de Comando) | `.venv\Scripts\activate.bat` |
| Linux / macOS | `source .venv/bin/activate` |

Funcionou se aparecer `(.venv)` no começo da linha do terminal.

### Erro no PowerShell: "a execução de scripts foi desabilitada"

O Windows bloqueia scripts por padrão. Você tem três opções:

1. Usar o **Prompt de Comando** (cmd) com `.venv\Scripts\activate.bat`.
2. Não ativar e chamar o Python do ambiente diretamente: `.venv\Scripts\python -m bot.main`.
3. Permitir scripts locais para o seu usuário (é uma configuração do sistema; leia sobre ela antes de alterar):

   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

No VS Code, depois de selecionar o interpretador do `.venv`, os terminais novos já abrem com o ambiente ativado.

## 3. Instalar as dependências

```bash
pip install -r requirements-dev.txt
```

| Arquivo | Contém | Quando usar |
|---|---|---|
| `requirements.txt` | `discord.py`, `python-dotenv` | só para executar o bot |
| `requirements-dev.txt` | o anterior + `pytest`, `pytest-asyncio` | para estudar e rodar os testes (recomendado) |

As versões estão **fixadas** (`==`) para que todos os estudantes tenham exatamente o mesmo ambiente.

## 4. Conferir

```bash
pip list
python -c "import discord; print(discord.__version__)"
```

A versão exibida deve ser `2.7.1`.

## Para sair do ambiente

```bash
deactivate
```

Próximo passo: [Criando o bot no Discord](06-criando-o-bot-no-discord.md).
