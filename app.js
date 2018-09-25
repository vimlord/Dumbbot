// For usage of express
const express = require("express");
const app = express();

// For enabling socket.io
const server = require('http').Server(app);
const io = require('socket.io')(server);

const configRoutes = require("./routes");

// Configure express routes
configRoutes(app);

// Start listening
server.listen(80);

// Initialize the bot connection
require('./scripts/bot').initSocket(app, io);

/*
app.listen(8080, () => {
    console.log("Server is now fully armed and operational.");
});
*/

