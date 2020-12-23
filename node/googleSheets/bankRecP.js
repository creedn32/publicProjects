let path = require('path');
pathArrayThisFile = path.resolve(__dirname, __filename).split(path.sep);

let googleSheetsLibrary = require('../creedLibrary/googleSheetsLibrary/googleSheetsLibrary');
let c = console.log.bind(console);

const getSheetAndUpdateSheet = async ([googleSheetsUsername, googleSpreadsheetTitle, firstGoogleSheetTitle, secondGoogleSheetTitle, thirdGoogleSheetTitle, bankName, userName, firstCheckbook, secondCheckbook]) => {

    test1SheetLevelObj = await googleSheetsLibrary.getSheetLevelObj(pathArrayThisFile, googleSheetsUsername, googleSpreadsheetTitle, firstGoogleSheetTitle);
    test2SheetLevelObj = await googleSheetsLibrary.getSheetLevelObj(pathArrayThisFile, googleSheetsUsername, googleSpreadsheetTitle, secondGoogleSheetTitle);
    test3SheetLevelObj = await googleSheetsLibrary.getSheetLevelObj(pathArrayThisFile, googleSheetsUsername, googleSpreadsheetTitle, thirdGoogleSheetTitle);

    arrayOfValues = await test1SheetLevelObj.getArrayOfValues();

    const expandedArrayOfValues = arrayOfValues.reduce(function(accumulator, currentElement, currentIndex) {

        firstPart = currentElement.slice(0, 5);
        secondPart = currentElement.slice(9, currentElement.length)
        transactionTypes = ['Gross', 'Fee'];

        if (currentIndex > 0) {

            transactionTypes.forEach((transactionType, transactionTypeIndex) => {

                currentAmountStr = currentElement[transactionTypeIndex + 5].replace(',', '')

                if (currentAmountStr.includes('(')) {

                    currentAmount = -parseFloat(currentAmountStr.replaceAll(/\(|\)/g, ''))

                } else {

                    currentAmount = parseFloat(currentAmountStr);

                }

                if (currentAmount) {
                    
                    accumulator.push(firstPart.concat(transactionType, currentAmount, secondPart));

                }
            });

        } else {

            accumulator.push(firstPart.concat('Type', 'Amount', ...secondPart));

        }

        return accumulator;


    }, []);

    transactionsToPostArray = [['Transfer Date', 'Description', 'Transfer From Checkbook ID', 'Amount', 'Transfer To Checkbook ID', 'Status', 'Person']];

    expandedArrayOfValues.forEach((row) => {

        if (row[10] === bankName) {

            [transferFromCheckbook, transferToCheckbook] = [firstCheckbook, secondCheckbook];

            if (row[6] > 0) {

                [transferFromCheckbook, transferToCheckbook] = [secondCheckbook, firstCheckbook];
            
            }

            description = transferFromCheckbook + ' to ' + transferToCheckbook;

            transactionsToPostArray.push([row[0], description, transferFromCheckbook, Math.abs(row[6]), transferToCheckbook, '', userName])

        }

    });

    test2SheetLevelObj.updateSheet(expandedArrayOfValues);
    test3SheetLevelObj.updateSheet(transactionsToPostArray);

}

module.exports = getSheetAndUpdateSheet;