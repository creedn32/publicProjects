from pathlib import Path

import pyautogui, pydirectinput
pathToThisPythonFile = Path(__file__).resolve()
parentDir = pathToThisPythonFile.parents[0]
import sys
sys.path.append(str(pathToThisPythonFile.parents[3]))
from herokuGorilla.backend.python.myPythonLibrary import myPyAutoGui as m
from herokuGorilla.backend.python.googleSheets.myGoogleSheetsLibrary import myGspreadFunc

from pprint import pprint as p
import json

def mainFunction(arrayOfArguments):

    # p(arrayOfArguments[3])

    pathBelowRepos = pathToThisPythonFile

    spreadsheetLevelObj = myGspreadFunc.getSpreadsheetLevelObj(True, pathBelowRepos, googleAccountUsername=arrayOfArguments[1]).open(arrayOfArguments[2])
    
    if arrayOfArguments[4] == 'From Google Sheets':

        invoicesArray = spreadsheetLevelObj.worksheet('Invoices').get_all_values()

    elif arrayOfArguments[4] == 'From Local File':

        with open(arrayOfArguments[5], 'r') as filehandle:

            invoicesArray = json.load(filehandle)

    invoicePulledColIdx = 0
    journalEntryColIdx = 2
    acctNumColIdx = 5
    debitColIdx = 7
    creditColIdx = 8
    nameColIdx = 11


    for row in invoicesArray:

        if row[invoicePulledColIdx] == '':

            m.clickWhenLocalPNGAppears('search', parentDir)
            m.clickWhenLocalPNGAppears('journalEntryInput', parentDir)

            pyautogui.press(['tab'] * 2)
            
            if row[journalEntryColIdx]: 
                pyautogui.write(row[journalEntryColIdx])
            else:
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.press('backspace')

            exit()

            pyautogui.press(['tab'] * 5)
            pyautogui.write(row[acctNumColIdx])

            pyautogui.press(['tab'] * 4)
            pyautogui.write(row[debitColIdx])

            pyautogui.press(['tab'] * 5)
            pyautogui.write(row[creditColIdx])

            pyautogui.press('enter')

            m.waitUntilLocalPNGAppears('completedOneTransactionSmallScreen', parentDir)
            pyautogui.press(['tab'] * 15)

            while not m.locateOnScreenLocal('accountBlue', parentDir):
                p('Looking for accountBlue...')
                pydirectinput.press('down')

            while not m.locateOnScreenLocal('blue', parentDir):
                p('Looking for blue...')
                pydirectinput.press('down')

            m.doubleClickWhenLocalPNGAppears('blue', parentDir)
            m.clickWhenLocalPNGAppears('sourceDocument', parentDir)
            m.clickWhenLocalPNGAppears('imageButton', parentDir)
            
            while not m.locateOnScreenLocal('relatedDocumentsIcon', parentDir):
                m.clickWhenLocalPNGAppears('bistrackIcon', parentDir)
                
            m.clickWhenLocalPNGAppears('relatedDocumentsIcon', parentDir)
            m.clickWhenLocalPNGAppears('relatedDocumentsWindow', parentDir)

            while not m.locateOnScreenLocal('openInvoice', parentDir):
                pydirectinput.press('down')

            m.clickWhenLocalPNGAppears('openInvoice', parentDir)
            
            
            m.clickWhenLocalPNGAppears('print', parentDir)
            m.waitUntilLocalPNGAppears('selectPrinter', parentDir)
            pyautogui.press(['c', 'u', 'enter'])

            # while not m.locateOnScreenLocal('cutePDFSaveAs', parentDir):

            #     p('Looking for cutePDFSaveAs...')

            #     if m.getCoordinatesIfLocalPNGIsShowing('gpInvoiceWindowNotHighlighted', parentDir):
            #         m.clickWhenLocalPNGAppears('gpInvoiceWindowNotHighlighted', parentDir)
            #     elif m.getCoordinatesIfLocalPNGIsShowing('cutePDFSaveAsIcon', parentDir):
            #         m.clickWhenLocalPNGAppears('cutePDFSaveAsIcon', parentDir)

            m.clickWhenLocalPNGAppears('cutePDFSaveAs', parentDir)

            pyautogui.press(['tab'] * 5)  #5)

            m.typeAndWriteOnRemoteDesktop(arrayOfArguments[3] + '\\' + row[journalEntryColIdx] + ' - ' + row[acctNumColIdx] + ' - ' + row[nameColIdx].replace('\\', '').replace('&', ''))

            pyautogui.press('enter')
            
            m.clickLocalPNGWhenAppearsAndWaitUntilLocaPNGDisappears('closeGPInvoice', 'print', parentDir)

            while m.locateOnScreenLocal('closeRelatedDocuments', parentDir):
                m.clickWhenLocalPNGAppears('closeRelatedDocuments', parentDir)

            m.waitUntilLocalPNGDisappears('relatedDocumentsWindow', parentDir)

            m.clickWhenLocalPNGAppears('payablesEntry', parentDir)

            m.clickLocalPNGWhenAppearsAndWaitUntilLocaPNGDisappears('closeGPWindow', 'payablesEntryActive', parentDir)
            m.clickLocalPNGWhenAppearsAndWaitUntilLocaPNGDisappears('closeGPWindow', 'transactionEntry', parentDir)

            row[invoicePulledColIdx] = 'Yes'

            if arrayOfArguments[4] == 'From Google Sheets':

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

                # myGspreadFunc.setFiltersOnSpreadsheet(spreadsheetLevelObj)

                # myGspreadFunc.autoAlignColumnsInSpreadsheet(spreadsheetLevelObj)

            elif arrayOfArguments[4] == 'From Local File':

                with open(arrayOfArguments[5], 'w') as filehandle:
                    json.dump(invoicesArray, filehandle)




if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
    p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')