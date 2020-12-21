let path = require('path');
pathArrayThisFile = path.resolve(__dirname, __filename).split(path.sep);

let googleSheetsLibrary = require('../creedLibrary/googleSheetsLibrary/googleSheetsLibrary');
let c = console.log.bind(console);

const getSheetAndUpdateSheet = async ([googleSheetsUsername, googleSpreadsheetTitle, googleSheetTitle]) => {

    sheetLevelObj = await googleSheetsLibrary.getSheetLevelObj(pathArrayThisFile, googleSheetsUsername, googleSpreadsheetTitle, googleSheetTitle);

    c(await sheetLevelObj.getArrayOfValues());

    // sheetLevelObj.updateSheet(
    //     [
    //         ['test5'],
    //         ['data3'],
    //         ['data4']
    //     ]
    // );
}

module.exports = getSheetAndUpdateSheet;