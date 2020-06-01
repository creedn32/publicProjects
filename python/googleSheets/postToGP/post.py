#local application imports
from pathlib import Path
import sys
pathToThisPythonFile = Path(__file__).resolve()
sys.path.append(str(pathToThisPythonFile.parents[3]))
import herokuGorilla.backend.python.myPythonLibrary._myPyFunc as _myPyFunc
import herokuGorilla.backend.python.googleSheets.myGoogleSheetsLibrary._myGoogleSheetsFunc as _myGoogleSheetsFunc
import herokuGorilla.backend.python.googleSheets.myGoogleSheetsLibrary._myGspreadFunc as _myGspreadFunc


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

    pyautogui.PAUSE = .01
    sendingKeystrokes = True

    pathToRepos = _myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')
    arrayOfPartsToAddToPath = ['privateData', 'python', 'googleCredentials', 'usingServiceAccount', 'jsonWithAPIKey.json']

    gspObj = gspread.service_account(filename=_myPyFunc.addToPath(pathToRepos, arrayOfPartsToAddToPath))
    gspSpreadsheet = gspObj.open('Transactions To Post')
    gspToPostFromSheet = gspSpreadsheet.worksheet(arrayOfArguments[1])
    toPostFromArray = gspToPostFromSheet.get_all_values()

    charactersNeedingShift = (list(range(123, 127)) + list(range(94, 96)) + list(range(62, 91)) + [60, 58] + list(range(40, 44)) + list(range(33, 39)))
    # p(charactersNeedingShift)


    columnNameToIndexObj = {}

    for columnIndexNumber, columnName in enumerate(toPostFromArray[0]):
        columnNameToIndexObj[columnName] = columnIndexNumber

    columnIndexToNumberOfTabsObj = {}


    if sendingKeystrokes:
        with pynput.mouse.Listener(on_click=_myPyFunc.functionOnClick) as listenerObj:
            print("Click on 'Clear' to begin posting...")
            listenerObj.join()



    if 'Bank Transactions' in arrayOfArguments[1]:

        columnIndexToNumberOfTabsObj[columnNameToIndexObj['Checkbook ID']] = 2
        columnIndexToNumberOfTabsObj[columnNameToIndexObj['Amount']] = 6

        optionIndexNumber = columnNameToIndexObj['Option']
        typeIndexNumber = columnNameToIndexObj['Type']
        amountIndexNumber = columnNameToIndexObj['Amount']
        arrayOfKeysResetDropDown = ['down', 'up', 'up', 'up']
        # p(columnNameToIndexObj)


        for row in toPostFromArray[1:]:

            optionData = row[optionIndexNumber]

            if row[columnNameToIndexObj['Status']] == '' and optionData != 'Enter/Edit':

                if optionData != 'Enter Transaction' or (optionData == 'Enter Transaction' and row[typeIndexNumber] not in ['Check', 'Decrease Adjustment']):
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

                            if ord(characterToType) in charactersNeedingShift:

                                priorPyAutoGuiPause = pyautogui.PAUSE
                                # pyautogui.PAUSE = .0000000000001
                                # pyautogui.hotkey('shift', characterToType)
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

                    

    elif arrayOfArguments[1] == 'Bank Transfers':

        # p(columnNameToIndexObj)

        columnIndexToNumberOfTabsObj[columnNameToIndexObj['Transfer From Checkbook ID']] = 2
        
        for row in toPostFromArray[1:]:

            if row[columnNameToIndexObj['Status']] == '':

                if numLockIsOff():
                    pyautogui.press('numlock')


                _myPyFunc.repetitiveKeyPress(2, "tab")

                rowToEnumerate = row[:]

                for columnIndexNumber, columnData in enumerate(rowToEnumerate):

                    # p(columnData)

                    if columnIndexNumber == columnNameToIndexObj['Transfer Date']:
            
                        dateObj = datetime.datetime.strptime(columnData, '%m/%d/%Y')
                        columnData = dateObj.strftime('%m%d%Y')


                    if columnIndexNumber == columnNameToIndexObj['Amount']:
                        columnData = columnData.lstrip('$').replace('.', '').replace(',', '')


                    for characterToType in columnData:

                        if ord(characterToType) in charactersNeedingShift:

                            priorPyAutoGuiPause = pyautogui.PAUSE
                            # pyautogui.PAUSE = .0000000000001
                            pyautogui.keyDown('shift')
                            pyautogui.press(characterToType)
                            pyautogui.keyUp('shift')
                            pyautogui.PAUSE = priorPyAutoGuiPause

                        else:
                            pyautogui.press(characterToType)


                    if columnIndexNumber in columnIndexToNumberOfTabsObj:
                        pass
                        _myPyFunc.repetitiveKeyPress(columnIndexToNumberOfTabsObj[columnIndexNumber], 'tab')
                    else:
                        pass
                        _myPyFunc.repetitiveKeyPress(1, 'tab')


                if not numLockIsOff():
                    pyautogui.press('numlock')


                with pynput.mouse.Listener(on_click=_myPyFunc.functionOnClick) as listenerObj:
                    print("Click on 'Post' or 'Clear' to continue with this entry...")
                    listenerObj.join()
















                #     numberTabs = 1

                #     try:
                #         string = str(row["values"][col]["formattedValue"])
                #     except:
                #         string = ""

                #     if col == 0:

                #         # string = row["values"][col]["formattedValue"]
                #         dateObj = datetime.datetime.strptime(string, "%m/%d/%Y")
                #         # print(datetime.ParseExact(string, "yyMMdd", CultureInfo.InvariantCulture))
                #         string = dateObj.strftime("%m%d%Y")



                #     elif col == 2:
                #         numberTabs = 2

                #     elif col == 3:

                #         # if len(string.split(".")) == 1:
                #         #     string = string + "00"

                #         string = string.lstrip("$").replace(".", "").replace(",", "")

                #     for letter in string:

                #         if ord(letter) in (
                #                 list(range(123, 127)) + list(range(94, 96)) + list(range(62, 91)) + [60, 58] + list(
                #             range(40, 44)) + list(range(33, 39))):

                #             currentPauseDelay = pyautogui.PAUSE
                #             pyautogui.PAUSE = .0000000000001
                #             pyautogui.keyDown("shift")
                #             pyautogui.press(letter)
                #             pyautogui.keyUp("shift")
                #             pyautogui.PAUSE = currentPauseDelay

                #         else:
                #             pyautogui.press(letter)

                #     _myPyFunc.repetitiveKeyPress(numberTabs, "tab")


                # with pynput.mouse.Listener(on_click=_myPyFunc.functionOnClick) as listenerObj:
                #     print("Click on 'Post' or 'Clear' to continue with this entry...")
                #     listenerObj.join()


if __name__ == '__main__':
    mainFunction(sys.argv)



