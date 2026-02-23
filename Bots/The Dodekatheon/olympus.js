const { Client, IntentsBitField } = require('discord.js');
const { applyJustice } = require('./themisTheEmbodimentOfJustice'); // Import Themis
const { trackActivity } = require('./argusTheAllSeeing'); // Import Argus
require('dotenv').config();

// --- 1. DEFINE THE PRESENCES ---

// Charon (The Ferryman)
const charon = new Client({
    intents: [IntentsBitField.Flags.Guilds, IntentsBitField.Flags.GuildMembers]
});

// Themis (The Judge)
const themis = new Client({
    intents: [
        IntentsBitField.Flags.Guilds,
        IntentsBitField.Flags.GuildMessages,
        IntentsBitField.Flags.MessageContent
    ]
});

// Argus (JS Component): Handles Data Entry
const argus = new Client({
    intents: [IntentsBitField.Flags.Guilds, IntentsBitField.Flags.GuildMessages, IntentsBitField.Flags.MessageContent]
});

// --- 2. ASSIGN THE WORK ---

// --- 2. INDIVIDUAL DUTIES ---

// ARGUS: Listens to chat ONLY to track activity
argus.on('messageCreate', async (message) => {
    if (message.author.bot || !message.guild) return;
    await trackActivity(message); 
});

// THEMIS: Listens to chat ONLY to check the watchlist
themis.on('messageCreate', async (message) => {
    if (message.author.bot || !message.guild) return;
    await applyJustice(message);
});

charon.once('ready', () => console.log("🛶 Charon has arrived at the Styx."));
themis.once('ready', () => console.log("⚖️ Themis has taken her seat."));
argus.once('ready', () => console.log("👁️ Argus: Online (Watching currents)"));

// --- 4. THE LOGIN ---

charon.login(process.env.TOKEN_CHARON);
themis.login(process.env.TOKEN_THEMIS);
argus.login(process.env.TOKEN_ARGUS);