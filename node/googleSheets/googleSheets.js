// var path = require('path');
// var fs = require('fs');
// thisFilePathArray = path.resolve(__dirname, __filename).split(path.sep);
var c = console.log.bind(console);

const mainFunction = ([googleSheetTitle, googleSheetUsername]) => { 

    c(googleSheetTitle);
    c(googleSheetUsername);


};

module.exports = mainFunction;