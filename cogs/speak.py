from discord.ext import commands
class Speak(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def speak(self, ctx, *, mensagem):
        await ctx.send(f"Você disse: {mensagem}")

        