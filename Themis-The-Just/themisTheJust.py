import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True


async def on_ready():
    print(f"Themis is watching... Logged in as {bot.user}")
    await bot.tree.sync()

async def load_cogs():
    await bot.load_extension("cogs.report")
    await bot.load_extension("cogs.strike")
    await bot.load_extension("cogs.history")

bot.loop.create_task(load_cogs())
bot.run(TOKEN)