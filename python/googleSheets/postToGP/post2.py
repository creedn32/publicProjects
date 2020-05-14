#local application imports
#local application imports
from pathlib import Path
import sys
pathToThisPythonFile = Path(__file__).resolve()
sys.path.append(str(pathToThisPythonFile.parents[2]))
import myPythonLibrary._myPyFunc as _myPyFunc
import googleSheets.myGoogleSheetsLibrary._myGoogleSheetsFunc as _myGoogleSheetsFunc
import googleSheets.myGoogleSheetsLibrary._myGspreadFunc as _myGspreadFunc


#standard library imports
from pprint import pprint as p
import datetime, pynput.mouse, win32api, win32con, pyautogui, time

#third-party imports
import gspread


#standard library imports
import datetime
from pprint import pprint as p
import pyautogui, pynput.mouse, time, win32api, win32con, time



#third-party imports
import gspread


def numLockIsOff():
    if win32api.GetKeyState(win32con.VK_NUMLOCK) == 1:
        return True
    else:
        return False  


def mainFunction(arrayOfArguments):
    objOfSheets = _myGspreadFunc.getObjOfSheets('Transactions To Post')

    columnNameToIndexObj = {}

    for columnIndexNumber, columnName in enumerate(objOfSheets[sys.argv[1]]['array'][0]):
        columnNameToIndexObj[columnName] = columnIndexNumber

    columnIndexToNumberOfTabsObj = {}
    
    columnIndexToNumberOfTabsObj[columnNameToIndexObj['Checkbook ID']] = 2
    columnIndexToNumberOfTabsObj[columnNameToIndexObj['Amount']] = 6

    optionIndexNumber = columnNameToIndexObj['Option']
    typeIndexNumber = columnNameToIndexObj['Type']
    amountIndexNumber = columnNameToIndexObj['Amount']
    arrayOfKeysResetDropDown = ['down', 'up', 'up', 'up']
    # p(columnNameToIndexObj)

    with pynput.mouse.Listener(on_click=_myPyFunc.functionOnClick) as listenerObj:
        print("Click on 'Clear' to begin posting...")
        listenerObj.join()



    for row in objOfSheets[sys.argv[1]]['array'][1:]:

        optionData = row[optionIndexNumber]

        if row[columnNameToIndexObj['Status']] == '' and optionData != 'Enter/Edit':

            if optionData != 'Enter Transaction' or  (optionData == 'Enter Transaction' and row[typeIndexNumber] not in ['Check', 'Decrease Adjustment']):
                columnIndexToNumberOfTabsObj[columnNameToIndexObj['Account']] = 2
            else:
                columnIndexToNumberOfTabsObj[columnNameToIndexObj['Account']] = 1

           
            if numLockIsOff():
                pyautogui.press('numlock')
            
            for columnIndexNumber, columnData in enumerate(row):

                if columnIndexNumber in [optionIndexNumber, typeIndexNumber]:
                    
                    pyautogui.press(arrayOfKeysResetDropDown)

                    numberOfDownKeyPresses = 0

                    if columnData in ['Enter Receipt', 'Cash']:
                        numberOfDownKeyPresses = 1
                    if columnData == 'Increase Adjustment':
                        numberOfDownKeyPresses = 2
                    if columnData == 'Decrease Adjustment':
                        numberOfDownKeyPresses = 3

                    _myPyFunc.repetitiveKeyPress(numberOfDownKeyPresses, 'down')


                if columnIndexNumber == columnNameToIndexObj['Transaction Date']:
    
                    # p(columnData)
                    dateObj = datetime.datetime.strptime(columnData, '%m/%d/%Y')
                    columnData = dateObj.strftime('%m%d%Y')


                if columnIndexNumber == columnNameToIndexObj['Account']:
                    columnData = columnData.replace('-', '')


                if columnIndexNumber in [amountIndexNumber, columnNameToIndexObj['Amount2']]:
                    columnData = columnData.lstrip('$').replace('.', '').replace(',', '')

                if columnIndexNumber not in [optionIndexNumber, typeIndexNumber]:

                    for characterToType in columnData:

                        characterNeedingShift = (list(range(123, 127)) + list(range(94, 96)) + list(range(62, 91)) + [60, 58] + list(range(40, 44)) + list(range(33, 39)))
                        
                        if ord(characterToType) in characterNeedingShift:

                            priorPyAutoGuiPause = pyautogui.PAUSE
                            pyautogui.PAUSE = .0000000000001
                            pyautogui.keyDown('shift')
                            pyautogui.press(characterToType)
                            pyautogui.keyUp('shift')
                            pyautogui.PAUSE = priorPyAutoGuiPause

                        else:
                            pyautogui.press(characterToType)


                if columnIndexNumber in columnIndexToNumberOfTabsObj:
                    _myPyFunc.repetitiveKeyPress(columnIndexToNumberOfTabsObj[columnIndexNumber], 'tab')
                else:
                    _myPyFunc.repetitiveKeyPress(1, 'tab')


            if not numLockIsOff():
                pyautogui.press('numlock')


            with pynput.mouse.Listener(on_click=_myPyFunc.functionOnClick) as listenerObj:
                print("Click on 'Post' or 'Clear' to continue with this entry...")
                listenerObj.join()



if __name__ == '__main__':
    mainFunction(sys.argv)



