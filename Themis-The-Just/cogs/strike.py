import discord
from discord.ext import commands
from discord import app_commands, Interaction
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from utils import isMod

DATA_FILE = "data/memberData.json"
modLogChannelId = 0#Figure out how to set this up with 2 different servers

class Strike(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def _load_data(self):
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'w') as f:
                json.dump({}, f)
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
    
    def _save_data(self, data):
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    
    @app_commands.command(name="strike", description="Issue a strike to a member")
    @isMod()
    @app_commands.describe(
        member="The member to strike",
        reason="The reason for the strike",
        message_link="Optional message link for reference"
    )

    async def strike(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided",
        message_link: str = None
    ):
        data = self._load_data()
        user_id = str(member.id)
        unix_timestamp = int(datetime.now().timestamp())

        entry = {
            "type": "strike",
            "reason": reason,
            "moderator": interaction.user.id,
            "timestamp": unix_timestamp,
            "message link": message_link
        }

        if user_id not in data:
            data[user_id] = []
        data[user_id].append(entry)
        self._save_data(data)

        await interaction.response.send_message(
            f"✅ {member.mention} has been struck for: {reason}", ephemeral=True
        )

        log_channel = self.bot.get_channel(modLogChannelId)
        if log_channel:
            embed = discord.Embed(title= "Strike Logged", colour=discord.Color.red())
            embed.add_field(name="Handled by", value=interaction.user.mention, inline=False)
            embed.add_field(name="Timestamp", value=f"<t:{unix_timestamp}:f>", inline=False)
            embed.add_field(name="Member Struck", value=member.mention, inline=False)
            embed.add_field(name="Member ID", value=str(member.id), inline=False)

            if message_link:
                embed.add_field(name="Message Link", value=f"[Jump to message]({message_link})", inline=False)

            embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_footer(text="This strike has been logged by Themis.")
            await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Strike(bot))
    print("Strike cog loaded successfully.")