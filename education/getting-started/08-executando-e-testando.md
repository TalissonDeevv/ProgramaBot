# 08. Executando e testando o bot

## 1. Rode os testes automatizados (opcional, recomendado)

Com o ambiente virtual ativado, na pasta raiz:

```bash
python -m pytest
```

No final deve aparecer algo como `... passed`. Esses testes não usam o Discord nem o seu token.

## 2. Inicie o bot

```bash
python -m bot.main
```

Se tudo estiver certo, você verá algo assim no terminal:

```
19/11/2026 14:02:10 | INFO     | bot.main | Iniciando ProgramaBot 1.0.0-dev (discord.py 2.7.1)
19/11/2026 14:02:11 | INFO     | bot.main | Extensão carregada: bot.commands.fun.dice
...
19/11/2026 14:02:12 | INFO     | bot.main | 20 slash commands sincronizados no servidor 1234....
19/11/2026 14:02:13 | INFO     | bot.events.ready | Conectado como MeuProgramaBot#1234 (ID: ...)
19/11/2026 14:02:13 | INFO     | bot.events.ready | ProgramaBot pronto! Use /help no Discord.
```

> Use `python -m bot.main`, e não `python bot/main.py`. O `-m` faz o Python reconhecer a pasta `bot` como pacote.

O bot fica online **enquanto o terminal estiver aberto**. Para desligar, pressione `Ctrl+C`.

## 3. Verifique se está online

No Discord, o bot deve aparecer com a bolinha verde na lista de membros, com o status "Jogando /help | aprendendo Python".

## 4. Teste os comandos

Digite `/` em um canal do servidor de testes e escolha o bot na lista. Sugestão de roteiro:

| Teste | O que esperar |
|---|---|
| `/ping` | "Pong!" com a latência |
| `/help` | Menu de categorias (só você vê) |
| `/hello nome:Seu Nome` | Cumprimento conforme o horário |
| `/calculator expressao:2 + 3 * 4` | 14 |
| `/calculator expressao:print(1)` | Erro amigável (a calculadora é segura) |
| `/userinfo` e `/serverinfo` | Informações em embed |
| `/poll pergunta:Teste? opcoes:Sim; Não duracao_minutos:1` | Enquete que encerra em 1 minuto |
| `/remind tempo:30s mensagem:Funcionou!` | Aviso depois de ~30 segundos |
| `/embed` | Formulário |
| `!ping` | Comando de prefixo |
| Mencionar o bot sozinho (`@SeuBot`) | Resposta com dicas |

Os comandos de moderação (`/kick`, `/ban`, `/timeout`, `/clear`) devem ser testados com uma **conta secundária**.

## 5. Faça sua primeira modificação

1. Pare o bot (`Ctrl+C`).
2. Abra `bot/commands/general/hello.py` e adicione uma dica sua em `STUDY_TIPS`.
3. Inicie o bot de novo e use `/hello` algumas vezes até ver a sua dica.

🎉 Você acabou de modificar um bot real. Continue pela [trilha de aprendizado](../README.md).

Algo deu errado? Veja [Problemas comuns](09-problemas-comuns.md).
