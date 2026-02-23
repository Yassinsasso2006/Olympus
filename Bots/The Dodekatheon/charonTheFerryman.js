// 1. Imports
const { Client, IntentsBitField, ActivityType, Collection } = require('discord.js'); // Added Collection here
const fs = require('node:fs'); 
const path = require('node:path'); 
const db = require('./db'); 
require('dotenv').config();

// 2. Intents
const client = new Client({
    intents: [
        IntentsBitField.Flags.Guilds,
        IntentsBitField.Flags.GuildMembers,
        IntentsBitField.Flags.GuildMessages
    ]
});

// 3. Command Handler (The "Cogs" Loader)
client.commands = new Collection();

const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
    const filePath = path.join(commandsPath, file);
    const command = require(filePath);
    
    // Safety check: ensure the file has the required properties
    if ('data' in command && 'execute' in command) {
        client.commands.set(command.data.name, command);
    } else {
        console.log(`[WARNING] The command at ${filePath} is missing "data" or "execute".`);
    }
}

// 4. On Ready Event
client.once('ready', async () => {
    console.log(`✅ Charon is online as ${client.user.tag}`);

    const statuses = ["Verifying souls", "Guiding spirits", "Ferrying users"];
    
    const updateStatus = () => {
        const randomStatus = statuses[Math.floor(Math.random() * statuses.length)];
        client.user.setActivity(randomStatus, { type: ActivityType.Playing });
    };

    updateStatus();
    setInterval(updateStatus, 600000); 
});

// 5. Slash Command Handling (The "Gear Turner")
client.on('interactionCreate', async (interaction) => {
    if (!interaction.isChatInputCommand()) return;
    
    const command = client.commands.get(interaction.commandName);

    if (!command) {
        console.error(`No command matching ${interaction.commandName} was found.`);
        return;
    }

    try {
        // This executes the logic inside your separate command files
        await command.execute(interaction);
    } catch (error) {
        console.error(error);
        const errorMessage = { content: '⚠️ The ferry stalled... an error occurred!', ephemeral: true };
        
        if (interaction.replied || interaction.deferred) {
            await interaction.followUp(errorMessage);
        } else {
            await interaction.reply(errorMessage);
        }
    }
});

// 6. Graceful Shutdown
const handleShutdown = async () => {
    console.log("\n🔴 Shutting down Charon...");
    client.destroy(); 
    process.exit(0);
};

process.on('SIGINT', handleShutdown);
process.on('SIGTERM', handleShutdown);

client.login(process.env.TOKEN_CHARON);