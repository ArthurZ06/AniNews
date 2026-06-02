from discord.ext import commands, tasks
import requests
import json
import os


class Anime(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.arquivo_ranking = "top_anime.json"

        self.verification_anime.start()

    def carregar_ranking(self):

        if not os.path.exists(
            self.arquivo_ranking
        ):
            return {}

        with open(
            self.arquivo_ranking,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def salvar_ranking(
        self,
        ranking
    ):

        with open(
            self.arquivo_ranking,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                ranking,
                f,
                indent=4
            )

    @tasks.loop(minutes=30)
    async def verification_anime(self):

        canal = self.bot.get_channel(
            1508215790103429170
        )

        if canal is None:
            return

        url = (
            "https://api.jikan.moe/v4/top/anime"
        )

        response = requests.get(
            url
        )

        data = response.json()

        top20 = data["data"][:20]

        ranking_anterior = (
            self.carregar_ranking()
        )

        ranking_atual = {}

        for posicao, anime in enumerate(
            top20,
            start=1
        ):

            anime_id = str(
                anime["mal_id"]
            )

            ranking_atual[
                anime_id
            ] = posicao

        # First run
        if not ranking_anterior:

            await canal.send(
                "🔥 **Top 20 Anime Ranking** 🔥"
            )

            for posicao, anime in enumerate(
                top20,
                start=1
            ):

                await canal.send(
                    f"#{posicao} - {anime['title']}"
                )

            self.salvar_ranking(
                ranking_atual
            )

            print(
                "Ranking inicial salvo."
            )

            return

        for posicao, anime in enumerate(
            top20,
            start=1
        ):

            anime_id = str(
                anime["mal_id"]
            )

            titulo = anime[
                "title"
            ]

            # New entry
            if anime_id not in ranking_anterior:

                await canal.send(
                    f"🆕 **{titulo}** **#{posicao}**"
                )

                continue

            posicao_antiga = (
                ranking_anterior[
                    anime_id
                ]
            )

            # Moved up
            if posicao < posicao_antiga:

                await canal.send(
                    f"⬆️ **{titulo}** subiu de **#{posicao_antiga}** para **#{posicao}**"
                )

            # Moved down
            elif posicao > posicao_antiga:

                await canal.send(
                    f"⬇️ **{titulo}** caiu de **#{posicao_antiga}** para **#{posicao}**"
                )

        self.salvar_ranking(
            ranking_atual
        )

    @verification_anime.before_loop
    async def before_verification_anime(self):

        await self.bot.wait_until_ready()

        print(
            "Sistema de anime iniciado!"
        )


async def setup(bot):

    await bot.add_cog(
        Anime(bot)
    )