# 03. Usando o terminal

O **terminal** (ou linha de comando) é uma janela onde você digita comandos de texto para o computador. Programadores o usam para executar programas, instalar bibliotecas e usar o Git.

## Abrindo

- **No VS Code (recomendado):** menu *Terminal > Novo Terminal*, ou `` Ctrl+` ``. Ele já abre na pasta do projeto.
- **Windows:** procure "Terminal" ou "PowerShell" no menu Iniciar.
- **macOS:** *Aplicativos > Utilitários > Terminal*.
- **Linux:** `Ctrl+Alt+T` na maioria das distribuições.

## Comandos essenciais

| O que fazer | Windows (PowerShell) | Linux / macOS |
|---|---|---|
| Ver em que pasta estou | `pwd` | `pwd` |
| Listar arquivos | `ls` ou `dir` | `ls` |
| Entrar em uma pasta | `cd nome-da-pasta` | `cd nome-da-pasta` |
| Voltar uma pasta | `cd ..` | `cd ..` |
| Criar pasta | `mkdir nome` | `mkdir nome` |
| Copiar arquivo | `copy origem destino` | `cp origem destino` |
| Limpar a tela | `cls` | `clear` |
| Parar um programa | `Ctrl+C` | `Ctrl+C` |
| Repetir comandos anteriores | seta ↑ | seta ↑ |
| Completar nomes | `Tab` | `Tab` |

## Dicas

- Nomes de pastas com espaço precisam de aspas: `cd "Meus Projetos"`.
- O terminal mostra a pasta atual antes do cursor. Quase todos os comandos do ProgramaBot devem ser executados **na pasta raiz do projeto** (a que tem o `README.md`).
- Quando o ambiente virtual está ativo, aparece `(.venv)` no início da linha.
- Ler a mensagem de erro com atenção resolve a maioria dos problemas.

## Pratique

```bash
pwd
mkdir teste-terminal
cd teste-terminal
python -c "print('Estou dentro da pasta de teste!')"
cd ..
```

Próximo passo: [Baixando o projeto](04-baixando-o-projeto.md).
