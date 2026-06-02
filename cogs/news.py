from discord.ext import commands, tasks
import discord
import feedparser
from bs4 import BeautifulSoup
import json
import os

FEED_URL = "https://www.intoxianime.com/feed/"
CANAL_ID = 1495959671658516550


class News(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.arquivo_posts = "posts_enviados.json"
        self.posts_enviados = self.carregar_posts()

        self.verificar_noticias.start()

    # Store sent posts locally

    def carregar_posts(self):

        if not os.path.exists(self.arquivo_posts):
            return set()

        with open(
            self.arquivo_posts,
            "r",
            encoding="utf-8"
        ) as f:

            return set(json.load(f))

    def salvar_posts(self):

        with open(
            self.arquivo_posts,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                list(self.posts_enviados),
                f,
                indent=4
            )

    # Extract the first image from a feed entry

    def pegar_imagem(self, post):

        if "content" in post:

            for content in post.content:

                soup = BeautifulSoup(
                    content.value,
                    "html.parser"
                )

                imagens = soup.find_all("img")

                for img in imagens:

                    url = (
                        img.get("src")
                        or img.get("data-src")
                    )

                    if not url and img.get("srcset"):

                        imagens_srcset = (
                            img.get("srcset")
                            .split(",")
                        )

                        ultima = imagens_srcset[-1]

                        url = (
                            ultima
                            .split(" ")[0]
                        )

                    if (
                        url
                        and url.startswith(
                            "http"
                        )
                    ):
                        return url

        if "summary" in post:

            soup = BeautifulSoup(
                post.summary,
                "html.parser"
            )

            img = soup.find("img")

            if img:

                url = (
                    img.get("src")
                    or img.get("data-src")
                )

                if url:
                    return url

        return None

    @tasks.loop(minutes=30)
    async def verificar_noticias(self):

        canal = self.bot.get_channel(
            CANAL_ID
        )

        if canal is None:

            print(
                "Canal não encontrado."
            )

            return

        feed = feedparser.parse(
            FEED_URL
        )

        # Check the latest 20 entries
        posts = list(
            reversed(
                feed.entries[:20]
            )
        )

        for post in posts:

            if (
                post.link
                in self.posts_enviados
            ):
                continue

            self.posts_enviados.add(
                post.link
            )

            self.salvar_posts()

            imagem = self.pegar_imagem(
                post
            )

            embed = discord.Embed(
                title=post.title,
                url=post.link,
                description="📰 Nova notícia de anime!",
                color=discord.Color.red()
            )

            if hasattr(
                post,
                "published"
            ):

                embed.add_field(
                    name="📅 Publicado em",
                    value=post.published,
                    inline=False
                )

            embed.set_footer(
                text="IntoxiAnime"
            )

            if imagem:

                embed.set_image(
                    url=imagem
                )

            else:

                embed.set_thumbnail(
                    url=(
                        "https://cdn-icons-png.flaticon.com/512/5968/5968885.png"
                    )
                )

            await canal.send(
                embed=embed
            )

    @verificar_noticias.before_loop
    async def before_verificar_noticias(self):

        await self.bot.wait_until_ready()

        print(
            "Sistema de notícias iniciado!"
        )


async def setup(bot):

    await bot.add_cog(
        News(bot)
    )