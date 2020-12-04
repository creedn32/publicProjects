from pathlib import Path

import pyautogui, pydirectinput
pathToThisPythonFile = Path(__file__).resolve()
parentDir = pathToThisPythonFile.parents[0]
import sys
sys.path.append(str(pathToThisPythonFile.parents[3]))
from herokuGorilla.backend.python.myPythonLibrary import myPyFunc
from herokuGorilla.backend.python.myPythonLibrary import myPyAutoGui as m
from herokuGorilla.backend.python.googleSheets.myGoogleSheetsLibrary import myGspreadFunc

from pprint import pprint as p
import datetime
import time
import json

def mainFunction(arrayOfArguments):

    pathBelowRepos = pathToThisPythonFile

    spreadsheetLevelObj = myGspreadFunc.getSpreadsheetLevelObj(True, pathBelowRepos, googleAccountUsername=arrayOfArguments[2]).open(arrayOfArguments[1])
    
    with open(arrayOfArguments[3], 'r') as filehandle:

        invoicesArray = json.load(filehandle)

    clearAndResizeParameters = [
        {
            'sheetObj': spreadsheetLevelObj.worksheet('Invoices'),
            'resizeRows': 2,
            'startingRowIndexToClear': 0,
            'resizeColumns': 1
        },
    ]

    myGspreadFunc.clearAndResizeSheets(clearAndResizeParameters)
    myGspreadFunc.displayArray(spreadsheetLevelObj.worksheet('Invoices'), invoicesArray)
    myGspreadFunc.autoAlignColumnsInSpreadsheet(spreadsheetLevelObj)


if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
    p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')