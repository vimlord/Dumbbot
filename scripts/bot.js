
const path = require('path')

function genText(x, fn) {
    var spawn = require("child_process").spawn;
    let proc = spawn('python3', ['model/model.py', '-m', 'model.h5', '-i', x])

    console.log('Generating text from ' + x)
    
    proc.stdout.on('data', (buf) => {
        fn(new String(buf));
    });
}

function initSocket(app, io) {

    console.log('Setting up socket functionality for bot');
    
    io.on('connection', function (socket) {
        console.log('A new user has connected');

        socket.on('input', function (data) {
            // Get user input
            x = data.input;

            console.log('user: ' + x);
            
            // Generate the text
            genText(x, (y) => {
                console.log('dumbbot: ' + y);
                socket.emit('output', {
                    output: y
                });
            });
        });

        socket.emit('output', {output: 'Hello! Type in a message to start chatting!'});

    });

}


module.exports = {
    genText,
    initSocket
}

