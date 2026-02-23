// themis.js (Module)
const db = require('./db');

// We export a function instead of starting a bot
async function applyJustice(message) {
    const checkSql = 'SELECT "watchlistStatus" FROM charon."verficationLogs" WHERE "discord_id" = $1 AND "watchlistStatus" = TRUE LIMIT 1';
    const res = await db.query(checkSql, [message.author.id]);

    if (res.rows.length > 0) {
        console.log(`🚩 THEMIS ALERT: ${message.author.tag} is active.`);
    }
}

module.exports = { applyJustice };