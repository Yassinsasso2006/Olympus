import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Themis is watching...")
    print(f"[✓] {bot.user.name} is online.")
    try:
        synced = await bot.tree.sync()
        print(f"[✓] Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"[!] Failed to sync commands: {e}")

async def load_cogs():
    await bot.load_extension("cogs.warn")
    await bot.load_extension("cogs.strike")
    await bot.load_extension("cogs.history")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())