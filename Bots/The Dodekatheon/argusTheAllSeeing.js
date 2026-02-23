const { Client, IntentsBitField } = require('discord.js');
const db = require('./db');

function initArgus() {
    const client = new Client({
        intents: [
            IntentsBitField.Flags.Guilds,
            IntentsBitField.Flags.GuildMessages,
            IntentsBitField.Flags.MessageContent
        ]
    });

    client.on('messageCreate', async (message) => {
        if (message.author.bot || !message.guild) return;

        try {
            const sql = `
                INSERT INTO argus."watchlist" ("discordID", "numOfMessagesSent", "lastMessageAt")
                VALUES ($1, 1, NOW())
                ON CONFLICT ("discordID") 
                DO UPDATE SET 
                    "numOfMessagesSent" = argus."watchlist"."numOfMessagesSent" + 1,
                    "lastMessageAt" = NOW();
            `;
            await db.query(sql, [message.author.id]);
        } catch (err) {
            console.error("👁️ Argus Data Entry Error:", err);
        }
    });

    client.once('ready', () => console.log("👁️ Argus Hub: Active"));

    return client;
}

module.exports = { initArgus };