// 1. Imports
const { Client, IntentsBitField, ActivityType, Collection } = require('discord.js'); // Added Collection here
const fs = require('node:fs'); 
const path = require('node:path'); 
const db = require('./db'); //Connecting to the database
const { setDefaultAutoSelectFamily } = require('node:net');

//2. Warapping everything in an initialization
function initCharon() {
    const clent = new Client({
        intents: [
            IntentsBitField.Flag.Guilds,
        IntentsBitField.Flags.GuildMessages,
        IntentsBitField.Flags.GuildMessages
        ]
    });
    //The shelf of commands that only Charon can use
    client.commands = new Collection();

    //This makes it so charon can only add commands to its shelf that have been tagged for it
    const commandsPath = path.join(__dirname, 'commands', 'charonTheFerryman');

    //A check to make sure the folder exists so charon doesn't crash
    if(fs.existsSync(commandsPath)) {
        const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js')); //Makes sure there is a filter so it only takes javascript files

        for(const file of commandFiles){
            const filePath = path.join(commandsPath, file);
            const command = require(filePath);

            if('data' in command && 'execute' in command) {
                client.commands.set(command.data.name, command);
            }
        }
    }

    //Events
    client.once('ready', () => {
        console.log(`Charon Hub: Online as ${client.user.tag}`); //Make this cooler

        const statuses = ["Verifying soulds", "Guiding Spirits", "Ferrying users"];
        const updateStatus = () => {
            const randomStatus = statuses[Math.floor(Math.random() * statuses.length)];
            client.user.setActivity(randomStatus, {type: ActivityType.Watching});
        };
        updateStatus();
        setInterval(updateStatus, 600000);
    });

    client.on('interactionCreate', async (interaction) => {
        if(!interaction.isChatInputCommand()) return;

        try {
            await command.execute(interaction);
        } catch (error) {
            console.error(error);
            const msg = {content: '⚠️ The ferry stalled... an error occurred!', ephemeral: true};
            interaction.replied || interaction.deferred ? await interaction.followUp(msg) : await interaction.reply(msg);
        }
    });

    //Return client back to Olympus
    return client;
    
}

module.exports = {initCharon};