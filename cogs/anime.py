from discord.ext import commands, tasks
import requests

class Anime(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.verification_anime.start()

    @tasks.loop(minutes=10)
    async def verification_anime(self):

        canal = self.bot.get_channel(
            1508215790103429170
        )

        url = "https://api.jikan.moe/v4/top/anime"

        response = requests.get(url)

        data = response.json()

        top5 = data["data"][:5]

        for anime in top5:

            await canal.send(
                f"Anime em alta: {anime['title']}"
            )

    @verification_anime.before_loop
    async def before_verification_anime(self):

        await self.bot.wait_until_ready()

        print("Sistema de anime iniciado!")

async def setup(bot):

    await bot.add_cog(Anime(bot))