from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'googleSheets', 'library')))
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'library')))


import _myGoogleSheetsLibrary, _myPyFunc
from runpy import run_path as runPath
from pprint import pprint as pp
import time, pynput.mouse, pyautogui
pyautogui.PAUSE = .0000000000001


idOfSpreadsheetToPullDataFrom = "1Jdl2wIHinX6A8O6H18l34V-qzorLPXxWMGeRsQ8FYy4"
googleSheetsAPIObj = _myGoogleSheetsLibrary.getGoogleSheetsAPIObj(['privateData', 'python', 'googleCredentials'])
# dataOfSpreadsheetToPullDataFrom = googleSheetsAPIObj.get(spreadsheetId=idOfSpreadsheetToPullDataFrom, includeGridData=True).execute()

# for dict in dataOfSpreadsheetToPullDataFrom["sheets"]:
#     if dict["properties"]["title"] == "Accounts To Create":
#         dataOfSheetToPullDataFrom = dict["data"][0]["rowData"]



# with pynput.mouse.Listener(on_click=myPyFunc.functionOnClick) as listenerObj:
#     print("Click the mouse to begin...")
#     listenerObj.join()


# for row in dataOfSheetToPullDataFrom[1:]:

#     charactersToType = row["values"][0]["formattedValue"]

#     print("The following string of characters will be entered: " + charactersToType)

#     time.sleep(.5)

#     for character in charactersToType:

#         if ord(character) in (
#                 list(range(123, 127)) + list(range(94, 96)) + list(range(62, 91)) + [60, 58] + list(
#             range(40, 44)) + list(range(33, 39))):

#             pyautogui.PAUSE = .0000000000001
#             pyautogui.press(character)


#         else:
#             pyautogui.press(character)


#     myPyFunc.repetitiveKeyPress(1, "tab")



#     with pynput.mouse.Listener(on_click=myPyFunc.functionOnClick) as listenerObj:
#         print("Click the mouse to continue...")
#         listenerObj.join()


