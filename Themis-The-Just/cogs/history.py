import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timezone
import json
import os
from utils import isMod

DATA_FILE = "data/memberData.json"
modLogChannelId = 0  # Figure out how to set this up with 2

class History(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def _load_data(self):
        if not os.path.exists(DATA_FILE):
            return {}
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    
    @app_commands.command(name="history", description="View a member's warning/strike history")
    @isMod()
    @app_commands.describe(member="The member whose history to view")
    async def history(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):
        data = self._load_data()
        user_id = str(member.id)

        if user_id not in data or not data[user_id]:
            await interaction.response.send_message(
                f"✅ {member.mention} has a clean record.", empheral=True
            )
            return
        
        history_entries = data[user_id]
        history_embed = discord.Embed(
            title=f"📜 History for {member}",
            colour = discord.Color.gold()
        )

        for entry in history_entries[-10]: #Shows last 10 entries max, make sure this works
            timestamp = f"<t{entry['timestamp']}:f>"
            modterator = f"<@{entry['moderator']}>"
            reason = entry['reason']
            entry_type = entry['type'].capitalize()
            message_link = entry.get('message link', 'No link provided')

            value = f"**Type:** {entry_type}\n" \
                    f"**Moderator:** {modterator}\n" \
                    f"**Reason:** {reason}\n" \
                    f"**Timestamp:** {timestamp}\n" \
                    f"**Message Link:** {message_link}"
            if message_link:
                value += f"\n[Jump to Message]({message_link})"
            
            history_embed.add_field(name="\u200b", value=value, inline=False)
        
        history_embed.set_footer(text=f"Total entries: {len(history_entries)}")
        await interaction.response.send_message(embed=history_embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(History(bot))
    print("History cog loaded successfully.")