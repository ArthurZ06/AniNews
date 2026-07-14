# Import required libraries

import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


async def main():

    async with bot:

        await bot.load_extension("cogs.news")
        await bot.load_extension("cogs.top_anime")

        await bot.start(TOKEN)


asyncio.run(main())