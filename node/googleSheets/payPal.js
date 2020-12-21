let path = require('path');
pathArrayThisFile = path.resolve(__dirname, __filename).split(path.sep);

let googleSheetsLibrary = require('../creedLibrary/googleSheetsLibrary/googleSheetsLibrary');
let c = console.log.bind(console);

const getSheetAndUpdateSheet = async ([googleSheetsUsername, googleSpreadsheetTitle, firstGoogleSheetTitle, secondGoogleSheetTitle]) => {

    test1SheetLevelObj = await googleSheetsLibrary.getSheetLevelObj(pathArrayThisFile, googleSheetsUsername, googleSpreadsheetTitle, firstGoogleSheetTitle);
    test2SheetLevelObj = await googleSheetsLibrary.getSheetLevelObj(pathArrayThisFile, googleSheetsUsername, googleSpreadsheetTitle, secondGoogleSheetTitle);

    arrayOfValues = await test1SheetLevelObj.getArrayOfValues();

    const expandedArrayOfValues = arrayOfValues.reduce(function(accumulator, currentElement, currentIndex) {

        firstPart = currentElement.slice(0, 5);
        secondPart = currentElement.slice(9, currentElement.length)

        if (currentIndex > 0) {

            accumulator.push(firstPart.concat(currentElement[5], ...secondPart), firstPart.concat(currentElement[6], ...secondPart), firstPart.concat(currentElement[7], ...secondPart));

        } else {

            accumulator.push(firstPart.concat('Amount', ...secondPart));

        }

        return accumulator;


    }, []);

    // c(expandedArrayOfValues)

    test2SheetLevelObj.updateSheet(expandedArrayOfValues);

}

module.exports = getSheetAndUpdateSheet;