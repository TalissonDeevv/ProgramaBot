# 01. Instalando o Python

O ProgramaBot foi desenvolvido e testado com **Python 3.12**. A versão mínima é a **3.10**, exigida pelas dependências do projeto.

## Windows

1. Acesse <https://www.python.org/downloads/>.
2. Baixe o instalador do Python 3.12 para Windows. A página "All releases" lista as versões anteriores à mais recente.
3. Abra o instalador. **Antes de clicar em instalar**, marque a opção **"Add python.exe to PATH"** (adicionar ao PATH). Sem ela, o comando `python` não funciona no terminal.
4. Clique em **Install Now** e aguarde.

> O instalador oficial pode mudar com o tempo. Siga as instruções exibidas pelo próprio site oficial e certifique-se de que o Python fique disponível no terminal.

## macOS

Baixe o instalador em <https://www.python.org/downloads/macos/>. No macOS, o comando costuma ser `python3` em vez de `python`.

## Linux

A maioria das distribuições já vem com Python 3. Confira a versão (próxima seção). No Ubuntu/Debian, o módulo de ambientes virtuais pode precisar ser instalado à parte:

```bash
sudo apt install python3 python3-venv python3-pip
```

## Verificando

Abra um terminal (veja [Usando o terminal](03-usando-o-terminal.md)) e digite:

```bash
python --version
```

Deve aparecer algo como `Python 3.12.x`. Se aparecer um erro, tente `python3 --version` (macOS/Linux) ou `py --version` (Windows).

## Primeiro teste

```bash
python -c "print('Olá, Python!')"
```

## Problemas comuns

| Problema | Solução |
|---|---|
| `'python' não é reconhecido como um comando` | O Python não está no PATH. Reinstale marcando "Add python.exe to PATH", ou use `py`. |
| Abre a Microsoft Store ao digitar `python` | Desative os "aliases de execução de aplicativo" do Python nas configurações do Windows ou instale pelo python.org. |
| Versão antiga (3.8, 3.9) | Instale a 3.12. |

Próximo passo: [Instalando o Visual Studio Code](02-instalando-o-vscode.md).
