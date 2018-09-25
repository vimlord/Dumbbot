const path = require("path");

const fs = require("fs");

function sendPage(res, name) {
    // Get the url
    let url = path.resolve(name);
    console.log(name + " is at '" + url + "'");
    
    // Send the file
    res.sendFile(url);
}


module.exports = app => {
    app.get('/', function (req, res) {
        // The user wants the homepage
        console.log("Homepage is requested");
        
        sendPage(res, 'index.html');
    });

    app.get('/public/site.css', function(req, res) {
        console.log("Stylesheet is requested");

        sendPage(res, 'site.css');
    });
    
    /*
    // Dafault behavior: 404
    app.get("/*", function (req, res) {
        fs.readFile(path.resolve("error.html"), 'utf-8',
        function (err, file) {
            let mssg = handlebars.compile(file)({
                title: "404 (file not found)",
                desc:  "The page you requested could not be loaded"
            });
            res.status(404).send(mssg);
        });
    });*/

}

