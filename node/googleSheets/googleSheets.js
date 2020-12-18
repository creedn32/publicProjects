let path = require('path');
pathArrayThisFile = path.resolve(__dirname, __filename).split(path.sep);

// let mainLibrary = require('../creedLibrary/mainLibrary');
let googleSheetsLibrary = require('../creedLibrary/googleSheetsLibrary/googleSheetsLibrary');
let c = console.log.bind(console);
const {google} = require('googleapis');
const { get } = require('http');

const mainFunction = async ([googleSheetsUsername, googleSpreadsheetTitle, googleSheetTitle]) => {

    // c(googleSheetsLibrary.getSpreadsheetLevelObj());

    const googleAccountLevelObj = await googleSheetsLibrary.getGoogleAccountLevelObj(pathArrayThisFile, googleSheetsUsername, googleSpreadsheetTitle);
    // const googleSheetsLevelObj = google.sheets({version: 'v4', auth: googleAccountLevelObj});

    c(await googleSheetsLibrary.getArrayOfValues(googleAccountLevelObj, googleSpreadsheetTitle, googleSheetTitle));

};


module.exports = mainFunction;