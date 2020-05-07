from pathlib import Path
import sys
pathToThisPythonFile = Path(__file__).resolve()
sys.path.append(str(pathToThisPythonFile.parents[2]))
import myPythonLibrary._myPyFunc as _myPyFunc

import gspread


def clearArray(startingRow, endingRow, startingColumn, endingColumn, arrayOfSheet):

    if endingRow == -1:
        endingRow = len(arrayOfSheet) - 1
    if endingColumn == -1:
        endingColumn = len(arrayOfSheet[len(arrayOfSheet) - 1]) - 1

    for row in range(startingRow, endingRow + 1):
        for column in range(startingColumn, endingColumn + 1):
            arrayOfSheet[row][column] = ''

    return arrayOfSheet



def clearSheet(startingRow, endingRow, startingColumn, endingColumn, gspSheetOfArray):

    arrayOfSheet = gspSheetOfArray.get_all_values()

    if len(arrayOfSheet) > 0:

        arrayOfSheet = clearArray(startingRow, endingRow, startingColumn, endingColumn, gspSheetOfArray.get_all_values())
        updateCells(gspSheetOfArray, arrayOfSheet)

        


def clearSheets(startingRow, endingRow, startingColumn, endingColumn, arrayOfSheetObjects):
    
    for sheetObj in arrayOfSheetObjects:
        clearSheet(startingRow, endingRow, startingColumn, endingColumn, sheetObj)



def clearAndResizeSheets(arrayOfSheetObjects):

    for sheetObj in arrayOfSheetObjects:
        sheetObj.resize(rows=1, cols=1)
        clearSheet(0, -1, 0, -1, sheetObj)



def updateCells(gspSheetOfArray, arrayOfSheet):

    if len(arrayOfSheet) > 0:

        numberOfRowsInArrayOfSheet = len(arrayOfSheet)

        numberOfColumnsInArrayOfSheet = 0

        for row in arrayOfSheet:
            if len(row) > numberOfColumnsInArrayOfSheet:
                numberOfColumnsInArrayOfSheet = len(row)
        
        startingCell = 'R1C1'
        endingCell = 'R' + str(numberOfRowsInArrayOfSheet) + 'C' + str(numberOfColumnsInArrayOfSheet)
        addressOfSheet = startingCell + ':' + endingCell

        # print(addressOfSheet)
        gspSheetOfArray.update(addressOfSheet, arrayOfSheet)



def getGspSpreadsheetObj(spreadsheetName):
    #return gspread spreadsheet object

    pathToRepos = _myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')
    arrayOfPartsToAddToPath = ['privateData', 'python', 'googleCredentials', 'usingServiceAccount', 'jsonWithAPIKey.json']

    pathToCredentialsFileServiceAccount = _myPyFunc.addToPath(pathToRepos, arrayOfPartsToAddToPath)

    gspObj = gspread.service_account(filename=pathToCredentialsFileServiceAccount)

    return gspObj.open(spreadsheetName)
