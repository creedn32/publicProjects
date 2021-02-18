const c = console.log.bind(console);
const path = require('path');
pathArrayThisFile = path.resolve(__dirname, __filename).split(path.sep);
// c(pathArrayThisFile);

const googleSheetsLibrary = require('../creedLibrary/googleSheetsLibrary/googleSheetsLibrary');

const getSheetAndUpdateSheet = async ([googleAccountUsername, googleSpreadsheetTitle, receivingBankFromPayPalData, accountantName, defaultTransferFromCheckbook, defaultTransferToCheckbook]) => {

    const bankSheetTitle = 'bank';
    const expandedBankSheetTitle = 'expandedBank';
    const transfersToPostSheetTitle = 'transfersToPost';
    const transactionsToPostSheetTitle = 'transactionsToPost';
    const glForFees = '01-000-5321';

    const bankSheetLevelObj = await googleSheetsLibrary.getSheetLevelObj(pathArrayThisFile, googleAccountUsername, googleSpreadsheetTitle, bankSheetTitle);
    const bankNewSheetLevelObj = await googleSheetsLibrary.getSheetLevelObj(pathArrayThisFile, googleAccountUsername, googleSpreadsheetTitle, expandedBankSheetTitle);
    const transfersToPostSheetLevelObj = await googleSheetsLibrary.getSheetLevelObj(pathArrayThisFile, googleAccountUsername, googleSpreadsheetTitle, transfersToPostSheetTitle);
    const transactionsToPostSheetLevelObj = await googleSheetsLibrary.getSheetLevelObj(pathArrayThisFile, googleAccountUsername, googleSpreadsheetTitle, transactionsToPostSheetTitle);

    const bankArray = await bankSheetLevelObj.getArrayOfValues();

    const expandedBankArray = bankArray.reduce(function(accumulator, currentElement, currentIndex) {

        arrayBeforeAmount = currentElement.slice(0, 5);
        arrayAfterAmount = currentElement.slice(9, currentElement.length)
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

                    accumulator.push(arrayBeforeAmount.concat(transactionType, currentAmount, arrayAfterAmount));

                }
            });

        } else {

            accumulator.push(arrayBeforeAmount.concat('Type', 'Amount', ...arrayAfterAmount));

        }

        return accumulator;

    }, []);

    transfersToPostArray = [['Transfer Date', 'Description', 'Transfer From Checkbook ID', 'Amount', 'Transfer To Checkbook ID', 'Status', 'Person']];
    feesToPostArray = [['Option', 'Type', 'Transaction Date', 'Checkbook ID', 'Paid To or Rcvd From', 'Description', 'Amount', 'Account', 'Amount2', 'Status', 'Person']];


    expandedBankArray.forEach((row) => {

        if (row[10] === receivingBankFromPayPalData) {

            [transferFromCheckbook, transferToCheckbook] = [defaultTransferFromCheckbook, defaultTransferToCheckbook];

            if (row[6] > 0) {

                [transferFromCheckbook, transferToCheckbook] = [defaultTransferToCheckbook, defaultTransferFromCheckbook];

            }

            description = transferFromCheckbook + ' to ' + transferToCheckbook;

            transfersToPostArray.push([row[0], description, transferFromCheckbook, Math.abs(row[6]), transferToCheckbook, '', accountantName])

        }

        if (row[5] === 'Fee') {

            adjustmentType = 'Decrease Adjustment';

            if (row[6] > 0) adjustmentType = 'Increase Adjustment';

            feesToPostArray.push(['Enter Transaction', adjustmentType, row[0], defaultTransferFromCheckbook, defaultTransferFromCheckbook, 'Fee', Math.abs(row[6]), glForFees, Math.abs(row[6]), '', accountantName]);

        }

    });

    bankNewSheetLevelObj.updateSheet(expandedBankArray);
    transfersToPostSheetLevelObj.updateSheet(transfersToPostArray);
    transactionsToPostSheetLevelObj.updateSheet(feesToPostArray);

    // c(expandedBankArray);

}

module.exports = getSheetAndUpdateSheet;

if (require.main === module) {

    getSheetAndUpdateSheet(process.argv.slice(2));
    console.log(path.basename(__filename) + ' is not being required as a module, it is being called directly...');

} else {

    console.log(__filename + ' is being required as a module...');
    
}