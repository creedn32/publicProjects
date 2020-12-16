let path = require('path');
pathArrayThisFile = path.resolve(__dirname, __filename).split(path.sep);

// let mainLibrary = require('../creedLibrary/mainLibrary');
let googleSheetsLibrary = require('../creedLibrary/googleSheetsLibrary/googleSheetsLibrary');
let c = console.log.bind(console);
const {google} = require('googleapis');

const mainFunction = async ([googleSheetsUsername, googleSpreadsheetTitle, googleSheetTitle]) => { 

    // c(googleSheetsLibrary.getSpreadsheetLevelObj());

    const googleAccountLevelObj = await googleSheetsLibrary.getGoogleAccountLevelObj(pathArrayThisFile, googleSheetsUsername, googleSpreadsheetTitle);
    
    const googleSpreadsheetID = await googleSheetsLibrary.getGoogleSpreadsheetID(googleAccountLevelObj, googleSpreadsheetTitle);

    const googleSheetsLevelObj = google.sheets({version: 'v4', auth: googleAccountLevelObj});


    try {
        
        const googleSheetValues = await googleSheetsLevelObj.spreadsheets.values.get({

            spreadsheetId: googleSpreadsheetID,
            range: googleSheetTitle,

        });

        const rows = googleSheetValues.data.values;

        if (rows.length) {
                
            c(rows);
        
        } else {

            c('No data found.');
        
        }

    } catch (error) {

        c('The API returned an error: ' + error);

    }


};


module.exports = mainFunction;