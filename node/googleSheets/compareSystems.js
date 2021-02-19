const c = console.log.bind(console);
const path = require('path');
pathArrayThisFile = path.resolve(__dirname, __filename).split(path.sep);
// c(pathArrayThisFile);

const googleSheetsLibrary = require('../creedLibrary/googleSheetsLibrary/googleSheetsLibrary');

const getSheetAndUpdateSheet = async ([googleAccountUsername, googleSpreadsheetTitle, firstAccount, firstAccountReport, secondAccount, secondAccountReport, thirdAccount, thirdAccountReport, accountingSystemStandardReport]) => {

    const dataSheetTitle = 'Data';
    const comparisonSheetTitle = 'Comparison';

    const dataSheetLevelObj = await googleSheetsLibrary.getSheetLevelObj(pathArrayThisFile, googleAccountUsername, googleSpreadsheetTitle, dataSheetTitle);
    const comparisonSheetLevelObj = await googleSheetsLibrary.getSheetLevelObj(pathArrayThisFile, googleAccountUsername, googleSpreadsheetTitle, comparisonSheetTitle);

    const dataArray = await dataSheetLevelObj.getArrayOfValues();
    const comparisonObj = {};
    const emptyDataPointObj = {

        [firstAccount]: {

            [accountingSystemStandardReport]: {

                'Amount': 0,
                'Prior EOY': 0,
                'Adjusted Amount': 0,
                'Date Of Data Pull': '',
                'Person': '',
                'File Name': '',
                'Notes': '',

            },

            [firstAccountReport]: {

                'Adjusted Amount': 0,
                'Date Of Data Pull': '',

            }

        },
        [secondAccount]: {

            [secondAccountReport]: {

                'Adjusted Amount': 0,
                'Date Of Data Pull': '',

            },

            [accountingSystemStandardReport]: {

                'Adjusted Amount': 0,
                'Date Of Data Pull': '',

            },
        },
        [thirdAccount]: {

            [thirdAccountReport]: {

                'Adjusted Amount': 0,
                'Date Of Data Pull': '',

            },

            [accountingSystemStandardReport]: {

                'Adjusted Amount': 0,
                'Date Of Data Pull': '',

            }

        }

    };

    dataArray.forEach((row) => {

        const dateFromRow = row[0];
        const adjustedAmountFromRow = row[7];
        const dateOfDataPullFromRow = row[1];
        const accountFromRow = row[2];
        const reportFromRow = row[4];

        if (dateFromRow != 'Date') {

            comparisonObj[dateFromRow] = JSON.parse(JSON.stringify(emptyDataPointObj));

        }

        for (const account of [firstAccount]) {
            
            for (const report of [accountingSystemStandardReport, firstAccountReport]) {

                if (accountFromRow === account && reportFromRow === report) {
    
                    comparisonObj[dateFromRow][account][report]['Adjusted Amount'] = adjustedAmountFromRow;
                    comparisonObj[dateFromRow][account][report]['Date Of Data Pull'] = dateOfDataPullFromRow;
        
                }

            }

        }
        

    });

    // c(JSON.stringify(comparisonObj));

    comparisonArray = [

        [

            '',
            firstAccount,
            '',
            '',
            '',
            secondAccount,
            '',
            '',
            '',
            thirdAccount,
            '',
            '',
            ''

        ],
        [

            'Date',
            accountingSystemStandardReport + ' Adjusted Amount',
            accountingSystemStandardReport + ' Date Of Data Pull',
            firstAccountReport + ' Adjusted Amount',
            firstAccountReport + ' Date Of Data Pull',
            secondAccountReport + ' Adjusted Amount',
            secondAccountReport + ' Date Of Data Pull',
            accountingSystemStandardReport + ' Adjusted Amount',
            accountingSystemStandardReport + ' Date Of Data Pull',
            thirdAccountReport + ' Adjusted Amount',
            thirdAccountReport + ' Date Of Data Pull',
            accountingSystemStandardReport + ' Adjusted Amount',
            accountingSystemStandardReport + ' Date Of Data Pull',

        ]

    ];

    for (const balanceDate in comparisonObj) {

        comparisonArray.push(

            [

                balanceDate,

                comparisonObj[balanceDate][firstAccount][accountingSystemStandardReport]['Adjusted Amount'],
                comparisonObj[balanceDate][firstAccount][accountingSystemStandardReport]['Date Of Data Pull'],
                comparisonObj[balanceDate][firstAccount][firstAccountReport]['Adjusted Amount'],
                comparisonObj[balanceDate][firstAccount][firstAccountReport]['Date Of Data Pull'],

                comparisonObj[balanceDate][secondAccount][secondAccountReport]['Adjusted Amount'],
                comparisonObj[balanceDate][secondAccount][secondAccountReport]['Date Of Data Pull'],
                comparisonObj[balanceDate][secondAccount][accountingSystemStandardReport]['Adjusted Amount'],
                comparisonObj[balanceDate][secondAccount][accountingSystemStandardReport]['Date Of Data Pull'],

                comparisonObj[balanceDate][thirdAccount][thirdAccountReport]['Adjusted Amount'],
                comparisonObj[balanceDate][thirdAccount][thirdAccountReport]['Date Of Data Pull'],
                comparisonObj[balanceDate][thirdAccount][accountingSystemStandardReport]['Adjusted Amount'],
                comparisonObj[balanceDate][thirdAccount][accountingSystemStandardReport]['Date Of Data Pull']

            ]

        );

    }

    // c(comparisonArray);
    comparisonSheetLevelObj.updateSheet(comparisonArray);

}

module.exports = getSheetAndUpdateSheet;

if (require.main === module) {

    getSheetAndUpdateSheet(process.argv.slice(2));
    console.log(path.basename(__filename) + ' is not being required as a module, it is being called directly...');

} else {

    console.log(__filename + ' is being required as a module...');
    
}