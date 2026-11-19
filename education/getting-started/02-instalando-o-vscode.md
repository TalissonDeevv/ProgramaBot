# 02. Instalando o Visual Studio Code

O **Visual Studio Code** (VS Code) é um editor de código gratuito. Ele mostra o código colorido, aponta erros, tem um terminal integrado e extensões para Python.

## Instalação

1. Acesse <https://code.visualstudio.com/> e baixe a versão do seu sistema.
2. Instale com as opções padrão. No Windows, é útil marcar **"Adicionar ao PATH"** e **"Abrir com Code"** no menu de contexto.

## Extensão de Python

1. Abra o VS Code.
2. Clique no ícone de **Extensões** na barra lateral (ou `Ctrl+Shift+X`).
3. Pesquise **Python** e instale a extensão publicada pela **Microsoft**.

O projeto também recomenda essa extensão automaticamente: o VS Code mostra um aviso ao abrir a pasta (arquivo `.vscode/extensions.json`).

## Recursos que você vai usar

| Recurso | Atalho | Para quê |
|---|---|---|
| Terminal integrado | `` Ctrl+` `` | Rodar comandos sem sair do editor |
| Explorador de arquivos | `Ctrl+Shift+E` | Navegar pelas pastas |
| Abrir arquivo pelo nome | `Ctrl+P` | Digite `ping.py` e pressione Enter |
| Buscar em todos os arquivos | `Ctrl+Shift+F` | Achar onde uma função é usada |
| Ir para a definição | `F12` | Ver onde uma função ou classe foi criada |
| Pré-visualizar Markdown | `Ctrl+Shift+V` | Ler a documentação formatada |
| Escolher o interpretador | `Ctrl+Shift+P` → "Python: Select Interpreter" | Usar o Python do `.venv` |

## Escolhendo o interpretador do projeto

Depois de criar o ambiente virtual ([passo 5](05-ambiente-virtual-e-dependencias.md)), selecione o Python de dentro de `.venv`. Assim o VS Code encontra o discord.py e para de sublinhar os imports em vermelho.

Próximo passo: [Usando o terminal](03-usando-o-terminal.md).
