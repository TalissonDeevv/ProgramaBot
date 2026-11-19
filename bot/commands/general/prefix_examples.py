"""Exemplos educacionais de comandos de PREFIXO (como ``!ping``).

Antes dos slash commands existirem, os bots liam todas as mensagens e
procuravam as que começavam com um prefixo (``!``, ``?``, ``.``...).
Esse modelo ainda funciona, mas exige a intent privilegiada MESSAGE CONTENT,
porque o bot precisa ler o texto das mensagens.

Compare este arquivo com ``ping.py`` e ``hello.py`` para ver as diferenças.
"""

from discord.ext import commands

from bot.utils.calculator import format_result


class PrefixExamples(commands.Cog):
    """Cog com comandos de prefixo de exemplo."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="ping")
    async def ping_prefix(self, ctx: commands.Context) -> None:
        """Uso: !ping"""
        latency_ms = round(self.bot.latency * 1000)
        await ctx.send(f"🏓 Pong! {latency_ms} ms (este é um comando de prefixo)")

    @commands.command(name="hello", aliases=["ola", "oi"])
    async def hello_prefix(self, ctx: commands.Context, *, nome: str | None = None) -> None:
        """Uso: !hello ou !hello Maria. O ``*`` junta todas as palavras em ``nome``."""
        name = nome or ctx.author.display_name
        await ctx.send(f"Olá, **{name}**! 👋 Experimente também o /hello.")

    @commands.command(name="soma")
    async def soma(self, ctx: commands.Context, a: float, b: float) -> None:
        """Uso: !soma 2 3. O discord.py converte os textos em float automaticamente."""
        await ctx.send(f"{format_result(a)} + {format_result(b)} = **{format_result(a + b)}**")

    @soma.error
    async def soma_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        """Tratamento de erro exclusivo do !soma."""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Faltou um número. Uso correto: `!soma 2 3`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Use apenas números. Exemplo: `!soma 2.5 4`")
        else:
            raise error


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PrefixExamples(bot))
