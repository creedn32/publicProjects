let path = require('path');
pathArrayThisFile = path.resolve(__dirname, __filename).split(path.sep);

let googleSheetsLibrary = require('../creedLibrary/googleSheetsLibrary/googleSheetsLibrary');
let c = console.log.bind(console);

const getSheetAndUpdateSheet = async ([googleSheetsUsername, googleSpreadsheetTitle, googleSheetTitle]) => {

    test1SheetLevelObj = await googleSheetsLibrary.getSheetLevelObj(pathArrayThisFile, googleSheetsUsername, googleSpreadsheetTitle, googleSheetTitle);
    test2SheetLevelObj = await googleSheetsLibrary.getSheetLevelObj(pathArrayThisFile, googleSheetsUsername, googleSpreadsheetTitle, googleSheetTitle.slice(0, -1) + '2');

    arrayOfValues = await test1SheetLevelObj.getArrayOfValues();

    const expandedArrayOfValues = arrayOfValues.reduce(function(runningArray, currentElement) {

        // c('before');
        // c(r);
        // c(currentElement);
        runningArray.push(currentElement, ['a']);
        // runningArray.push(currentElement + 1, currentElement + 2);
        // c('after');
        // c(r)
        return runningArray;

    }, []);

    c(expandedArrayOfValues)

    test2SheetLevelObj.updateSheet(expandedArrayOfValues);

}

module.exports = getSheetAndUpdateSheet;