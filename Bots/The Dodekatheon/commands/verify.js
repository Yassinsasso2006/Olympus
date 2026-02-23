const { SlashCommandBuilder, PermissionFlagsBits } = require('discord.js'); //Importing
const db = require('../db'); //Connecting to database

module.exports = {
    //Building the /verify command
    data: new SlashCommandBuilder()
        .setName('verify')
        .setDescription('Verify a user by removing Unverified and adding standard roles.')
        .addUserOption(option => 
            option.setName('member')
                .setDescription('The member to verify')
                .setRequired(true))
        .addBooleanOption(option =>
            option.setName('watchlist status')
                .setDescription('Is this memeber suspicious enough to be put on a watchlist immediately so the mods know to keep an eye on them?')
                .setRequired(false)
        )
        .setDefaultMemberPermissions(PermissionFlagsBits.ManageRoles),

    async execute(interaction) {
        const targetMember = interaction.options.getMember('member');
        const guild = interaction.guild;

        // 1. Defer the reply since role changes take time [This is to tell the discord API to wait and that more is coming]
        await interaction.deferReply({ ephemeral: true });

        try {
            // FETCH SETTINGS FROM DATABASE
            // Instead of hardcoding, we ask the DB for the role list
            const settingsRes = await db.query(
                'SELECT "settingValue" FROM public.settings WHERE "settingKey" = $1', 
                ['roles_to_add_on_verify'] //Have them in 1 value but seperate them with commas and no spaces
            );
            //Fetching the 'Unverified' role from the settings table
            const unverifiedSetting = await db.query(
                'SELECT "settingValue" FROM public.settings WHERE "settingKey" = $1', 
                ['role_unverified_id']
            );

            // Turn our comma-separated string from the DB back into an Array
            const rolesToAdd = settingsRes.rows[0].settingValue.split(',');
            const unverifiedRoleId = unverifiedSetting.rows[0].settingValue;

            // ROLE CHECKS
            // Check if they are missing the Unverified role
            const isNotUnverified = !targetMember.roles.cache.has(unverifiedRoleId);

            // Check if they already have the FIRST banner role in your verified list (as a shortcut)
            const isAlreadyVerifiedFirstRole = targetMember.roles.cache.has(rolesToAdd[0]);

            //Check if they already have the LAST banner role in your unverified list (as a shortcut)
            const isAlreadyVerifiedLastRole = targetMember.roles.cache.has(rolesToAdd[rolesToAdd.length-1])

            //This checks that the memeber does not have the 'Unverified Role' and also makes sure that the member has the first and last banner role before saying that he is verified
            if (isNotUnverified || isAlreadyVerifiedFirstRole || isAlreadyVerifiedLastRole) {
                return await interaction.editReply("❌ This member is already verified or is not in the 'Unverified' state.");
            }

            // 4. THE ACTION
            await targetMember.roles.remove(unverifiedRoleId);
            await targetMember.roles.add(rolesToAdd);

            // 5. DATABASE LOGGING (Permanent record)

            //Checking to see if the member's supposed to be on the watchlist
            const isWatchlisted = interaction.options.getBoolean('watchlist') ?? false;

            //Logging inside the database
            await db.query(
                'INSERT INTO charon."verficationLogs" ("discordID", "verifiedBy", "watchlistStatus", "isVerify") VALUES ($1, $2, $3, $4)',
                [targetMember.id, interaction.user.id, isWatchlisted, true]
            );

            // 6. SUCCESS MESSAGE
            await interaction.editReply(`✅ ${targetMember.user.tag} has been successfully verified!`);
            
            // Send the public welcome message
            await interaction.channel.send(
                `🎉 Congratulations, ${targetMember}! Please head over to <id:customize> to collect your roles. Be sure you have followed the <id:guide> to fulfill your journey of initiation into the Lounge! Now, sit back, relax and enjoy! ❤️`
            );
          //If an error occurs this message is sent to the mods
        } catch (error) {
            console.error("Verification Error:", error);
            await interaction.editReply("⚠️ Fates were unkind. Charon got stuck in traffic... Something went wrong during verification");
        }
    },
};