from discord import app_commands, Interaction

MOD_ROLE_ID = 1376500702108586045 #1073396088603693167  # or load from env/config

def isMod():
    async def predicate(interaction: Interaction) -> bool:
        return any(role.id == MOD_ROLE_ID for role in interaction.user.roles)
    return app_commands.check(predicate)