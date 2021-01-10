let path = require('path');
pathArrayThisFile = path.resolve(__dirname, __filename).split(path.sep);

let googleSheetsLibrary = require('../creedLibrary/googleSheetsLibrary/googleSheetsLibrary');
let c = console.log.bind(console);

const getSheetAndUpdateSheet = async ([googleSheetsUsername, googleSpreadsheetTitle, bankSheetTitle, bankNewSheetTitle, transfersToPostSheetTitle, transactionsToPostSheetTitle, bankName, userName, firstCheckbook, secondCheckbook, glForFees]) => {

    bankSheetLevelObj = await googleSheetsLibrary.getSheetLevelObj(pathArrayThisFile, googleSheetsUsername, googleSpreadsheetTitle, bankSheetTitle);
    bankNewSheetLevelObj = await googleSheetsLibrary.getSheetLevelObj(pathArrayThisFile, googleSheetsUsername, googleSpreadsheetTitle, bankNewSheetTitle);
    transfersToPostSheetLevelObj = await googleSheetsLibrary.getSheetLevelObj(pathArrayThisFile, googleSheetsUsername, googleSpreadsheetTitle, transfersToPostSheetTitle);
    transactionsToPostSheetLevelObj = await googleSheetsLibrary.getSheetLevelObj(pathArrayThisFile, googleSheetsUsername, googleSpreadsheetTitle, transactionsToPostSheetTitle);

    arrayOfValues = await bankSheetLevelObj.getArrayOfValues();

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

    transfersToPostArray = [['Transfer Date', 'Description', 'Transfer From Checkbook ID', 'Amount', 'Transfer To Checkbook ID', 'Status', 'Person']];
    feesToPostArray = [['Option', 'Type', 'Transaction Date', 'Checkbook ID', 'Paid To or Rcvd From', 'Description', 'Amount', 'Account', 'Amount2', 'Status', 'Person']];


    expandedArrayOfValues.forEach((row) => {

        if (row[10] === bankName) {

            [transferFromCheckbook, transferToCheckbook] = [firstCheckbook, secondCheckbook];

            if (row[6] > 0) {

                [transferFromCheckbook, transferToCheckbook] = [secondCheckbook, firstCheckbook];
            
            }

            description = transferFromCheckbook + ' to ' + transferToCheckbook;

            transfersToPostArray.push([row[0], description, transferFromCheckbook, Math.abs(row[6]), transferToCheckbook, '', userName])

        }
        
        if (row[5] === 'Fee') {

            feesToPostArray.push(['Enter Transaction', 'Decrease Adjustment', row[0], firstCheckbook, firstCheckbook, 'Fee', Math.abs(row[6]), glForFees, Math.abs(row[6]), '', userName]);

        }

    });

    bankNewSheetLevelObj.updateSheet(expandedArrayOfValues);
    transfersToPostSheetLevelObj.updateSheet(transfersToPostArray);
    transactionsToPostSheetLevelObj.updateSheet(feesToPostArray);

    // c(expandedArrayOfValues);

}

module.exports = getSheetAndUpdateSheet;