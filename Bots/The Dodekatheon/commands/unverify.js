const { SlashCommandBuilder, PermissionFlagsBits } = require('discord.js'); //importing libraries
const db = require('../db'); //Connecting to database

module.exports = {
    //Building the /unverify command
    data: new SlashCommandBuilder()
        .setName('unverify')
        .setDescription("Remove a user's access and return them to the Unverified state.")
        .addUserOption(option => 
            option.setName('member')
                .setDescription('The member to unverify')
                .setRequired(true))
        .setDefaultMemberPermissions(PermissionFlagsBits.ManageRoles),

    async execute(interaction) {
        const targetMember = interaction.options.getMember('member');

        //Defer tells discord to wait and that the interactionisn't done
        await interaction.deferReply({ ephemeral: true });

        try {
            // 1. Fetch settings (Same as verify)
            const settingsRes = await db.query('SELECT "settingValue" FROM public.settings WHERE "settingKey" = $1', ['roles_to_add_on_verify']);
            const unverifiedSetting = await db.query('SELECT "settingValue" FROM public.settings WHERE "settingKey" = $1', ['role_unverified_id']);

            const rolesToRemove = settingsRes.rows[0].settingValue.split(',');
            const unverifiedRoleId = unverifiedSetting.rows[0].settingValue;

            // 2. CHECK: Is the member actually verified?
            // If they don't have the first role in the verified list, they probably aren't verified.
            if (!targetMember.roles.cache.has(rolesToRemove[0] || !targetMember.roles.cache.has(rolesToRemove[rolesToRemove.length -1]))) {
                return await interaction.editReply("❌ This member does not appear to be verified.");
            }

            // 3. THE REVERSAL
            await targetMember.roles.remove(rolesToRemove);
            await targetMember.roles.add(unverifiedRoleId);

            // 4. LOGGING (Optional: You could create a separate table for unverify logs)
            console.log(`Log: ${interaction.user.tag} unverified ${targetMember.user.tag}`);

            // 5. SUCCESS MESSAGES
            await interaction.editReply(`🛑 ${targetMember.user.tag} has been unverified.`);
            
            // Log to the mod-log channel (using the ID from your config)
            const MOD_LOG_CHANNEL_ID = "1393736874069327963";
            const logChannel = interaction.guild.channels.cache.get(MOD_LOG_CHANNEL_ID);
            if (logChannel) {
                logChannel.send(`🛑 **${interaction.user.tag}** unverified **${targetMember.user.tag}**.`);
            }

        } catch (error) {
            console.error("Unverify Error:", error);
            await interaction.editReply("⚠️ The ferry is going the wrong way! Something went wrong.");
        }
    },
};