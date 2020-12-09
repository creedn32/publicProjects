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
import time
import re
import pyperclip
import platform

def addFileToAcrobatOCRList(fileObj):

    while not myPyAutoGui.locateOnScreenLocal('addFilesButton', pathToThisPythonFile.parents[0]) and not myPyAutoGui.locateOnScreenLocal('acrobatStartScreen', pathToThisPythonFile.parents[0]):

        p('Waiting for Acrobat to appear...')

    if myPyAutoGui.locateOnScreenLocal('addFilesButton', pathToThisPythonFile.parents[0]):
        
        myPyAutoGui.clickWhenLocalPNGAppears('addFilesButton', pathToThisPythonFile.parents[0])
    
    elif myPyAutoGui.locateOnScreenLocal('acrobatStartScreen', pathToThisPythonFile.parents[0]):
        
        pyautogui.press(['alt', 'f', 'w', 'down', 'down', 'enter'])
        myPyAutoGui.clickWhenLocalPNGAppears('addFilesButton', pathToThisPythonFile.parents[0])

    pyautogui.press('f')
    myPyAutoGui.getCoordinatesWhenLocalPNGAppears('filenameBoxReady', pathToThisPythonFile.parents[0])

    pyperclip.copy(str(fileObj))

    if platform.system() == 'Darwin':
        pyautogui.hotkey('command', 'v')
    else:
        pyautogui.hotkey('ctrl', 'v')


    # def type_unicode(word):
    #     for c in word:
    #         c = '%04x' % ord(c)
    #         pyautogui.keyDown('optionleft')
    #         pyautogui.typewrite(c)
    #         pyautogui.keyUp('optionleft')


    # import pyautogui as px

    # def type_unicode(word):
    #     for char in word:
    #         num = hex(ord(char))
    #         px.hotkey('ctrl', 'shift', 'u')
    #         for n in num:
    #             px.typewrite(n)
    #         px.typewrite('\n')


    pyautogui.press('enter')
    myPyAutoGui.waitUntilLocalPNGDisappears('addFilesDialogBox', pathToThisPythonFile.parents[0])


def ocrPDFFiles(arrayOfArguments):

    pathBelowRepos = pathToThisPythonFile
    spreadsheetLevelObj = myGspreadFunc.getSpreadsheetLevelObj(True, pathBelowRepos, googleAccountUsername=arrayOfArguments[1]).open(arrayOfArguments[2])

    filesSheetName = arrayOfArguments[3]
    googleSheetsFileArray = spreadsheetLevelObj.worksheet(filesSheetName).get_all_values()

    filePathColIdx = 0
    completedColIdx = 3
    lastRowIndexToOCR = None

    for rowIndex, row in enumerate(googleSheetsFileArray):

        if row[completedColIdx] == '':

            lastRowIndexToOCR = rowIndex

    currentGroupCount = 0
    currentGroupRowIndices = []

    for rowIndex, row in enumerate(googleSheetsFileArray):

        if row[completedColIdx] == '':

            fileObjPath = Path(row[filePathColIdx])

            addFileToAcrobatOCRList(fileObjPath)

            currentGroupCount = currentGroupCount + 1
            currentGroupRowIndices.append(rowIndex)


            if currentGroupCount == int(arrayOfArguments[5]) or rowIndex == lastRowIndexToOCR:

                myPyAutoGui.clickWhenLocalPNGAppears('nextButtonBeginOCR', pathToThisPythonFile.parents[0])
                myPyAutoGui.clickWhenLocalPNGAppears('closeActionCompleted', pathToThisPythonFile.parents[0])
                myPyAutoGui.waitUntilLocalPNGDisappears('closeActionCompleted', pathToThisPythonFile.parents[0])

                for currentGroupRowIndex in currentGroupRowIndices:

                    googleSheetsFileArray[currentGroupRowIndex][completedColIdx] = 'Yes - ' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

                clearAndResizeParameters = [
                    {
                        'sheetObj': spreadsheetLevelObj.worksheet(arrayOfArguments[4]),
                        'resizeRows': 2,
                        'startingRowIndexToClear': 0,
                        'resizeColumns': 1
                    },
                ]

                p('Updating Google Sheets...')

                myGspreadFunc.clearAndResizeSheets(clearAndResizeParameters)
                myGspreadFunc.displayArray(spreadsheetLevelObj.worksheet(arrayOfArguments[4]), googleSheetsFileArray)
                # myGspreadFunc.autoAlignColumnsInSpreadsheet(spreadsheetLevelObj)

                p('Done updating Google Sheets.')
                
                currentGroupCount = 0
                currentGroupRowIndices = []

                pyautogui.press(['alt', 'f', 'w', 'down', 'down', 'enter'])




def mainFunction(arrayOfArguments):

    ocrPDFFiles(arrayOfArguments)


if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
    p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')