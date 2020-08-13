from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
# sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
# import _myPyFunc

import pyautogui as g
from pprint import pprint as p
import time
import win32com.client
from datetime import date


pathToTxtFile = Path(pathToThisPythonFile.parents[4], 'privateData', 'python', 'guiAutomation', 'saveStatementOfCashFlows', 'pathToSaveFile.txt')

with open(pathToTxtFile, 'rt') as pathToSaveFileTxt: 
    pathToSaveFile = Path(pathToSaveFileTxt.read())

if len(sys.argv) > 2:
    startingYear = int(sys.argv[2])
else:
    startingYear = 1969 

for year in range(startingYear, 2021):

    quickbooksFromCoordinates = None

    while not quickbooksFromCoordinates:
        p('Looking for From field...')
        quickbooksFromCoordinates = g.locateOnScreen('quickBooksFrom.png')

    g.click(quickbooksFromCoordinates[0] + 45, quickbooksFromCoordinates[1] + 10)

    g.press(['backspace']*10)
    g.press(['delete']*10)
    g.write('01/01/' + str(year))
    g.press('tab')
    g.write('12/31/' + str(year))
    g.press('tab')

    while not g.locateOnScreen('quickBooksStatementOfCashFlowsTitle.png', grayscale=True, confidence=.9):
        p('Looking for title of Statement of Cash Flows...')

    locatedBoxNetCashFlow = g.locateOnScreen('quickBooksNoCashFlow.png', grayscale=True, confidence=.9)

    if locatedBoxNetCashFlow:

        p('There are no cash flows in ' + str(year))
    
    else:

        p('There are cash flows in ' + str(year))

        g.hotkey('alt', 't')
        g.press(['p', 'enter'], interval=.2)

        while not g.locateOnScreen('quickbooksSave.png'):
            p('Looking for Save Document As PDF window...')

        pathToSaveFileWithFilename = Path(pathToSaveFile, 'Cash Flow - ' + sys.argv[1] + ' - ' + str(year) + ' - ' + date.today().strftime('%Y%m%d'))
        g.write(str(pathToSaveFileWithFilename))
        g.press('enter')

        while g.locateOnScreen('quickbooksSave.png', confidence=.9):
            p('Waiting for Save Document As PDF window to close...')

        g.hotkey('alt', 'x')
        g.press('n', interval=.2)

        while not g.locateOnScreen('quickBooksCSVMarkedHighlighted.png') and not g.locateOnScreen('quickBooksCSVMarkedUnHighlighted.png'):
            
            p('Looking for CSV option button...')

            if g.locateOnScreen('quickBooksCSVUnMarkedHighlighted.png', confidence=.95):
                g.press(['space', 'enter'])
                break
            else:
                g.press('down')



        while not g.locateOnScreen('quickbooksCreateDiskFile.png'):
            p('Looking for Create Disk File window...')
        
        g.write(str(pathToSaveFileWithFilename))
        g.press('enter')

        while g.locateOnScreen('quickbooksCreateDiskFile.png'):
            p('Wating for Create Disk File window to close...')


    # break