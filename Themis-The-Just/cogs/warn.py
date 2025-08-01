import discord
from discord.ext import commands
import json
from datetime import datetime, timezone
import os
from discord import app_commands
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from utils import isMod 
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
main_modLogChannelId = MAIN_LOG_CHANNEL_ID
mod_modLogChannelId = MOD_LOG_CHANNEL_ID
modRoleId = 1073396088603693167 # The Council of Elders role ID


class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    def _load_data(self):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
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
        try:
            await interaction.response.defer(ephemeral=True)


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

            await interaction.followup.send(
                f"✅ {member.mention} has been warned for: {reason}", ephemeral=True
            )

            
            embed = discord.Embed(title="⚖️ Warning Logged", colour=discord.Color.orange())
            embed.add_field(name="Handled by", value=interaction.user.mention, inline=False)
            embed.add_field(name="Timestamp", value=f"<t:{unix_timestamp}:f>", inline=False)
            embed.add_field(name="Member Warned", value=member.mention, inline=False)
            embed.add_field(name="Member ID", value=str(member.id), inline=False)

            if message_link:
                embed.add_field(name="Message Link", value=f"[Jump to message]({message_link})", inline=False)

            embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_footer(text="This warning has been logged by Themis.")
            
            for guild_id, channel_id in log_channels.items():
                log_channel = self.bot.get_channel(channel_id)
                if log_channel:
                    try:
                        await log_channel.send(embed=embed)
                    except Exception as e:
                        print(f"Failed to send log to channel {channel_id}: {e}")
        except Exception as e:
            print(f"[ERROR] Exception in /warn command: {e}")
            if not interaction.response.is_done():
                await interaction.followup.send("⚠️ Something went wrong.", ephemeral=True)
async def setup(bot):
    await bot.add_cog(Warn(bot))
    print("Warn cog loaded successfully.")