import sys, pathlib
sys.path.append(str(pathlib.Path.cwd().parents[1]))
sys.path.append(str(pathlib.Path.cwd().parents[0]))
from myPythonLibrary import myPythonFunctions


startTime = myPythonFunctions.startCode()


import time, importlib
import datetime, pynput.mouse, win32api, win32con, pyautogui
from pprint import pprint as pp



# class moduleNameClass:
#     pass
#
# moduleName = "myGoogleSheetsPythonLibrary"
# moduleNameObj = moduleNameClass()
#
#
#
#
# for filePath in pathlib.Path(pathlib.Path.cwd().parents[0]/moduleName).iterdir():
#     if filePath.stem not in ["__init__", "__pycache__"]:
#         importedModuleObj = importlib.import_module(moduleName + "." + filePath.stem)
#         setattr(moduleNameObj, filePath.stem, importedModuleObj)
# myGoogleSheetsPythonLibrary = moduleNameObj


import myGoogleSheetsPythonLibrary.googleSheetsAuthenticate
import myGoogleSheetsPythonLibrary.googleSheetsFunctions



# spreadsheetIDStr = "1uQezYVWkLZEvXzbprJPLRyDdyn04MdO-k6yaiyZPOx8"   #ID of public Google Sheet
spreadsheetIDStr = "1nR8wJISZjeJh6DCBf1OTpiG6rdY5DyyUtDI763axGhg"  #ID of private Google Sheet
# spreadsheetIDStr = "1kCI36ash9JI2AO0mCjbIUndRo93oiWgx2KWgeeJeP28"  #ID of simple Google Sheet
sheetName = "Bank Transactions"
# sheetName = "Bank Transactions - Recurring"
changeCellColor = False
numLockChanged = False
pyautogui.PAUSE = 0
activateKeyboard = True



googleSheetsObj = myGoogleSheetsPythonLibrary.googleSheetsAuthenticate.authFunc()
googleSheetsData = googleSheetsObj.get(spreadsheetId=spreadsheetIDStr, includeGridData=True).execute()

# with open("output.txt", "wt") as out:
#     pprint(googleSheetsData, stream=out)



for dict in googleSheetsData["sheets"]:
    if dict["properties"]["title"] == sheetName:
        currentSheetIDStr = dict["properties"]["sheetId"]
        currentSheetData = dict["data"][0]["rowData"]



requestDictionary = {}
requestDictionary["requests"] = []
requestDictionary["requests"].append({})
requestDictionary["requests"][0]["repeatCell"] = {}
requestDictionary["requests"][0]["repeatCell"]["range"] = {}
requestDictionary["requests"][0]["repeatCell"]["range"]["sheetId"] = currentSheetIDStr
requestDictionary["requests"][0]["repeatCell"]["range"]["startRowIndex"] = 0
requestDictionary["requests"][0]["repeatCell"]["range"]["endRowIndex"] = 0
requestDictionary["requests"][0]["repeatCell"]["cell"] = {}
requestDictionary["requests"][0]["repeatCell"]["cell"]["userEnteredFormat"] = {}
requestDictionary["requests"][0]["repeatCell"]["cell"]["userEnteredFormat"]["backgroundColor"] = {}
requestDictionary["requests"][0]["repeatCell"]["cell"]["userEnteredFormat"]["backgroundColor"]["red"] = 208/255
requestDictionary["requests"][0]["repeatCell"]["cell"]["userEnteredFormat"]["backgroundColor"]["green"] = 224/255
requestDictionary["requests"][0]["repeatCell"]["cell"]["userEnteredFormat"]["backgroundColor"]["blue"] = 227/255
requestDictionary["requests"][0]["repeatCell"]["fields"] = "userEnteredFormat(backgroundColor)"



print("Comment: Importing modules and setting up variables...Done. " + str(round(time.time() - startTime, 3)) + " seconds")

if activateKeyboard:

    with pynput.mouse.Listener(on_click=myPythonFunctions.functionOnClick) as listenerObj:
        print("Click on 'Clear' to begin posting...")
        listenerObj.join()




for row in currentSheetData[1:]:


    if myGoogleSheetsPythonLibrary.googleSheetsFunctions.isWhite(row["values"][0]) and myGoogleSheetsPythonLibrary.googleSheetsFunctions.hasFormattedValue(row["values"][0]):


        if row["values"][0]["formattedValue"] != "Enter/Edit" and activateKeyboard:

            # pprint(row)
            print("Row " + str("") + " will be populated into the Great Plains entry window.")

            if win32api.GetKeyState(win32con.VK_NUMLOCK) == 1:
                pyautogui.press("numlock")


            for col in range(0, 9):

                numberTabs = 1

                try:
                    string = str(row["values"][col]["formattedValue"])
                except:
                    string = ""


                if col == 0:

                    pyautogui.press(["down", "up", "up", "up"])

                    if string == "Enter Receipt":
                        pyautogui.press("down")


                elif col == 1:

                    pyautogui.press(["down", "up", "up", "up"])

                    if string == "Cash":
                        pyautogui.press("down")
                    elif string == "Increase Adjustment":
                        myPythonFunctions.repetitiveKeyPress(2, "down")
                    elif string == "Decrease Adjustment":
                        myPythonFunctions.repetitiveKeyPress(3, "down")


                elif col == 2:

                    # string = row["values"][col]["formattedValue"]
                    dateObj = datetime.datetime.strptime(string, "%m/%d/%Y")
                    # print(datetime.ParseExact(string, "yyMMdd", CultureInfo.InvariantCulture))
                    string = dateObj.strftime("%m%d%Y")


                elif col == 3:
                    numberTabs = 2

                elif col == 6:
                    numberTabs = 6


                elif col == 7:
                    string = string.replace("-", "")

                    if row["values"][0]["formattedValue"] != "Enter Transaction" or (row["values"][0]["formattedValue"] == "Enter Transaction" and row["values"][1]["formattedValue"] not in ["Check", "Decrease Adjustment"]):
                        numberTabs = 2


                if col in [6, 8]:

                    # if len(string.split(".")) == 1:
                    # string = string + "00"
                    string = string.lstrip("$").replace(".", "").replace(",", "")


                if col not in [0, 1]:

                    for letter in string:

                        if ord(letter) in (list(range(123, 127)) + list(range(94, 96)) + list(range(62, 91)) + [60, 58] + list(
                                range(40, 44)) + list(range(33, 39))):

                            pyautogui.PAUSE = .0000000000001
                            pyautogui.keyDown("shift")
                            pyautogui.press(letter)
                            pyautogui.keyUp("shift")
                            pyautogui.PAUSE = 0

                        else:
                            pyautogui.press(letter)


                myPythonFunctions.repetitiveKeyPress(numberTabs, "tab")


            if win32api.GetKeyState(win32con.VK_NUMLOCK) == 0:
                pyautogui.press("numlock")


            with pynput.mouse.Listener(on_click=myPythonFunctions.functionOnClick) as listenerObj:
                print("Click on 'Post' or 'Clear' to continue with this entry...")
                listenerObj.join()


    # requestDictionary["requests"][0]["repeatCell"]["range"]["startRowIndex"] = rowCount - 1
    # requestDictionary["requests"][0]["repeatCell"]["range"]["endRowIndex"] = rowCount

    # if changeCellColor:
    #     googleSheetsObj.batchUpdate(spreadsheetId=spreadsheetIDStr, body=requestDictionary).execute()








################################################################################################################


# for row in googleSheetValues:
#     row.insert(0, "Blank Space")

# googleSheetValues.insert(0, ["Blank Space"])



# requestDictionary2 = {
#     "requests": [
#         {
#             "repeatCell": {
#                 "range": {
#                     "sheetId": 0,
#                     "startRowIndex": 0,
#                     "endRowIndex": 1
#                 },
#                 "cell": {
#                     "userEnteredFormat": {
#                         "backgroundColor": {
#                             "red": 0.0,
#                             "green": 1.0,
#                             "blue": 0.0
#                         }
#                     }
#                 },
#                 "fields": "userEnteredFormat(backgroundColor)"
#             }
#         }
#     ]
# }
#
# print(str(requestDictionary2).replace("'", "\""))


#
# requestDictionary = {}
# print(requestDictionary)
#
# requestDictionary["requests"] = []
# print(requestDictionary)
#
# requestDictionary["requests"].append({})
# print(requestDictionary)
#
# requestDictionary["requests"][0]["updateSpreadsheetProperties"] = {}
# print(requestDictionary)
#
# requestDictionary["requests"][0]["updateSpreadsheetProperties"]["properties"] = {}
# print(requestDictionary)
#
# requestDictionary["requests"][0]["updateSpreadsheetProperties"]["properties"]["title"] = "this title is new"
# print(requestDictionary)
#
# requestDictionary["requests"][0]["updateSpreadsheetProperties"]["fields"] = "title"
# print(requestDictionary)

#
# requestDictionary = []
# print(requestDictionary)
#
#
# requestDictionary.append({
#     'updateSpreadsheetProperties': {
#         'properties': {
#             'title': "this title is new"
#         },
#         'fields': 'title'
#     }
# })
# print(requestDictionary)
#
#
# requestDictionary = {
#     'requests': requestDictionary
# }
# print(requestDictionary)
#
#




# pprint.pprint(googleSheetsObj)
# print("dir: ")
# pprint.pprint(dir(googleSheetsObj))
# print("help: ")
# pprint.pprint(help(googleSheetsObj))

# print("Creed's List: ")
# pprint.pprint([(name,type(getattr(googleSheetsObj, name))) for name in dir(googleSheetsObj)])
# print("An attribute: ")
# print(googleSheetsObj._baseUrl)
# print("A method: ")
# print(googleSheetsObj.values().get(spreadsheetId=spreadsheetIDStr, range=rangeName).execute())
# print("Another method: ")
# print(googleSheetsObj.batchUpdate(spreadsheetId=spreadsheetIDStr, body=requestDictionary).execute())