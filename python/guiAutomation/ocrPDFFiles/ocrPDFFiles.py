from pathlib import Path

import pyautogui
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(pathToThisPythonFile.parents[3]))
from herokuGorilla.backend.python.myPythonLibrary import myPyFunc
from herokuGorilla.backend.python.myPythonLibrary import myPyAutoGui
from herokuGorilla.backend.python.googleSheets.myGoogleSheetsLibrary import myGspreadFunc

from pprint import pprint as p

def addFileToOCRList(fileObj):

    pass

    # myPyAutoGui.clickWhenLocalPNGAppears('addFilesButton', pathToThisPythonFile.parents[0])

    # pyautogui.press('f')
    # myPyAutoGui.getCoordinatesWhenLocalPNGAppears('addFilesDialogBox', pathToThisPythonFile.parents[0])

    # pyautogui.keyDown('shift')

    # while not myPyAutoGui.getCoordinatesIfLocalPNGIsShowing('pathArrow', pathToThisPythonFile.parents[0]):
    #     pyautogui.press('tab')


    # pyautogui.keyUp('shift')

    # pyautogui.press('enter')
    # pyautogui.write(str(dataForActionObj['currentFileObj'].parents[0]))
    # pyautogui.press('enter')

    # myPyAutoGui.getCoordinatesWhenLocalPNGAppears('folderBoxReady', pathToThisPythonFile.parents[0])

    # while not myPyAutoGui.getCoordinatesIfLocalPNGIsShowing('filenameBoxReady', pathToThisPythonFile.parents[0], confidence=.95):
    #     pyautogui.press('tab')

    # pyautogui.write(str(dataForActionObj['currentFileObj'].name))
    # pyautogui.press('enter')
    # myPyAutoGui.waitUntilLocalPNGDisappears('addFilesDialogBox', pathToThisPythonFile.parents[0])




def getArrayOfPDFFiles(pathToRoot):

    def ifPDFFile(fileObj):

        if fileObj.is_file() and fileObj.suffix == '.pdf': return fileObj

        return False

    return myPyFunc.getArrayOfFileObjInTreeBreadthFirst(Path(pathToRoot), ifPDFFile)



def ocrPDFFiles(arrayOfArguments):

    # arrayOfPDFFiles = getArrayOfPDFFiles(arrayOfArguments[1])

    filesSheetName = 'Files'
    pathBelowRepos = pathToThisPythonFile
    spreadsheetLevelObj = myGspreadFunc.getSpreadsheetLevelObj(True, pathBelowRepos, googleAccountUsername=arrayOfArguments[3]).open(arrayOfArguments[2])
    
    googleSheetsFileArray = spreadsheetLevelObj.worksheet(filesSheetName).get_all_values()

    groupMax = 4
    currentGroupCount = 0

    filePathColIdx = 0
    completedColIdx = 1

    for rowIndex, row in enumerate(googleSheetsFileArray):

        if rowIndex:

            if row[completedColIdx] != 'Yes':

                addFileToOCRList(row[filePathColIdx])
                currentGroupCount = currentGroupCount + 1

            if currentGroupCount == groupMax or rowIndex == len(googleSheetsFileArray) - 1:

                p(row[filePathColIdx])
                # myPyAutoGui.clickWhenLocalPNGAppears('nextButtonBeginOCR', pathToThisPythonFile.parents[0])
                currentGroupCount = 0


    clearAndResizeParameters = [
        {
            'sheetObj': spreadsheetLevelObj.worksheet(filesSheetName),
            'resizeRows': 2,
            'startingRowIndexToClear': 0,
            'resizeColumns': 1
        },
    ]

    myGspreadFunc.clearAndResizeSheets(clearAndResizeParameters)
    myGspreadFunc.displayArray(spreadsheetLevelObj.worksheet(filesSheetName), googleSheetsFileArray)
    myGspreadFunc.autoAlignColumnsInSpreadsheet(spreadsheetLevelObj)





def mainFunction(arrayOfArguments):

    ocrPDFFiles(arrayOfArguments)


if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
    p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')