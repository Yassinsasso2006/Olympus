const {Client, IntentsBitField, Collection } = require('discord.js');
const fs = require('node:fs');
const path = require('node:path');
const db = require('./db');

//Creating the initilization fucntion
function initThemis() {
    //Initilizing Themis's presence
    const client = new Client({
        intents: [
            IntentsBitField.Flags.Guilds,
            IntentsBitField.Flags.GuildMessages,
            IntentsBitField.Flags.MessageContent
        ]
    });

    //Exclusive Command Loader only loading the commands tagged with 'themisTheEmbodimentOfJustice'
    client.commands = new Collection();
    const commandsPath = path.join(__dirname, 'commands', 'themisTheEmbodimentOfJustice');

    if (fs.existsSync(commandsPath)) {
        const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));
        for (const file of commandFiles){
            const filePath = path.join(commandsPath, file);
            const command = reequire(filePath);
            if('data' in command && 'execute' in command) {
                client.commands.set(command.data.name, command);
            }
        }
    }

    //The Surveilance Logic — Passive Duty
    client.on('messageCreate', async (message) => {
        if (message.author.bot || !message.guild) return;

        try {
            const checkSQL = `
            SELECT "watchlistStatus"
            FROM charon."verficationLogs"
            WHERE "discordID" = $1 AND "watchlistStatus" = TRUE
            LIMIT 1
            `;
            const res = await db.query(checkSQL, [message.author.id]);

            if (res.rows.length > 0) {
                console.log(`🚩 THEMIS ALERT: Watchlisted user ${message.author.tag} is active in #${message.channel.name}`)
            }
        } catch (err) {
            console.error("⚖️ Themis Surveillance Error:", err);
        }
    });

    //Command Handling — Active Duty
    client.on('interactionCreate', async (interaction) => {
        if (!interaction.isChatInputCommand()) return;

        const command = client.commands.get(interaction.commandName);
        if (!command) return;

        try {
            await command.execute(interaction);
        } catch (error) {
            console.error(error);
            await interaction.reply({content: '⚖️ The scales have tipped! An error occurred.', ephemeral: true});

        }
    });

    //Return to Olympus
    return client;
}

module.exports = { initThemis };