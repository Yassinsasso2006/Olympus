import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
import signal  # Used to handle graceful shutdowns
import sys
import asyncio  # Async operations
from pathlib import Path

# Load bot token from .env using an absolute path relative to this script
script_dir = Path(__file__).resolve().parent
dotenv_path = script_dir / ".env"
load_dotenv(dotenv_path=dotenv_path)
TOKEN = os.getenv("TOKEN")

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# Set up bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Graceful shutdown function
async def shutdown():
    print("🔴 Shutting down gracefully...")
    await bot.change_presence(status=discord.Status.offline)
    await bot.close()
    print("✅ Shutdown complete.")

# Define a setup_hook to safely assign shutdown handlers once the loop is running
async def custom_setup_hook():
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown()))
        except NotImplementedError:
            # Windows fallback
            if sig == signal.SIGINT:
                signal.signal(signal.SIGINT, lambda sig, frame: asyncio.create_task(shutdown()))

bot.setup_hook = custom_setup_hook
tree = bot.tree  # slash command handler

# Role configuration IDs
UNVERIFIED_ROLE_NAME = 1059289964124323880
ROLES_TO_ADD = [
    1059289967827894333, # Verified
    1064171885081919518, # Peasant of Prose(Lvl. 1)
    1077367546740736161, # 《──────Lounge ID──────》
    1077367715607609415, # 《──────Writing Badge──────》
    1077367888542961675,  # 《──────Spy Database──────》
    1077368081506119680, # 《──────Quests──────》
    1077368229376307252, # 《────Summoning Spells────》
    1077368412524785835  # 《──────Comm System──────》
]

MOD_LOG_CHANNEL_ID = 1393736874069327963

# Authorized Moderator Roles allowed to run verification/unverification
ALLOWED_MOD_ROLES = [
    1073396088603693167, # Original Moderator / Council role
    1465334314332852367  # General Chat Moderator role
]


@bot.event
async def on_ready():
    statuses = ["Verifying souls", "Guiding spirits", "Ferrying users"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))
    channel = bot.get_channel(1077299662526107808)
    if channel:
        await channel.send("🔧 Bot is now online and ready.")
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
    # Defer immediately using followup workflow to prevent 3-second timeouts completely
    await interaction.response.defer(ephemeral=False)

    guild = interaction.guild

    # Check if user has at least one authorized mod role
    has_permission = any(role.id in ALLOWED_MOD_ROLES for role in interaction.user.roles)

    if not has_permission:
        await interaction.followup.send("❌ You must be a moderator to use this command.", ephemeral=True)

        # Log the failed attempt
        log_channel = interaction.guild.get_channel(MOD_LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(
                f"❌ Unauthorized attempt: {interaction.user.mention} (ID: {interaction.user.id}) tried to use `/verify` on {member.display_name}, but lacks a required moderator role. <@&1073396088603693167> <@&1465334314332852367> be careful!"
            )
        return

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

        # Send a follow-up message to complete the interaction
        await interaction.followup.send(
            f"🎉 Congratulations, {member.mention}! Please head over to <id:customize> and collect your roles. Be sure you have followed the <id:guide> to fulfill your journey of initiation into the Lounge! Now, sit back, relax and enjoy! ❤️"
        )

    except discord.Forbidden:
        await interaction.followup.send("❌ I don’t have permission to manage those roles.")
    except Exception as e:
        await interaction.followup.send(f"⚠️ Something went wrong: {e}")


# Global Error Handler for /verify to catch invalid usernames before the command runs
@verify_user.error
async def verify_user_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.errors.TransformerError):
        error_msg = "❌ Could not find that member. Please make sure to mention them or select them from the Discord user drop-down list!"
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(error_msg, ephemeral=True)
            else:
                await interaction.followup.send(error_msg, ephemeral=True)
        except Exception:
            pass
    else:
        print(f"An unexpected error occurred in /verify: {error}")


# Slash command: /unverify @member
@tree.command(name="unverify", description="Remove verified roles and reassign 'Unverified' role.")
@app_commands.describe(member="The member to unverify")
async def unverify_user(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.defer(ephemeral=False)

    guild = interaction.guild

    # Check if user has at least one authorized mod role
    has_permission = any(role.id in ALLOWED_MOD_ROLES for role in interaction.user.roles)

    if not has_permission:
        await interaction.followup.send("❌ You do not have the required role to use this command.", ephemeral=True)
        return

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