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

def mainFunction(arrayOfArguments):

    pathBelowRepos = pathToThisPythonFile

    spreadsheetLevelObj = myGspreadFunc.getSpreadsheetLevelObj(True, pathBelowRepos, googleAccountUsername=arrayOfArguments[2]).open(arrayOfArguments[1])
    invoicesArray = spreadsheetLevelObj.worksheet('Invoices').get_all_values()

    journalEntryColIdx = 1
    amountColIdx = 6    

    for rowIndex, row in enumerate(invoicesArray):

        if rowIndex == 1:


            m.clickWhenLocalPNGAppears('search', parentDir)
            m.clickWhenLocalPNGAppears('journalEntryInput', parentDir)
            pyautogui.press(['tab', 'tab'])
            # m.waitUntilLocalPNGAppears('journalEntryInputClicked', parentDir)
            pyautogui.write(invoicesArray[1][journalEntryColIdx])
            pyautogui.press('enter')
            m.waitUntilLocalPNGAppears('completed', parentDir)
            pyautogui.press(['tab'] * 15)

            # m.clickWhenLocalPNGAppears('blue', parentDir)

            while not m.locateOnScreenLocal('accountBlue', parentDir):
                p('Looking for accountBlue...')
                pydirectinput.press('down')

            while not m.locateOnScreenLocal('blue', parentDir):
                p('Looking for blue...')
                pydirectinput.press('down')

            m.doubleClickWhenLocalPNGAppears('blue', parentDir)
            m.clickWhenLocalPNGAppears('sourceDocument', parentDir)
            m.clickWhenLocalPNGAppears('imageButton', parentDir)
            m.clickWhenLocalPNGAppears('yellowBistrackIcon', parentDir)
            m.clickWhenLocalPNGAppears('relatedDocumentsIcon', parentDir)
            m.clickWhenLocalPNGAppears('relatedDocumentsWindow', parentDir)

            while not m.locateOnScreenLocal('openInvoice', parentDir):
                pydirectinput.press('down')

            m.clickWhenLocalPNGAppears('openInvoice', parentDir)
            m.clickWhenLocalPNGAppears('print', parentDir)
            m.waitUntilLocalPNGAppears('selectPrinter', parentDir)
            pyautogui.press(['c', 'u', 'enter'])
            m.clickWhenLocalPNGAppears('cutePDFSaveAs', parentDir)
            pyautogui.press(['tab'] * 5)
            m.typeAndWriteOnRemoteDesktop(arrayOfArguments[3] + row[journalEntryColIdx] + ' - ' + row[amountColIdx])
            m.clickLocalPNGWhenAppearsAndWaitUntilLocaPNGDisappears('cutePDFSaveButton', 'cutePDFSaveAs', parentDir)
            
            time.sleep(5)

            m.clickLocalPNGWhenAppearsAndWaitUntilLocaPNGDisappears('closeGPInvoice', 'print', parentDir)
            m.clickLocalPNGWhenAppearsAndWaitUntilLocaPNGDisappears('closeRelatedDocuments', 'relatedDocumentsWindow', parentDir)

            m.clickWhenLocalPNGAppears('payablesEntry', parentDir)

            m.clickLocalPNGWhenAppearsAndWaitUntilLocaPNGDisappears('closeGPWindow', 'payablesEntryActive', parentDir)
            m.clickLocalPNGWhenAppearsAndWaitUntilLocaPNGDisappears('closeGPWindow', 'transactionEntry', parentDir)









if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
    p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')