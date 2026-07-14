from discord.ext import commands, tasks
import requests
import json
import os


class Anime(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.ranking_file = "top_anime.json"

        self.check_anime_ranking.start()

    # Load the saved ranking

    def load_ranking(self):

        # Create the file if it does not exist
        if not os.path.exists(
            self.ranking_file
        ):

            with open(
                self.ranking_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    {},
                    f,
                    indent=4
                )

            return {}

        try:

            with open(
                self.ranking_file,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except json.JSONDecodeError:

            # If the file is empty or corrupted,
            # recreate it.
            with open(
                self.ranking_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    {},
                    f,
                    indent=4
                )

            return {}

    # Save the current ranking

    def save_ranking(
        self,
        ranking
    ):

        with open(
            self.ranking_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                ranking,
                f,
                indent=4
            )

    @tasks.loop(minutes=30)
    async def check_anime_ranking(self):

        channel = self.bot.get_channel(
            1508215790103429170
        )

        if channel is None:
            return

        url = "https://api.jikan.moe/v4/top/anime"

        response = requests.get(url)

        if response.status_code != 200:
            print("Failed to fetch ranking.")
            return

        data = response.json()

        top20 = data["data"][:20]

        previous_ranking = self.load_ranking()

        current_ranking = {}

        for position, anime in enumerate(
            top20,
            start=1
        ):

            anime_id = str(
                anime["mal_id"]
            )

            current_ranking[anime_id] = position

        # First execution
        if not previous_ranking:

            await channel.send(
                "🔥 **Top 20 Anime Ranking** 🔥"
            )

            for position, anime in enumerate(
                top20,
                start=1
            ):

                await channel.send(
                    f"#{position} - {anime['title']}"
                )

            self.save_ranking(
                current_ranking
            )

            print(
                "Initial ranking saved."
            )

            return

        ranking_changed = False

        for position, anime in enumerate(
            top20,
            start=1
        ):

            anime_id = str(
                anime["mal_id"]
            )

            title = anime["title"]

            # New anime
            if anime_id not in previous_ranking:

                ranking_changed = True

                await channel.send(
                    f"🆕 **{title}** entrou no ranking em **#{position}**"
                )

                continue

            previous_position = previous_ranking[
                anime_id
            ]

            # Moved up
            if position < previous_position:

                ranking_changed = True

                await channel.send(
                    f"⬆️ **{title}** subiu de **#{previous_position}** para **#{position}**"
                )

            # Moved down
            elif position > previous_position:

                ranking_changed = True

                await channel.send(
                    f"⬇️ **{title}** caiu de **#{previous_position}** para **#{position}**"
                )

        if ranking_changed:

            message = "🔥 **Top 20 Anime Atualizado** 🔥\n\n"

            for position, anime in enumerate(
                top20,
                start=1
            ):

                message += (
                    f"**#{position}** - {anime['title']}\n"
                )

            await channel.send(message)

        self.save_ranking(
            current_ranking
        )

    @check_anime_ranking.before_loop
    async def before_check_anime_ranking(self):

        await self.bot.wait_until_ready()

        print(
            "Anime ranking system started!"
        )

    def cog_unload(self):

        self.check_anime_ranking.cancel()


async def setup(bot):

    await bot.add_cog(
        Anime(bot)
    )