import sys, pathlib, time
sys.path.append(str(pathlib.Path.cwd().parents[1])) #for myPyLib
from myPyLib import myPyFunc, myGoogleSheetsFunc

startTime = time.time()
print("Comment: Importing modules and setting up variables...")

# import datetime, pynput.mouse, win32api, win32con, pyautogui
import pynput.mouse, pyautogui, time

pyautogui.PAUSE = 0
activateKeyboard = True

dataEntrypreadsheetID = "1Jdl2wIHinX6A8O6H18l34V-qzorLPXxWMGeRsQ8FYy4"
# sheetsToDownload = ["Raw Data - Robinhood", "Transactions To Add - Robinhood"]
googleSheetsAPIObj = myGoogleSheetsFunc.authFunc()
googleSheetsData = googleSheetsAPIObj.get(spreadsheetId=dataEntrypreadsheetID, includeGridData=True).execute()

for dict in googleSheetsData["sheets"]:
    if dict["properties"]["title"] == "Accounts To Create":
        currentSheetIDStr = dict["properties"]["sheetId"]
        currentSheetData = dict["data"][0]["rowData"]



print("Comment: Importing modules and setting up variables...Done. " + str(round(time.time() - startTime, 3)) + " seconds")


if activateKeyboard:
    with pynput.mouse.Listener(on_click=myPyFunc.functionOnClick) as listenerObj:
        print("Click 'Save' to begin creating accounts...")
        listenerObj.join()


for row in currentSheetData[1:]:

    charactersToType = row["values"][0]["formattedValue"]

    print("The following string of characters will be entered: " + charactersToType)

    time.sleep(.5)

    for character in charactersToType:

        if ord(character) in (
                list(range(123, 127)) + list(range(94, 96)) + list(range(62, 91)) + [60, 58] + list(
            range(40, 44)) + list(range(33, 39))):

            pyautogui.PAUSE = .0000000000001
            pyautogui.press(character)


        else:
            pyautogui.press(character)


    myPyFunc.repetitiveKeyPress(1, "tab")



    with pynput.mouse.Listener(on_click=myPyFunc.functionOnClick) as listenerObj:
        print("Click 'Save' to continue with this entry...")
        listenerObj.join()


