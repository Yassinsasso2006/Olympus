// 1. Imports
const { Client, IntentsBitField, EmbedBuilder, ActivityType } = require('discord.js');
const db = require('./db'); // Our shared DB connection
require('dotenv').config();

// 2. Intents (Permission requirements)
const client = new Client({
    intents: [
        IntentsBitField.Flags.Guilds,
        IntentsBitField.Flags.GuildMembers,
        IntentsBitField.Flags.GuildMessages
    ]
});

// 3. Configuration (IDs converted to Strings for safety) //Make these dynamic later through the dashboard. Only accessable by the admin
const UNVERIFIED_ROLE_ID = "1059289964124323880";
const MOD_ROLE_ID = "1073396088603693167"; 
const MOD_LOG_CHANNEL_ID = "1393736874069327963";
const ROLES_TO_ADD = [
    "1059289967827894333", // Verified
    "1064171885081919518", // Peasant of Prose
    "1077367546740736161", // Lounge ID
    "1077367715607609415", // Writing Badge
    "1077367888542961675", // Spy Database
    "1077368081506119680", // Quests
    "1077368229376307252", // Summoning Spells
    "1077368412524785835"  // Comm System
];

// 4. On Ready Event (The "Status" and Login message)
client.once('ready', async () => {
    console.log(`✅ Charon is online as ${client.user.tag}`);

    const statuses = ["Verifying souls", "Guiding spirits", "Ferrying users"];
    
    //Create a function to change the status
    const updateStatus = () => {
        const randomStatus = statuses[Math.floor(Math.random() * statuses.length)];
        client.user.setActivity(randomStatus, { type: ActivityType.Playing });
    };

    //Run it immediately so the bot doesn't start with nothing
    updateStatus();

    //Set an interval to run it every 10 minutes (600,000 milliseconds)
    setInterval(updateStatus, 600000); 
});

// 5. Slash Command Handling
client.on('interactionCreate', async (interaction) => {
    if (!interaction.isChatInputCommand()) return;

    const { commandName, options, guild, member: moderator } = interaction;

    if (commandName === 'verify') {
        const targetMember = options.getMember('member');

        // Check for Moderator Role
        if (!moderator.roles.cache.has(MOD_ROLE_ID)) {
            await interaction.reply({ content: "❌ You must be a moderator to use this.", ephemeral: true });
            
            // Log unauthorized attempt to Discord
            const logChannel = guild.channels.cache.get(MOD_LOG_CHANNEL_ID);
            if (logChannel) {
                logChannel.send(`⚠️ Unauthorized verify attempt by ${moderator.user.tag}`);
            }
            return;
        }

        // Defer reply (like Python's await interaction.response.defer)
        await interaction.deferReply();

        try {
            // Remove Unverified role
            await targetMember.roles.remove(UNVERIFIED_ROLE_ID);
            // Add all the new roles
            await targetMember.roles.add(ROLES_TO_ADD);

            // 🏛️ DATABASE LOGGING (The Olympus way)
            const sql = `
                INSERT INTO charon."verficationLogs" ("discordID", "verifiedBy")
                VALUES ($1, $2)
                ON CONFLICT ("discordID") DO UPDATE SET "verifiedAt" = NOW();
            `;
            await db.query(sql, [targetMember.id, moderator.id]);

            // Discord Logging
            const logChannel = guild.channels.cache.get(MOD_LOG_CHANNEL_ID);
            if (logChannel) {
                logChannel.send(`✅ **${targetMember.user.tag}** verified by **${moderator.user.tag}**.`);
            }

            // Final message to user
            await interaction.editReply(`🎉 Congratulations, ${targetMember}! Head to <id:customize> and enjoy the Lounge!`);

        } catch (error) {
            console.error(error);
            await interaction.editReply("❌ Failed to manage roles. Check my permissions!");
        }
    }
});

// 6. Graceful Shutdown (The 'Signal' handlers)
const handleShutdown = async () => {
    console.log("\n🔴 Shutting down Charon...");
    client.destroy(); // Closes the bot connection
    process.exit(0);
};

process.on('SIGINT', handleShutdown);
process.on('SIGTERM', handleShutdown);

client.login(process.env.TOKEN_CHARON);