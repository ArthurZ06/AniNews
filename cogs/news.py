from discord.ext import commands, tasks
import discord
import feedparser
from bs4 import BeautifulSoup
import json
import os

FEED_URL = "https://www.intoxianime.com/feed/"
CHANNEL_ID = 1495959671658516550


class News(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.sent_posts_file = "sent_posts.json"
        self.sent_posts = self.load_sent_posts()

        self.check_news.start()

    # Load previously sent posts

    def load_sent_posts(self):

        # Create the file if it does not exist
        if not os.path.exists(self.sent_posts_file):

            with open(
                self.sent_posts_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    [],
                    f,
                    indent=4
                )

            return set()

        try:

            with open(
                self.sent_posts_file,
                "r",
                encoding="utf-8"
            ) as f:

                return set(json.load(f))

        except json.JSONDecodeError:

            # If the file is empty or corrupted,
            # recreate it.
            with open(
                self.sent_posts_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    [],
                    f,
                    indent=4
                )

            return set()

    # Save sent posts to the local file

    def save_sent_posts(self):

        with open(
            self.sent_posts_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                list(self.sent_posts),
                f,
                indent=4
            )

    # Extract the first image from a feed entry

    def get_image(self, post):

        if "content" in post:

            for content in post.content:

                soup = BeautifulSoup(
                    content.value,
                    "html.parser"
                )

                images = soup.find_all("img")

                for img in images:

                    url = (
                        img.get("src")
                        or img.get("data-src")
                    )

                    if not url and img.get("srcset"):

                        srcset_images = (
                            img.get("srcset")
                            .split(",")
                        )

                        last_image = srcset_images[-1]

                        url = (
                            last_image
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
    async def check_news(self):

        channel = self.bot.get_channel(
            CHANNEL_ID
        )

        if channel is None:

            print(
                "Channel not found."
            )

            return

        feed = feedparser.parse(
            FEED_URL
        )

        # Check the latest 20 feed entries
        posts = list(
            reversed(
                feed.entries[:20]
            )
        )

        for post in posts:

            if (
                post.link
                in self.sent_posts
            ):
                continue

            self.sent_posts.add(
                post.link
            )

            self.save_sent_posts()

            image = self.get_image(
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

            if image:

                embed.set_image(
                    url=image
                )

            else:

                embed.set_thumbnail(
                    url="https://cdn-icons-png.flaticon.com/512/5968/5968885.png"
                )

            await channel.send(
                embed=embed
            )

    @check_news.before_loop
    async def before_check_news(self):

        await self.bot.wait_until_ready()

        print(
            "News system started!"
        )

    def cog_unload(self):

        self.check_news.cancel()


async def setup(bot):

    await bot.add_cog(
        News(bot)
    )