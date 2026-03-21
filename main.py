import discord
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("봇 준비 완료")

async def load_cogs():
    await bot.load_extension("cogs.yeonsam")
    await bot.load_extension("cogs.welcome")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv("TOKEN"))

asyncio.run(main())