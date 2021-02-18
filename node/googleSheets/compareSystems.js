const c = console.log.bind(console);
const path = require('path');
pathArrayThisFile = path.resolve(__dirname, __filename).split(path.sep);
// c(pathArrayThisFile);

const googleSheetsLibrary = require('../creedLibrary/googleSheetsLibrary/googleSheetsLibrary');

const getSheetAndUpdateSheet = async ([googleAccountUsername, googleSpreadsheetTitle]) => {

    const dataSheetTitle = 'Data';

    const dataSheetLevelObj = await googleSheetsLibrary.getSheetLevelObj(pathArrayThisFile, googleAccountUsername, googleSpreadsheetTitle, dataSheetTitle);

    const dataArray = await dataSheetLevelObj.getArrayOfValues();

    dataArray.forEach((row) => {

        c(1);

    });

}

module.exports = getSheetAndUpdateSheet;

if (require.main === module) {

    getSheetAndUpdateSheet(process.argv.slice(2));
    console.log(path.basename(__filename) + ' is not being required as a module, it is being called directly...');

} else {

    console.log(__filename + ' is being required as a module...');
    
}