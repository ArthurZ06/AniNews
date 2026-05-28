from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mantega(self, ctx):
        await ctx.send("Mantega é o melhor anime de todos os tempos! 🧈")


async def setup(bot):
    await bot.add_cog(Fun(bot))