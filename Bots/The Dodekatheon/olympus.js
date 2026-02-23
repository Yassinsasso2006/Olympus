const { Client, IntentsBitField, Collection } = require('discord.js');
const db = require('./db');
require('dotenv').config();

// --- 1. THE PRESENCES (The Gods) ---

// Charon: The Ferryman (Verification)
const charon = new Client({ intents: [IntentsBitField.Flags.Guilds, IntentsBitField.Flags.GuildMembers] });

// Themis: The Judge (Surveillance)
const themis = new Client({ 
    intents: [
        IntentsBitField.Flags.Guilds, 
        IntentsBitField.Flags.GuildMessages, 
        IntentsBitField.Flags.MessageContent 
    ] 
});

// --- 2. SHARED LOGIC (The Logging Engine) ---

// This function handles Argus's data collection and Themis's alerts
async function processMessage(message) {
    if (message.author.bot || !message.guild) return;

    try {
        // A. ARGUS: Log activity to the database for the Python script
        const argusSql = `
            INSERT INTO argus."watchlist" ("discordID", "numOfMessagesSent", "lastMessageAt")
            VALUES ($1, 1, NOW())
            ON CONFLICT ("discordID") 
            DO UPDATE SET "numOfMessagesSent" = argus."watchlist"."numOfMessagesSent" + 1, "lastMessageAt" = NOW();
        `;
        await db.query(argusSql, [message.author.id]);

        // B. THEMIS: Check for flagged users
        const themisSql = `
            SELECT "watchlistStatus" FROM charon."verficationLogs" 
            WHERE "discord_id" = $1 AND "watchlistStatus" = TRUE LIMIT 1
        `;
        const res = await db.query(themisSql, [message.author.id]);

        if (res.rows.length > 0) {
            console.log(`🚩 THEMIS ALERT: Watchlisted user ${message.author.tag} is active.`);
        }
    } catch (err) {
        console.error("Olympus Engine Error:", err);
    }
}

// --- 3. EVENT ASSIGNMENT ---

// Only Themis needs to listen to messages to track them
themis.on('messageCreate', (message) => processMessage(message));

charon.once('ready', () => console.log("🛶 Charon has arrived at the Styx."));
themis.once('ready', () => console.log("⚖️ Themis has taken her seat."));

// --- 4. THE LOGIN ---

charon.login(process.env.TOKEN_CHARON);
themis.login(process.env.TOKEN_THEMIS);