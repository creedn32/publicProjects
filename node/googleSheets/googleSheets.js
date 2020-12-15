// var path = require('path');
// var fs = require('fs');
// thisFilePathArray = path.resolve(__dirname, __filename).split(path.sep);
let l = require('../..node/creedLibrary/creedLibrary')
var c = console.log.bind(console);

const mainFunction = ([googleSheetTitle, googleSheetUsername]) => { 

    c(googleSheetTitle);
    c(googleSheetUsername);
    // l.c(1);

};

module.exports = mainFunctio