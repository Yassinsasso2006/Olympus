import discord
from discord.ext import commands
from discord import app_commands, Interaction
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from utils.utils import isMod
from dotenv import load_dotenv

load_dotenv()

MAIN_GUILD_ID = int(os.getenv("MAIN_GUILD_ID"))
MAIN_LOG_CHANNEL_ID = int(os.getenv("MAIN_LOG_CHANNEL_ID"))

MOD_GUILD_ID = int(os.getenv("MOD_GUILD_ID"))
MOD_LOG_CHANNEL_ID = int(os.getenv("MOD_LOG_CHANNEL_ID"))

log_channels = {
    MAIN_GUILD_ID: MAIN_LOG_CHANNEL_ID,
    MOD_GUILD_ID: MOD_LOG_CHANNEL_ID
}

DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "memberData.json"))

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
        message_link: str = None,
        evidence1: discord.Attachment = None,
        evidence2: discord.Attachment = None,
        evidence3: discord.Attachment = None,
        evidence4: discord.Attachment = None,
        evidence5: discord.Attachment = None,
        evidence6: discord.Attachment = None,
        evidence7: discord.Attachment = None,
        evidence8: discord.Attachment = None,
        evidence9: discord.Attachment = None,
        evidence10: discord.Attachment = None
    ):
        

        evidence_attachments = [
        evidence1, evidence2, evidence3, evidence4, evidence5,
        evidence6, evidence7, evidence8, evidence9, evidence10,
    ]
        
        evidence_urls = [e.url for e in evidence_attachments if e is not None]

        
        try:

            await interaction.response.defer(ephemeral=True)

            data = self._load_data()
            user_id = str(member.id)
            unix_timestamp = int(datetime.now().timestamp())

            entry = {
                "type": "strike",
                "reason": reason,
                "moderator": interaction.user.id,
                "timestamp": unix_timestamp,
                "message link": message_link,
                "evidence":evidence_urls
            }

            if user_id not in data:
                data[user_id] = []
            data[user_id].append(entry)
            self._save_data(data)

            await interaction.followup.send(
                f"✅ {member.mention} has been struck for: {reason}", ephemeral=True
            )


            embed = discord.Embed(title= "Strike Logged", colour=discord.Color.red())
            embed.add_field(name="Handled by", value=interaction.user.mention, inline=False)
            embed.add_field(name="Timestamp", value=f"<t:{unix_timestamp}:f>", inline=False)
            embed.add_field(name="Member Struck", value=member.mention, inline=False)
            embed.add_field(name="Member ID", value=str(member.id), inline=False)

            if message_link:
                embed.add_field(name="Message Link", value=f"[Jump to message]({message_link})", inline=False)

            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Evidence", value="\n".join(evidence_urls) if evidence_urls else "No evidence provided", inline=False)
            embed.set_footer(text="This strike has been logged by Themis.")

            for guild_id, channel_id in log_channels.items():
                log_channel = self.bot.get_channel(channel_id)
                if log_channel:
                    try:
                        await log_channel.send(embed=embed)
                    except Exception as e:
                        print(f"Failed to send log to channel {channel_id}: {e}")

        except Exception as e:
            print(f"[ERROR] Exception in /strike command: {e}")
            if not interaction.response.is_done():
                await interaction.followup.send("⚠️ Something went wrong.", ephemeral=True)
async def setup(bot):
    await bot.add_cog(Strike(bot))
    print("Strike cog loaded successfully.")