from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
import _myPyFunc
sys.path.append(str(Path(_myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'googleSheets'), 'myGoogleSheetsLibrary')))
import _myGoogleSheetsFunc, _myGspreadFunc

from pprint import pprint as p
import gspread

pathToRepos = _myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')
arrayOfPartsToAddToPath = ['privateData', 'python', 'googleCredentials']

pathToCredentialsFileServiceAccount = _myPyFunc.addToPath(pathToRepos, arrayOfPartsToAddToPath + ['usingServiceAccount', 'jsonWithAPIKey.json'])

gspObj = gspread.service_account(filename=pathToCredentialsFileServiceAccount)
gspSpreadsheet = gspObj.open("Reconcile Arrays")
gspFirstArraySheet = gspSpreadsheet.worksheet('firstArray')
gspSecondArraySheet = gspSpreadsheet.worksheet('secondArray')
gspComparisonSheet = gspSpreadsheet.worksheet('comparison')
gspEndingFirstArraySheet = gspSpreadsheet.worksheet('endingFirstArray')
gspEndingSecondArraySheet = gspSpreadsheet.worksheet('endingSecondArray')

firstArray = gspFirstArraySheet.get_all_values()
secondArray = gspSecondArraySheet.get_all_values()

firstArrayColumnIndexToCompare = 8
secondArrayColumnIndexToCompare = 4

comparisonArray = [[''] * len(firstArray[0]) + ['Side-By-Side'] + [''] * len(secondArray[0])]
# comparisonArray = []


while firstArray:

    currentFirstArrayRow = firstArray.pop(0)
    # p(currentFirstArrayRow)
    rowToAppend = currentFirstArrayRow + ['']

    for secondArrayRowCount, currentSecondArrayRow in enumerate(secondArray):

        # p(currentSecondArrayRow)

        if currentFirstArrayRow[firstArrayColumnIndexToCompare] == currentSecondArrayRow[secondArrayColumnIndexToCompare]:

            secondArrayRowToAppend = secondArray.pop(secondArrayRowCount)
            rowToAppend = rowToAppend + currentSecondArrayRow

    comparisonArray.append(rowToAppend)


# p(comparisonArray[0:2])

_myGspreadFunc.clearAndResizeSheets([gspComparisonSheet, gspEndingFirstArraySheet, gspEndingSecondArraySheet])
_myGspreadFunc.updateCells(gspComparisonSheet, comparisonArray)
_myGspreadFunc.updateCells(gspEndingFirstArraySheet, firstArray)
_myGspreadFunc.updateCells(gspEndingSecondArraySheet, secondArray)








