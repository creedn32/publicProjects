const importedExpress = require('express')
const importedPath = require('path');
const importedStringifyObject = require('stringify-object')
// const importedUtil = require('util')
const expressApp = importedExpress()
const configFile = require('../aConfigFiles/config');
const portStr = configFile.portStr;


expressApp.get('/canary', (reqObj, resObj) => {
    resObj.send('The server is running...');

    printingOn = false;

    if (printingOn) {

        lengthOfStringToPrint = 100;

        console.log('Printed reqObj: ' + importedStringifyObject(reqObj, {
            indent: '  ',
            singleQuotes: false
        }).substr(0, lengthOfStringToPrint));
    
    
        console.log('Printed resObj: ' + importedStringifyObject(resObj, {
            indent: '  ',
            singleQuotes: false
        }).substr(0, lengthOfStringToPrint));
    }
        
})


pathToThisJavascriptFileDirectory = __dirname
expressApp.use('/', importedExpress.static(importedPath.join(pathToThisJavascriptFileDirectory, '../frontend')))


expressApp.listen(portStr, () => console.log(`Example app listening at http://localhost:${portStr}`))
