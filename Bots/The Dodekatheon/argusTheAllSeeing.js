const db = require('./db');

// We "export" this function so Olympus can call it
async function trackActivity(message) {
    const sql = `
        INSERT INTO argus."watchlist" ("discordID", "numOfMessagesSent", "lastMessageAt")
        VALUES ($1, 1, NOW())
        ON CONFLICT ("discordID") 
        DO UPDATE SET 
            "numOfMessagesSent" = argus."watchlist"."numOfMessagesSent" + 1,
            "lastMessageAt" = NOW();
    `;
    await db.query(sql, [message.author.id]);
}

module.exports = { trackActivity };