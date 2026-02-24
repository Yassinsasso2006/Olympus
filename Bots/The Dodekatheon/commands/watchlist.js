const { SlashCommandBuilder, PermissionFlagsBits } = require('discord.js');
const db = require('../db');

module.exports = {
    owner: 'themisTheEmbodimentOfJustice',
    data: new SlashCommandBuilder()
        .setName('watchlist')
        .setDescription('Add or remove a user from the watchlist')
        .addUserOption(option => option.setName('target').setDescription('The user to flag').setRequired(true))
        .addBooleanOption(option => option.setName('status').setDescription('set to true to flag the member, set to false to clear the member\'s name').setRequired(true))
        .setDefaultMemberPermissions(PermissionFlagsBits.ModerateMembers),

    async execute(interaction) {
        const target = interaction.options.getUser('target');
        const status = interaction.options.getBoolean('status');

        await interaction.deferReply({ ephemeral: true });

        try {
            // Update the most recent log for this user
            const result = await db.query(
                `UPDATE charon."verficationLogs" 
                 SET "watchlistStatus" = $1 
                 WHERE "discord_id" = $2 
                 RETURNING *`,
                [status, target.id]
            );

            if (result.rowCount === 0) {
                return await interaction.editReply("❌ That user has no verification record in the database.");
            }

            const state = status ? "🚩 added to" : "✅ removed from";
            await interaction.editReply(`User **${target.tag}** has been ${state} the watchlist.`);

        } catch (error) {
            console.error(error);
            await interaction.editReply("⚠️ Failed to update the Scales of Justice.");
        }
    }
};