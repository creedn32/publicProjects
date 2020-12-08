from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(pathToThisPythonFile.parents[3]))
from herokuGorilla.backend.python.myPythonLibrary import myPyFunc
from herokuGorilla.backend.python.myPythonLibrary import myPyAutoGui
from herokuGorilla.backend.python.googleSheets.myGoogleSheetsLibrary import myGspreadFunc

from pprint import pprint as p


def mainFunction(arrayOfArguments):

    pathBelowRepos = pathToThisPythonFile
    spreadsheetLevelObj = myGspreadFunc.getSpreadsheetLevelObj(True, pathBelowRepos, googleAccountUsername=arrayOfArguments[1]).open(arrayOfArguments[2])
    
    arrayFilenameColIdx = 0
    arrayCompletedStatusColIdx = 1

    filesToReviewArray = spreadsheetLevelObj.worksheet(arrayOfArguments[3]).get_all_values()
    filesToReviewArrayFirstRow = filesToReviewArray.pop(0)

    filesCompletedArray = spreadsheetLevelObj.worksheet(arrayOfArguments[4]).get_all_values()
    filesCompletedArray = list(filter(lambda x: x[arrayCompletedStatusColIdx] != '', filesCompletedArray))

    matchedArray = []
    matchedArray.append(filesToReviewArrayFirstRow + [''] + filesCompletedArray[0])

    # p(filesCompletedWithCompletedStatusArray)

    def filenameComparisonFunction(firstArrayCurrentRow, filesCompletedArrayCurrentRow):

        if firstArrayCurrentRow[arrayFilenameColIdx] == filesCompletedArrayCurrentRow[arrayFilenameColIdx]:
            return True
        return False


    def rowForMatchedArray(filesToReviewArrayCurrentRow):

        rowToReturn = filesToReviewArrayCurrentRow
        
        rowIndicesThatMatch = myPyFunc.rowIndicesInSecondFromTestsOnFirst([filenameComparisonFunction], filesToReviewArrayCurrentRow, filesCompletedArray)

        if len(rowIndicesThatMatch) == 1:
            rowToReturn.extend([''] + filesCompletedArray.pop(rowIndicesThatMatch[0]))
        elif len(rowIndicesThatMatch) > 1:
            p('More than one row matches on the first pass')

        return rowToReturn

    myPyFunc.transferToArray(filesToReviewArray, matchedArray, rowForMatchedArray)


    clearAndResizeParameters = [
        {
            'sheetObj': spreadsheetLevelObj.worksheet(arrayOfArguments[5]),
            'resizeRows': 2,
            'startingRowIndexToClear': 0,
            'resizeColumns': 1
        },
        {
            'sheetObj': spreadsheetLevelObj.worksheet(arrayOfArguments[6]),
            'resizeRows': 2,
            'startingRowIndexToClear': 0,
            'resizeColumns': 1
        }
    ]

    myGspreadFunc.clearAndResizeSheets(clearAndResizeParameters)
    myGspreadFunc.displayArray(spreadsheetLevelObj.worksheet(arrayOfArguments[5]), matchedArray)
    myGspreadFunc.displayArray(spreadsheetLevelObj.worksheet(arrayOfArguments[6]), filesCompletedArray)
    myGspreadFunc.autoAlignColumnsInSpreadsheet(spreadsheetLevelObj)


if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
    p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')