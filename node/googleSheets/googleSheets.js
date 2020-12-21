let path = require('path');
pathArrayThisFile = path.resolve(__dirname, __filename).split(path.sep);

// let mainLibrary = require('../creedLibrary/mainLibrary');
let googleSheetsLibrary = require('../creedLibrary/googleSheetsLibrary/googleSheetsLibrary');
let c = console.log.bind(console);
const {google} = require('googleapis');

const mainFunction = async ([googleSheetsUsername, googleSpreadsheetTitle, googleSheetTitle]) => {

    const googleAccountLevelObj = await googleSheetsLibrary.getGoogleAccountLevelObj(pathArrayThisFile, googleSheetsUsername, googleSpreadsheetTitle);
    const googleSheetsValuesLevelObj = googleSheetsLibrary.getGoogleSheetsValuesLevelObj(googleAccountLevelObj);
    const spreadsheetLevelObj = await googleSheetsLibrary.getSpreadsheetLevelObj(googleAccountLevelObj, googleSpreadsheetTitle);
    const sheetLevelObj = googleSheetsLibrary.getSheetLevelObj(googleSheetsValuesLevelObj);
    c(sheetLevelObj.getArrayOfValues());





    // // class GoogleSheetsSheetLevelObj {
        
    // //     constructor() {

    // //         this.googleSheetsLevelObj = 

    // //     }


    
    // let sheetLevelObj = new GoogleSheetsSheetLevelObj();

    // c(sheetLevelObj.propertyInfo);
    // c(sheetLevelObj.getArrayOfValues());


    // module.exports.getArrayOfValues = async (googleAccountLevelObj, googleSpreadsheetTitle, googleSheetTitle) => {

    //     const googleSpreadsheetID = await module.exports.getGoogleSpreadsheetID(googleAccountLevelObj, googleSpreadsheetTitle);
    //     const googleSheetsLevelObj = module.exports.getGoogleSheetsLevelObj(googleAccountLevelObj);

    
    // };





    // c(await googleSheetsLibrary.getArrayOfValues(googleAccountLevelObj, googleSpreadsheetTitle, googleSheetTitle));






    // const updateSheet = async () => {

    //     const googleSheetsLevelObj = google.sheets({version: 'v4', auth: googleAccountLevelObj});

    //     const request = {

    //         spreadsheetId: await googleSheetsLibrary.getGoogleSpreadsheetID(googleAccountLevelObj, googleSpreadsheetTitle),

    //         resource: {

    //             valueInputOption: 'RAW',

    //             data: {

    //                 range: googleSheetTitle,
    //                 values: [
    //                     ['test1'],
    //                     ['data1'],
    //                     ['data1']
    //                 ]
    //             },

    //         },

    //         auth: googleAccountLevelObj,
    //     };

    //     try {

    //         const response = await googleSheetsLevelObj.spreadsheets.values.batchUpdate(request);
    //         // c(JSON.stringify(response, null, 2));

    //     } catch (err) {

    //         c(err);

    //     }

    // }

    // await updateSheet();
    
}


module.exports = mainFunction;