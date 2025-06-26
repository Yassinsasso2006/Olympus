import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env file
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # needed for reading messages

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

bot.run(TOKEN)
