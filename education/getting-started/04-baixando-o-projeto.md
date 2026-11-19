# 04. Baixando o projeto

Há duas formas de obter o ProgramaBot.

## Opção A: clonar com Git (recomendado)

Com o Git instalado (veja [Git e GitHub](10-git-e-github.md)), abra o terminal na pasta onde quer guardar o projeto e execute:

```bash
git clone https://github.com/TalissonDeevv/ProgramaBot.git
cd ProgramaBot
```

Vantagem: depois, para receber as atualizações do projeto, basta executar `git pull`.

## Opção B: baixar o ZIP

1. Acesse <https://github.com/TalissonDeevv/ProgramaBot>.
2. Clique no botão verde **Code** > **Download ZIP**.
3. Extraia o arquivo (botão direito > *Extrair tudo*).
4. A pasta extraída pode se chamar `ProgramaBot-main`. Tudo bem.

## Quer publicar suas modificações? Faça um fork

Um **fork** é uma cópia do repositório na **sua** conta do GitHub. Clique em **Fork** no topo da página do repositório e depois clone o **seu** fork. Assim, você pode fazer commits sem afetar o projeto original e, se quiser, propor melhorias com um *pull request* (veja o [CONTRIBUTING.md](../../CONTRIBUTING.md)).

## Abrindo no VS Code

- *File > Open Folder...* (*Arquivo > Abrir Pasta...*) e escolha a pasta `ProgramaBot`; ou
- no terminal, dentro da pasta: `code .`

Abra a **pasta raiz** (a que contém `README.md`, `bot/` e `education/`), e não uma subpasta.

## Conhecendo a estrutura

```
ProgramaBot/
├── bot/            ← o código do bot
├── education/      ← o curso (você está aqui)
├── examples/       ← exemplos para praticar
├── resources/      ← playlists, glossário, links
├── tests/          ← testes automatizados
├── .env.example    ← modelo de configuração
└── README.md
```

Próximo passo: [Ambiente virtual e dependências](05-ambiente-virtual-e-dependencias.md).
