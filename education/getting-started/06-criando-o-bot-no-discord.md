# 06. Criando o bot no Discord Developer Portal

Para o código se conectar ao Discord, você precisa criar uma **aplicação** com um **usuário bot**. É gratuito.

> A interface do Developer Portal muda de tempos em tempos. Os nomes abaixo são os da interface em inglês. Se algo estiver diferente, procure a opção com nome parecido ou consulte a [documentação oficial](https://discord.com/developers/docs/quick-start/getting-started).

## 1. Crie um servidor de testes

No Discord, clique em **+** (Adicionar um servidor) > **Criar o meu** > **Para meus amigos e eu**. Use esse servidor só para testes. Assim, você pode testar moderação à vontade.

## 2. Crie a aplicação

1. Acesse <https://discord.com/developers/applications> e entre com sua conta do Discord.
2. Clique em **New Application**.
3. Dê um nome (ex.: `MeuProgramaBot`), aceite os termos e clique em **Create**.

## 3. Configure o bot

1. No menu lateral, abra **Bot**.
2. Em **Token**, clique em **Reset Token** e confirme. **Copie o token** e guarde-o temporariamente; você vai colá-lo no `.env` no próximo passo.
   - O token só é exibido uma vez. Se perdê-lo, gere outro.
   - **Nunca** compartilhe esse texto. Quem tiver o token controla o seu bot.
3. Em **Privileged Gateway Intents**, ative:
   - ✅ **Server Members Intent** (necessária para as boas-vindas);
   - ✅ **Message Content Intent** (necessária para os comandos de prefixo, como `!ping`).
   - (Não é preciso ativar *Presence Intent*.)
4. Clique em **Save Changes**.

Entenda o motivo em [Intents](../discord-development/02-intents.md).

## 4. Gere o link de convite

1. No menu lateral, abra **OAuth2** e procure **OAuth2 URL Generator**.
2. Em **Scopes**, marque:
   - ✅ `bot`
   - ✅ `applications.commands` (necessário para os slash commands)
3. Em **Bot Permissions**, marque:
   - View Channels, Send Messages, Embed Links, Read Message History, Add Reactions;
   - Manage Messages (`/clear`, `/say`), Kick Members (`/kick`), Ban Members (`/ban`, `/unban`), Moderate Members (`/timeout`).
   - **Não** marque *Administrator*. Veja o motivo em [Permissões](../discord-development/08-permissoes.md).
4. Copie a URL gerada no final da página.

## 5. Convide o bot

1. Cole a URL no navegador.
2. Escolha o seu servidor de testes e clique em **Continuar** > **Autorizar**.
3. O bot aparece na lista de membros, **offline**. Ele só fica online quando o código estiver rodando.

## 6. Ative o Modo Desenvolvedor e copie o ID do servidor

1. No Discord: **Configurações de usuário** > **Avançado** > ative **Modo de desenvolvedor**.
2. Clique com o botão direito no ícone do seu servidor > **Copiar ID do servidor**.
3. Guarde o número para o próximo passo (`GUILD_ID`).

## 7. Ajuste a hierarquia de cargos (para a moderação)

Em **Configurações do servidor** > **Cargos**, arraste o cargo do bot (criado com o nome dele) para **acima** dos cargos dos membros que ele deve moderar.

Próximo passo: [Configurando o arquivo .env](07-configurando-o-env.md).
