import discord
from discord.ext import commands
import json
from datetime import datetime, timezone
import os
from discord import app_commands
from utils import isMod 

DATA_FILE = "data/memberData.json"
modLogChannelId = 0  # Figure out how to set this up with 2 different servers
modRoleId = 1073396088603693167 # The Council of Elders role ID


class Warn(commands.Cog):
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

    @discord.app_commands.command(name="warn", description="Issue a warning to a member")
    @isMod()
    @app_commands.describe(member="The member to warn", reason="Reason for the warning")
    async def warn(
        self,
        interaction: discord.Interaction,
        member: discord.Member, 
        reason: str = "No reason provided",
        message_link: str = None
        ):
        data = self._load_data()
        user_id = str(member.id)
        unix_timestamp = int(datetime.now(timezone.utc).timestamp())

        entry = {
            "type": "warning",
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
            f"✅ {member.mention} has been warned for: {reason}", ephemeral=True
        )

        log_channel = self.bot.get_channel(modLogChannelId)
        if log_channel:
            embed = discord.Embed(title="⚖️ Warning Logged", colour=discord.Color.orange())
            embed.add_field(name="Handled by", value=interaction.user.mention, inline=False)
            embed.add_field(name="Timestamp", value=f"<t:{unix_timestamp}:f>", inline=False)
            embed.add_field(name="Member Warned", value=member.mention, inline=False)
            embed.add_field(name="Member ID", value=str(member.id), inline=False)

            if message_link:
                embed.add_field(name="Message Link", value=f"[Jump to message]({message_link})", inline=False)

            embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_footer(text="This warning has been logged by Themis.")
            await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Warn(bot))
    print("Warn cog loaded successfully.")