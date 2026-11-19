# Política de segurança

## Versões suportadas

O ProgramaBot ainda não tem uma versão estável lançada. As correções de segurança são aplicadas na branch `main`.

| Versão | Suporte |
|---|---|
| `main` (em desenvolvimento, rumo à 1.0.0) | ✅ |

Esta tabela será atualizada quando versões forem lançadas.

## Como relatar uma vulnerabilidade

**Não abra uma issue pública** com detalhes de uma falha de segurança.

1. Se o repositório tiver o relato privado de vulnerabilidades habilitado, use a aba **Security** > **Report a vulnerability** do [repositório no GitHub](https://github.com/TalissonDeevv/ProgramaBot/security).
2. Caso essa opção não esteja disponível, entre em contato com o mantenedor de forma privada pelo perfil do GitHub (<https://github.com/TalissonDeevv>), dizendo apenas que deseja relatar um problema de segurança, sem os detalhes técnicos, para combinar um canal privado.

Inclua no relato:

- uma descrição do problema e do impacto possível;
- os passos para reproduzir;
- a versão ou o commit afetado;
- uma sugestão de correção, se tiver.

Esta é uma iniciativa mantida voluntariamente. Os relatos serão analisados assim que possível, e quem relatou receberá os créditos na correção, se quiser.

## Escopo

Exemplos de problemas que nos interessam:

- execução de código a partir de entradas de usuários (por exemplo, burlar a calculadora segura);
- SQL injection no banco de lembretes;
- formas de contornar as verificações de permissão ou de hierarquia;
- menções em massa (`@everyone`) por meio de comandos do bot;
- exposição acidental de tokens ou dados.

## Se o seu token vazou

O token é responsabilidade de quem hospeda o bot. Se o **seu** token vazou:

1. Acesse o [Developer Portal](https://discord.com/developers/applications) > sua aplicação > **Bot** > **Reset Token**.
2. Atualize o seu `.env`.
3. Se o token foi para um commit, saiba que ele continua no histórico do Git. O passo 1 é o que realmente resolve.

Mais orientações: [Boas práticas de segurança](education/best-practices/01-seguranca.md).
