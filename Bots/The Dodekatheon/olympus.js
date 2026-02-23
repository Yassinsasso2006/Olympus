const { initCharon } = require('./charonTheFerryman');
const { initThemis } = require('./themisTheEmbodimentOfJustice');
const { initArgus } = require('./argusTheAllSeeing');
require('dotenv').config();

// Initialize the "Hubs"
const charon = initCharon();
const themis = initThemis();
const argus = initArgus();

// Final Login - The Spark of Life
charon.login(process.env.TOKEN_CHARON);
themis.login(process.env.TOKEN_THEMIS);
argus.login(process.env.TOKEN_ARGUS);