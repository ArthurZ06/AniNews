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

        # Cria o arquivo caso ele não exista
        if not os.path.exists(
            self.arquivo_ranking
        ):

            with open(
                self.arquivo_ranking,
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
                self.arquivo_ranking,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except json.JSONDecodeError:

            # Se estiver vazio ou corrompido,
            # recria o arquivo.

            with open(
                self.arquivo_ranking,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    {},
                    f,
                    indent=4
                )

            return {}

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

        url = "https://api.jikan.moe/v4/top/anime"

        response = requests.get(url)

        if response.status_code != 200:
            print("Erro ao obter ranking.")
            return

        data = response.json()

        top20 = data["data"][:20]

        ranking_anterior = self.carregar_ranking()

        ranking_atual = {}

        for posicao, anime in enumerate(
            top20,
            start=1
        ):

            anime_id = str(
                anime["mal_id"]
            )

            ranking_atual[anime_id] = posicao

        # Primeira execução
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

        houve_mudanca = False

        for posicao, anime in enumerate(
            top20,
            start=1
        ):

            anime_id = str(
                anime["mal_id"]
            )

            titulo = anime["title"]

            # Novo anime
            if anime_id not in ranking_anterior:

                houve_mudanca = True

                await canal.send(
                    f"🆕 **{titulo}** entrou no ranking em **#{posicao}**"
                )

                continue

            posicao_antiga = ranking_anterior[
                anime_id
            ]

            # Subiu
            if posicao < posicao_antiga:

                houve_mudanca = True

                await canal.send(
                    f"⬆️ **{titulo}** subiu de **#{posicao_antiga}** para **#{posicao}**"
                )

            # Caiu
            elif posicao > posicao_antiga:

                houve_mudanca = True

                await canal.send(
                    f"⬇️ **{titulo}** caiu de **#{posicao_antiga}** para **#{posicao}**"
                )

        if houve_mudanca:

            mensagem = "🔥 **Top 20 Anime Atualizado** 🔥\n\n"

            for posicao, anime in enumerate(
                top20,
                start=1
            ):

                mensagem += (
                    f"**#{posicao}** - {anime['title']}\n"
                )

            await canal.send(mensagem)

        self.salvar_ranking(
            ranking_atual
        )

    @verification_anime.before_loop
    async def before_verification_anime(self):

        await self.bot.wait_until_ready()

        print(
            "Sistema de anime iniciado!"
        )

    def cog_unload(self):

        self.verification_anime.cancel()


async def setup(bot):

    await bot.add_cog(
        Anime(bot)
    )