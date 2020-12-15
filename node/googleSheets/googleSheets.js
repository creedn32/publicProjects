let path = require('path');
pathArrayThisFile = path.resolve(__dirname, __filename).split(path.sep);

// let mainLibrary = require('../creedLibrary/mainLibrary');
let googleSheetsLibrary = require('../creedLibrary/googleSheetsLibrary/googleSheetsLibrary');
let c = console.log.bind(console);

const mainFunction = ([googleSheetTitle, googleSheetsUsername]) => { 

    // c(googleSheetsLibrary.getSpreadsheetLevelObj());

    googleSheetsLevelObj = googleSheetsLibrary.getGoogleSheetsLevelObj(pathArrayThisFile, googleSheetsUsername);

    // setTimeout(() => {c(googleSheetsLevelObj);}, 10000);

    // function listMajors(auth) {

    //     const sheets = google.sheets({version: 'v4', auth});

    //     sheets.spreadsheets.values.get({

    //         spreadsheetId: '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms',
    //         range: 'Class Data!A2:E',

    //     }, (err, res) => {

    //         if (err) return c('The API returned an error: ' + err);
            
    //         const rows = res.data.values;
            
    //         if (rows.length) {
                
    //             c('Name, Major:');
    //             // Print columns A and E, which correspond to indices 0 and 4.
    //             rows.map((row) => {
    //                 c(`${row[0]}, ${row[4]}`);
    //             });
            
    //         } else {

    //             c('No data found.');
            
    //         }
    //     });
    // }
};

module.exports = mainFunction;