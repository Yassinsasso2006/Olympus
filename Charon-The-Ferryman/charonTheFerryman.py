import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load bot token from .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# Set up bot
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree  # slash command handler

# Role configuration
# Variable intialization
UNVERIFIED_ROLE_NAME = 1059289964124323880
ROLES_TO_ADD = [
    1059289967827894333, #Verified
    1064171885081919518, #Peasant of Prose(Lvl. 1)
    1077367546740736161, #《──────Lounge ID──────》
    1077367715607609415, #《──────Writing Badge──────》
    1077367888542961675, #《──────Spy Database──────》
    1077368081506119680, #《──────Quests──────》
    1077368229376307252, #《────Summoning Spells────》
   1077368412524785835 #《──────Comm System──────》
]

MOD_LOG_CHANNEL_ID = 1393736874069327963


@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")
    try:
        synced = await tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"❌ Failed to sync slash commands: {e}")

# Slash command: /verify @member

@tree.command(name="verify", description="Verify a user by removing 'Unverified' and adding standard roles.")
@app_commands.describe(member="The member to verify")
async def verify_user(interaction: discord.Interaction, member: discord.Member):
    guild = interaction.guild

    required_role = interaction.guild.get_role(1073396088603693167)  # Moderator role

    if required_role not in interaction.user.roles:
        await interaction.response.send_message("❌ You must be a moderator to use this command.", ephemeral=True)

        # ✅ Log the failed attempt
        log_channel = interaction.guild.get_channel(MOD_LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(
                f"❌ Unauthorized attempt: {interaction.user.mention} (ID: {interaction.user.id}) tried to use `/verify` on {member.display_name}, but lacks the required moderator role. <@&1073396088603693167> be careful!"
            )
        return

    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message("❌ You don't have permission to verify members.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=False)

    unverified_role = guild.get_role(UNVERIFIED_ROLE_NAME)
    roles_to_add = [guild.get_role(role_id) for role_id in ROLES_TO_ADD]

    if unverified_role is None or any(r is None for r in roles_to_add):
        await interaction.followup.send("⚠️ One or more roles were not found. Please check role IDs.")
        return

    if unverified_role not in member.roles:
        await interaction.followup.send(f"{member.mention} is already verified or missing the 'Unverified' role.")
        return

    try:
        await member.remove_roles(unverified_role)
        await member.add_roles(*roles_to_add)

        log_channel = guild.get_channel(MOD_LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(
                f"✅ {member.mention} has been verified and given roles: {', '.join(role.name for role in roles_to_add)}"
            )
            await log_channel.send(
                f"🛠️ {interaction.user.display_name} verified {member.mention} using `/verify`."
            )


        # ✅ REQUIRED: send a follow-up message to complete the interaction
        await interaction.followup.send(
        f"🎉 Congratulations, {member.mention}! Please head over to <id:customize> and collect your roles. Be sure you have followed the <id:guide> to fulfill your journey of initiation into the Lounge!"
            "Now, sit back, relax and enjoy! ❤️"
        )

    except discord.Forbidden:
        await interaction.followup.send(
            "❌ I don’t have permission to manage those roles.", ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(
            f"⚠️ Something went wrong: {e}", ephemeral=True
        )

    except discord.Forbidden:
        await interaction.followup.send("❌ I don’t have permission to manage those roles.")
    except Exception as e:
        await interaction.followup.send(f"⚠️ Something went wrong: {e}")




# Slash command: /unverify @member
@app_commands.checks.has_role(1073396088603693167)  #The Council of Elders role ID
@tree.command(name="unverify", description="Remove verified roles and reassign 'Unverified' role.")
@app_commands.describe(member="The member to unverify")
async def unverify_user(interaction: discord.Interaction, member: discord.Member):
    guild = interaction.guild

    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message("❌ You don't have permission to unverify members.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=False)

    unverified_role = guild.get_role(UNVERIFIED_ROLE_NAME)
    roles_to_remove = [guild.get_role(role_id) for role_id in ROLES_TO_ADD]

    if unverified_role is None or any(r is None for r in roles_to_remove):
        await interaction.followup.send("⚠️ One or more roles were not found. Please check role IDs.")
        return

    try:
        await member.remove_roles(*roles_to_remove)
        await member.add_roles(unverified_role)

        await interaction.followup.send(
            f"❌ {member.mention} has been unverified and their roles were removed."
        )

        log_channel = guild.get_channel(MOD_LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(
                f"🛑 {interaction.user.display_name} unverified {member.mention} using `/unverify`."
            )
            


    except discord.Forbidden:
        await interaction.followup.send("❌ I don’t have permission to manage those roles.")
    except Exception as e:
        await interaction.followup.send(f"⚠️ Something went wrong: {e}")






# Run the bot
bot.run(TOKEN)