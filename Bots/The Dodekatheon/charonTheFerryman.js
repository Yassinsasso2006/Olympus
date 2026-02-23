// 1. Imports
const { Client, IntentsBitField, EmbedBuilder, ActivityType } = require('discord.js'); //How imports look in discord.js
const fs = require('node:fs'); // Built-in tool to read files
const path = require('node:path'); // Built-in tool to handle folder paths
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

//Create a Collection to store our cogs/commands
client.commands = new Collection();

//Read the commands folder
const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
    const filePath = path.join(commandsPath, file);
    const command = require(filePath);
    
    // Set a new item in the Collection
    // Key = command name, Value = the exported module
    if ('data' in command && 'execute' in command) {
        client.commands.set(command.data.name, command);
    }
}


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
    
    // We look for the command in our Collection
    const command = client.commands.get(interaction.commandName);

    if (!command) {
        console.error(`No command matching ${interaction.commandName} was found.`);
        return;
    }

    try {
        // This runs the "execute" function inside your verify.js or unverify.js
        await command.execute(interaction);
    } catch (error) {
        console.error(error);
        if (interaction.replied || interaction.deferred) {
            await interaction.followUp({ content: 'There was an error while executing this command!', ephemeral: true });
        } else {
            await interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true });
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