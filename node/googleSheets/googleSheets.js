let path = require('path');
pathArrayThisFile = path.resolve(__dirname, __filename).split(path.sep);

let googleSheetsLibrary = require('../creedLibrary/googleSheetsLibrary/googleSheetsLibrary');
let c = console.log.bind(console);
const {google} = require('googleapis');

const getSheetAndUpdateSheet = async ([googleSheetsUsername, googleSpreadsheetTitle, googleSheetTitle]) => {

    let sheetLevelObj = {

        googleAccountLevelObj: await googleSheetsLibrary.getGoogleAccountLevelObj(pathArrayThisFile, googleSheetsUsername, googleSpreadsheetTitle),
        googleSheetsValuesLevelObj: googleSheetsLibrary.getGoogleSheetsValuesLevelObj(this.googleAccountLevelObj),
        // spreadsheetLevelObj: await googleSheetsLibrary.getSpreadsheetLevelObj(this.googleAccountLevelObj, googleSpreadsheetTitle),
        spreadsheetID: 1,
        // spreadsheetID: googleSheetsLibrary.getGoogleSpreadsheetID(this.googleAccountLevelObj, googleSpreadsheetTitle),
        getArrayOfValues: function() {

            try {

                const request = {

                        spreadsheetId: this.spreadsheetID,
                        range: googleSheetTitle,

                };

                // const googleSheetValues = await googleSheetsLevelObj.spreadsheets.values.get();

                // let rows = googleSheetValues.data.values;

                let rows = [['a', 'b'], ['c']];

                if (rows.length) {

                    const maxRowLength = Math.max(...rows.map(row => row.length));
                    const rowsWithFill = rows.map(row => row.concat(Array(maxRowLength - row.length).fill('')));
                    return rowsWithFill;

                }

            } catch (error) {

                c('The API returned an error: ' + error);

            }

        },
        updateSheet: function(arrayToUpload) {

            const request = {

                spreadsheetId: this.spreadsheetID,
                // spreadsheetId: await googleSheetsLibrary.getGoogleSpreadsheetID(googleAccountLevelObj, googleSpreadsheetTitle),

                resource: {

                    valueInputOption: 'RAW',

                    data: {

                        range: googleSheetTitle,
                        values: arrayToUpload
                    },

                },

                auth: this.googleAccountLevelObj,

            };

            try {

                // const response = await googleSheetsLevelObj.spreadsheets.values.batchUpdate(request);

                response = null;
                c(JSON.stringify(response, null, 2));

            } catch (err) {

                c(err);

            }

        }

    };

    c(sheetLevelObj.getArrayOfValues());

    await sheetLevelObj.updateSheet(
        [
            ['test1'],
            ['data1'],
            ['data1']
        ]
    );
}


module.exports = getSheetAndUpdateSheet;