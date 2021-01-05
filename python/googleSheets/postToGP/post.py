#local application imports
from pathlib import Path
import sys
pathToThisPythonFile = Path(__file__).resolve()
sys.path.append(str(pathToThisPythonFile.parents[4]))
import herokuGorilla.backend.python.myPythonLibrary.myPyFunc as myPyFunc
import herokuGorilla.backend.python.myPythonLibrary.myPyAutoGui as myPyAutoGui
import herokuGorilla.backend.python.googleSheets.myGoogleSheetsLibrary.myGoogleSheetsFunc as myGoogleSheetsFunc
import herokuGorilla.backend.python.googleSheets.myGoogleSheetsLibrary.myGspreadFunc as myGspreadFunc

#third-party imports
import gspread


#standard library imports
from pprint import pprint as p
import datetime, pyautogui, pynput.mouse



#third-party imports
import gspread





def mainFunction(arrayOfArguments):

    pyautogui.PAUSE = 0.01
    sendingKeystrokes = True

    # pathToRepos = myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')
    # arrayOfPartsToAddToPath = ['privateData', 'python', 'googleCredentials', 'usingServiceAccount', 'jsonWithAPIKey.json']

    # gspObj = gspread.service_account(filename=myPyFunc.addToPath(pathToRepos, arrayOfPartsToAddToPath))

    pathBelowRepos = pathToThisPythonFile
    spreadsheetLevelObj = myGspreadFunc.getSpreadsheetLevelObj(True, pathBelowRepos, googleAccountUsername=arrayOfArguments[1]).open('Transactions To Post')
    sheetName = arrayOfArguments[2]
    toPostFromArray = spreadsheetLevelObj.worksheet(sheetName).get_all_values()

    # charactersNeedingShift = (list(range(123, 127)) + list(range(94, 96)) + list(range(62, 91)) + [60, 58] + list(range(40, 44)) + list(range(33, 39)))
    # p(charactersNeedingShift)


    columnNameToIndexObj = {}

    for columnIndexNumber, columnName in enumerate(toPostFromArray[0]):
        columnNameToIndexObj[columnName] = columnIndexNumber

    columnNameToNumberOfTabsObj = {}


    if sendingKeystrokes:
        with pynput.mouse.Listener(on_click=myPyFunc.functionOnClick) as listenerObj:
            print("Click on 'Clear' to begin posting...")
            listenerObj.join()



    if 'Bank Transactions' in sheetName:

        columnNameToNumberOfTabsObj['Checkbook ID'] = 2
        columnNameToNumberOfTabsObj['Amount'] = 6

        arrayOfKeysResetDropDown = ['down', 'up', 'up', 'up']
        # p(columnNameToIndexObj)


        for row in toPostFromArray[1:]:   #toPostFromArray[1728:1729]: #

            optionData = row[columnNameToIndexObj['Option']]

            if row[columnNameToIndexObj['Status']] == '' and optionData != 'Enter/Edit':

                if optionData != 'Enter Transaction' or (optionData == 'Enter Transaction' and row[columnNameToIndexObj['Type']] not in ['Check', 'Decrease Adjustment']):
                    columnNameToNumberOfTabsObj['Account'] = 2
                else:
                    columnNameToNumberOfTabsObj['Account'] = 1


                if myPyFunc.numLockIsOff():
                    pyautogui.press('numlock')

                # p(columnNameToNumberOfTabsObj)
                # p(columnNameToIndexObj)

                for columnIndexNumber, columnData in enumerate(row):

                    for columnIndexNumberFromObj, columnNameFromObj in enumerate(columnNameToIndexObj):
                            if columnIndexNumberFromObj == columnIndexNumber:
                                currentColumnName = columnNameFromObj

                    if currentColumnName not in ['Status', 'Person', 'Notes1', 'Notes2']:  #< 9: # 

                        # p(currentColumnName) 

                        if currentColumnName in ['Option', 'Type']:
                            
                            pyautogui.press(arrayOfKeysResetDropDown)

                            numberOfDownKeyPresses = 0

                            if columnData in ['Enter Receipt', 'Cash']:
                                numberOfDownKeyPresses = 1  
                            if columnData == 'Increase Adjustment':
                                numberOfDownKeyPresses = 2
                            if columnData == 'Decrease Adjustment':
                                numberOfDownKeyPresses = 3

                            myPyAutoGui.repetitiveKeyPress(numberOfDownKeyPresses, 'down')


                        if currentColumnName == 'Transaction Date':

                            # p(columnData)
                            dateObj = datetime.datetime.strptime(columnData, '%m/%d/%Y')
                            columnData = dateObj.strftime('%m%d%Y')


                        if currentColumnName == 'Account':
                            columnData = columnData.replace('-', '')


                        if currentColumnName in ['Amount', 'Amount2']:
                            columnData = columnData.lstrip('$').replace('.', '').replace(',', '')

                        if currentColumnName not in ['Option', 'Type']:

                            myPyAutoGui.typeCharactersOnRemoteDesktop(columnData)

                        if currentColumnName in columnNameToNumberOfTabsObj:
                            myPyAutoGui.repetitiveKeyPress(columnNameToNumberOfTabsObj[currentColumnName], 'tab')
                        else:
                            myPyAutoGui.repetitiveKeyPress(1, 'tab')


                if not myPyFunc.numLockIsOff():
                    pyautogui.press('numlock')


                with pynput.mouse.Listener(on_click=myPyFunc.functionOnClick) as listenerObj:
                    print("Click on 'Post' or 'Clear' to continue with this entry...")
                    listenerObj.join()



    elif sheetName == 'Bank Transfers':

        # p(columnNameToIndexObj)

        columnNameToNumberOfTabsObj[columnNameToIndexObj['Transfer From Checkbook ID']] = 2

        for row in toPostFromArray[1:]:

            if row[columnNameToIndexObj['Status']] == '':

                if myPyFunc.numLockIsOff():
                    pyautogui.press('numlock')


                myPyAutoGui.repetitiveKeyPress(2, "tab")

                rowToEnumerate = row[0:5]

                # p(rowToEnumerate)

                for columnIndexNumber, columnData in enumerate(rowToEnumerate):

                    # p(columnData)

                    if columnIndexNumber == columnNameToIndexObj['Transfer Date']:

                        dateObj = datetime.datetime.strptime(columnData, '%m/%d/%Y')
                        columnData = dateObj.strftime('%m%d%Y')


                    if columnIndexNumber == columnNameToIndexObj['Amount']:
                        columnData = columnData.lstrip('$').replace('.', '').replace(',', '')


                    myPyAutoGui.typeCharactersOnRemoteDesktop(columnData)

                    # for characterToType in columnData:

                    #     if ord(characterToType) in charactersNeedingShift:

                    #         priorPyAutoGuiPause = pyautogui.PAUSE
                    #         pyautogui.PAUSE = .000000000001
                    #         pyautogui.keyDown('shift')
                    #         pyautogui.press(characterToType)
                    #         pyautogui.keyUp('shift')
                    #         pyautogui.PAUSE = priorPyAutoGuiPause

                    #     else:
                    #         pyautogui.press(characterToType)


                    if columnIndexNumber in columnNameToNumberOfTabsObj:
                        pass
                        myPyAutoGui.repetitiveKeyPress(columnNameToNumberOfTabsObj[columnIndexNumber], 'tab')
                    else:
                        pass
                        myPyAutoGui.repetitiveKeyPress(1, 'tab')


                if not myPyFunc.numLockIsOff():
                    pyautogui.press('numlock')


                with pynput.mouse.Listener(on_click=myPyFunc.functionOnClick) as listenerObj:
                    print("Click on 'Post' or 'Clear' to continue with this entry...")
                    listenerObj.join()


if __name__ == '__main__':
    mainFunction(sys.argv)



