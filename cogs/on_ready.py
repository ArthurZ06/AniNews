from discord.ext import commands, tasks
import discord
import feedparser

class News(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.posts_enviados = set()

        self.verificar_noticias.start()

    @tasks.loop(minutes=30)
    async def verificar_noticias(self):

        canal = self.bot.get_channel(1495959671658516550)

        feed = feedparser.parse(
            "https://www.intoxianime.com/feed/"
        )

        for post in feed.entries[:5]:

            if post.link in self.posts_enviados:
                continue

            self.posts_enviados.add(post.link)

            embed = discord.Embed(
                title=post.title,
                url=post.link,
                description="Nova notícia de anime!",
                color=discord.Color.red()
            )

            await canal.send(embed=embed)

    @verificar_noticias.before_loop
    async def before_verificar_noticias(self):

        await self.bot.wait_until_ready()

        print("Sistema de notícias iniciado!")

async def setup(bot):

    await bot.add_cog(News(bot))