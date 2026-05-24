# IMPORTS
import discord
from discord.ext import commands, tasks
import requests
import os   
from dotenv import load_dotenv


# pegando o token do .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} Hello World! Estou pronto para usar!")

    verificar_anime.start()  # Inicia a tarefa de verificar anime

@bot.command()
async def mantega(ctx):
    await ctx.send("Mantega é o melhor anime de todos os tempos! 🧈")

@bot.command()
async def falar(ctx, *, mensagem):
    await ctx.send(f"Você disse: {mensagem}")

@bot.command()
async def soma(ctx, num1: int, num2: int):
    resultado = num1 + num2
    await ctx.send(f"A soma de {num1} e {num2} é: {resultado}")


@tasks.loop(minutes=10)
async def verificar_anime():

    canal = bot.get_channel(1508215790103429170)

    url = "https://api.jikan.moe/v4/top/anime"

    response = requests.get(url)

    data = response.json()

    top5 = data["data"][:5]
    for anime in top5:
        await canal.send(f"Anime em alta: {anime['title']}")




# evento de quando o bot estiver pronto
bot.run(TOKEN)

