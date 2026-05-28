from discord.ext import commands

class Soma(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def soma(self, ctx, num1: int, num2: int):

        resultado = num1 + num2

        await ctx.send(
            f"A soma de {num1} e {num2} é: {resultado}"
        )

async def setup(bot):
    await bot.add_cog(Soma(bot))