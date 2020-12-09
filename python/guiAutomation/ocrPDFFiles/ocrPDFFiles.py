from pathlib import Path

import pyautogui
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(pathToThisPythonFile.parents[3]))
from herokuGorilla.backend.python.myPythonLibrary import myPyFunc
from herokuGorilla.backend.python.myPythonLibrary import myPyAutoGui
from herokuGorilla.backend.python.googleSheets.myGoogleSheetsLibrary import myGspreadFunc

from pprint import pprint as p
import datetime

def addFileToAcrobatOCRList(fileObj):

    myPyAutoGui.clickWhenLocalPNGAppears('addFilesButton', pathToThisPythonFile.parents[0])

    pyautogui.press('f')
    myPyAutoGui.getCoordinatesWhenLocalPNGAppears('filenameBoxReady', pathToThisPythonFile.parents[0])

    pyautogui.write(str(fileObj))
    pyautogui.press('enter')
    myPyAutoGui.waitUntilLocalPNGDisappears('addFilesDialogBox', pathToThisPythonFile.parents[0])


def ocrPDFFiles(arrayOfArguments):


    pathBelowRepos = pathToThisPythonFile
    spreadsheetLevelObj = myGspreadFunc.getSpreadsheetLevelObj(True, pathBelowRepos, googleAccountUsername=arrayOfArguments[1]).open(arrayOfArguments[2])

    filesSheetName = arrayOfArguments[3]
    googleSheetsFileArray = spreadsheetLevelObj.worksheet(filesSheetName).get_all_values()

    groupMax = 60

    filePathColIdx = 0
    completedColIdx = 1
    matchedFilePathColIdx = 2

    currentGroupCount = 0
    currentGroupRowIndices = []

    for rowIndex, row in enumerate(googleSheetsFileArray):

        if rowIndex and row[matchedFilePathColIdx] == '':

            fileObjPath = Path(row[filePathColIdx])

            # addFileToAcrobatOCRList(fileObjPath)

            currentGroupCount = currentGroupCount + 1
            currentGroupRowIndices.append(rowIndex)


            # row[completedColIdx] = 'Yes - ' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

            if currentGroupCount == groupMax or rowIndex == len(googleSheetsFileArray) - 1:

            #     myPyAutoGui.clickWhenLocalPNGAppears('nextButtonBeginOCR', pathToThisPythonFile.parents[0])
            #     myPyAutoGui.clickWhenLocalPNGAppears('closeActionCompleted', pathToThisPythonFile.parents[0])
            #     myPyAutoGui.waitUntilLocalPNGDisappears('closeActionCompleted', pathToThisPythonFile.parents[0])

                # p(currentGroupCount)

                # if currentGroupRowIndices[0] == 92:
                #     p(currentGroupRowIndices)

                # p(currentGroupRowIndices[0])
                # p(currentGroupRowIndices[59])


            #     pyautogui.press(['alt', 'f', 'w', 'down', 'down', 'enter'])


            #     clearAndResizeParameters = [
            #         {
            #             'sheetObj': spreadsheetLevelObj.worksheet(filesSheetName),
            #             'resizeRows': 2,
            #             'startingRowIndexToClear': 0,
            #             'resizeColumns': 1
            #         },
            #     ]

            #     myGspreadFunc.clearAndResizeSheets(clearAndResizeParameters)
            #     myGspreadFunc.displayArray(spreadsheetLevelObj.worksheet(filesSheetName), googleSheetsFileArray)
            #     # myGspreadFunc.autoAlignColumnsInSpreadsheet(spreadsheetLevelObj)


                for currentGroupRowIndex in currentGroupRowIndices:

                    googleSheetsFileArray[currentGroupRowIndex] = 'Yes - ' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

                currentGroupCount = 0
                currentGroupRowIndices = []




def mainFunction(arrayOfArguments):

    ocrPDFFiles(arrayOfArguments)


if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
    p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')