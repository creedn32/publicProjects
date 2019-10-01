print("Comment: Importing modules and setting up variables...")
import time
startTime = time.time()

#ID of public Google Sheet
# spreadsheetIDStr = "1uQezYVWkLZEvXzbprJPLRyDdyn04MdO-k6yaiyZPOx8"
#ID of private Google Sheet
spreadsheetIDStr = "1nR8wJISZjeJh6DCBf1OTpiG6rdY5DyyUtDI763axGhg"
# sheetName = "Bank Transactions"
sheetName = "Bank Transactions - Recurring"



import sys
sys.path.append("..")
from creed_modules import creedFunctions

from pprint import pprint
import pyautogui, datetime, pynput.mouse, win32api, win32con
import pickle, os.path, googleapiclient.discovery, google_auth_oauthlib.flow, google.auth.transport.requests



# If modifying these scopes, delete the file token.pickle.
changeCellColor = False
credentialsPath = os.path.abspath(os.path.join(os.curdir, "..\\private_data\\googleCredentials\\googleCredentials.json"))
tokenPath = os.path.abspath(os.path.join(os.curdir, "..\\private_data\\googleCredentials\\googleToken.pickle"))
googleScopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentialsObj = None
numLockChanged = False
pyautogui.PAUSE = 0


# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.


if os.path.exists(tokenPath):
    with open(tokenPath, "rb") as tokenObj:
        credentialsObj = pickle.load(tokenObj)

# If there are no (valid) credentials available, let the user log in.

if not credentialsObj or not credentialsObj.valid:
    if credentialsObj and credentialsObj.expired and credentialsObj.refresh_token:
        credentialsObj.refresh(google.auth.transport.requests.Request())
    else:
        flowObj = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(credentialsPath, googleScopes)
        credentialsObj = flowObj.run_local_server(port=0)
    # Save the credentials for the next run
    with open(tokenPath, "wb") as tokenObj:
        pickle.dump(credentialsObj, tokenObj)



googleSheetsObj = googleapiclient.discovery.build("sheets", "v4", credentials=credentialsObj).spreadsheets()
googleSheetsData = googleSheetsObj.get(spreadsheetId=spreadsheetIDStr, includeGridData=True).execute()
googleSheetsDictionary = {}

# print(str(googleSheetsData).replace("'", "\""))



for sheet in googleSheetsObj.get(spreadsheetId=spreadsheetIDStr).execute()["sheets"]:
    googleSheetsDictionary[sheet["properties"]["title"]] = sheet

googleSheetValues = googleSheetsObj.values().get(spreadsheetId=spreadsheetIDStr, range=sheetName).execute()["values"]



requestDictionary = {}
requestDictionary["requests"] = []
requestDictionary["requests"].append({})
requestDictionary["requests"][0]["repeatCell"] = {}
requestDictionary["requests"][0]["repeatCell"]["range"] = {}
requestDictionary["requests"][0]["repeatCell"]["range"]["sheetId"] = googleSheetsDictionary[sheetName]["properties"]["sheetId"]
requestDictionary["requests"][0]["repeatCell"]["range"]["startRowIndex"] = 0
requestDictionary["requests"][0]["repeatCell"]["range"]["endRowIndex"] = 0
requestDictionary["requests"][0]["repeatCell"]["cell"] = {}
requestDictionary["requests"][0]["repeatCell"]["cell"]["userEnteredFormat"] = {}
requestDictionary["requests"][0]["repeatCell"]["cell"]["userEnteredFormat"]["backgroundColor"] = {}
requestDictionary["requests"][0]["repeatCell"]["cell"]["userEnteredFormat"]["backgroundColor"]["red"] = 208/255
requestDictionary["requests"][0]["repeatCell"]["cell"]["userEnteredFormat"]["backgroundColor"]["green"] = 224/255
requestDictionary["requests"][0]["repeatCell"]["cell"]["userEnteredFormat"]["backgroundColor"]["blue"] = 227/255
requestDictionary["requests"][0]["repeatCell"]["fields"] = "userEnteredFormat(backgroundColor)"


if win32api.GetKeyState(win32con.VK_NUMLOCK) == 1:
    pyautogui.press("numlock")


print("Comment: Importing modules and setting up variables...Done. " + str(round(time.time() - startTime, 3)) + " seconds")


with pynput.mouse.Listener(on_click=creedFunctions.functionOnClick) as listenerObj:
    print("Click on 'Clear' to begin posting...")
    listenerObj.join()



# sys.exit()


for sheet in googleSheetsData["sheets"]:

    if sheet["properties"]["title"] == sheetName:

        rowCount = 1

        for row in sheet["data"][0]["rowData"]:

            # print(rowCount)

            if rowCount in range(2, len(googleSheetValues) + 1):

                # print("row: " + str(rowCount))

                try:
                    cellColorTotal = row["values"][0]["userEnteredFormat"]["backgroundColor"]["red"] + row["values"][0]["userEnteredFormat"]["backgroundColor"]["green"] + row["values"][0]["userEnteredFormat"]["backgroundColor"]["blue"]
                except KeyError:
                    cellColorTotal = 3

                if cellColorTotal == 3 and googleSheetValues[rowCount - 1][0] != "Enter/Edit":


                    # print("First cell in this row is white")
                    # time.sleep(1)


                    print("Row " + str(rowCount) + " will be populated into the Great Plains entry window.")


                    optionVar = googleSheetValues[rowCount - 1][1 - 1]
                    typeVar = googleSheetValues[rowCount - 1][2 - 1]

                    for col in range(1, 10):

                        numberTabs = 1
                        string = googleSheetValues[rowCount - 1][col - 1]


                        if col == 1:

                            pyautogui.press(["down", "up", "up", "up"])

                            if optionVar == "Enter Receipt":
                                pyautogui.press("down")

                        elif col == 2:

                            pyautogui.press(["down", "up", "up", "up"])

                            if typeVar == "Cash":
                                pyautogui.press("down")
                            elif typeVar == "Increase Adjustment":
                                creedFunctions.repetitiveKeyPress(2, "down")
                            elif typeVar == "Decrease Adjustment":
                                creedFunctions.repetitiveKeyPress(3, "down")


                        elif col == 3:
                            dateObj = datetime.datetime.strptime(string, "%m/%d/%Y")
                            string = dateObj.strftime("%m%d%Y")

                        elif col == 4:
                            numberTabs = 2

                        elif col == 7:
                            numberTabs = 6


                        elif col == 8:
                            string = string.replace("-", "")

                            if optionVar != "Enter Transaction" or (optionVar == "Enter Transaction" and typeVar not in ["Check", "Decrease Adjustment"]):
                                numberTabs = 2


                        if col in [7, 9]:

                            if len(string.split(".")) == 1:
                                string = string + "00"

                            string = string.lstrip("$").replace(".", "").replace(",", "")


                        if col not in [1, 2]:

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


                        creedFunctions.repetitiveKeyPress(numberTabs, "tab")


                    with pynput.mouse.Listener(on_click=creedFunctions.functionOnClick) as listenerObj:
                        print("Click on 'Post' or 'Clear' to continue with this entry...")
                        listenerObj.join()

                    requestDictionary["requests"][0]["repeatCell"]["range"]["startRowIndex"] = rowCount - 1
                    requestDictionary["requests"][0]["repeatCell"]["range"]["endRowIndex"] = rowCount

                    if changeCellColor:
                        googleSheetsObj.batchUpdate(spreadsheetId=spreadsheetIDStr, body=requestDictionary).execute()




            rowCount = rowCount + 1



if win32api.GetKeyState(win32con.VK_NUMLOCK) == 0:
    pyautogui.press("numlock")




# ################################################################################################################
#
#
# # for row in googleSheetValues:
# #     row.insert(0, "Blank Space")
#
# # googleSheetValues.insert(0, ["Blank Space"])
#
#
#
# # requestDictionary2 = {
# #     "requests": [
# #         {
# #             "repeatCell": {
# #                 "range": {
# #                     "sheetId": 0,
# #                     "startRowIndex": 0,
# #                     "endRowIndex": 1
# #                 },
# #                 "cell": {
# #                     "userEnteredFormat": {
# #                         "backgroundColor": {
# #                             "red": 0.0,
# #                             "green": 1.0,
# #                             "blue": 0.0
# #                         }
# #                     }
# #                 },
# #                 "fields": "userEnteredFormat(backgroundColor)"
# #             }
# #         }
# #     ]
# # }
# #
# # print(str(requestDictionary2).replace("'", "\""))
#
#
# #
# # requestDictionary = {}
# # print(requestDictionary)
# #
# # requestDictionary["requests"] = []
# # print(requestDictionary)
# #
# # requestDictionary["requests"].append({})
# # print(requestDictionary)
# #
# # requestDictionary["requests"][0]["updateSpreadsheetProperties"] = {}
# # print(requestDictionary)
# #
# # requestDictionary["requests"][0]["updateSpreadsheetProperties"]["properties"] = {}
# # print(requestDictionary)
# #
# # requestDictionary["requests"][0]["updateSpreadsheetProperties"]["properties"]["title"] = "this title is new"
# # print(requestDictionary)
# #
# # requestDictionary["requests"][0]["updateSpreadsheetProperties"]["fields"] = "title"
# # print(requestDictionary)
#
# #
# # requestDictionary = []
# # print(requestDictionary)
# #
# #
# # requestDictionary.append({
# #     'updateSpreadsheetProperties': {
# #         'properties': {
# #             'title': "this title is new"
# #         },
# #         'fields': 'title'
# #     }
# # })
# # print(requestDictionary)
# #
# #
# # requestDictionary = {
# #     'requests': requestDictionary
# # }
# # print(requestDictionary)
# #
# #
#
#
#
#
# # pprint.pprint(googleSheetsObj)
# # print("dir: ")
# # pprint.pprint(dir(googleSheetsObj))
# # print("help: ")
# # pprint.pprint(help(googleSheetsObj))
#
# # print("Creed's List: ")
# # pprint.pprint([(name,type(getattr(googleSheetsObj, name))) for name in dir(googleSheetsObj)])
# # print("An attribute: ")
# # print(googleSheetsObj._baseUrl)
# # print("A method: ")
# # print(googleSheetsObj.values().get(spreadsheetId=spreadsheetIDStr, range=rangeName).execute())
# # print("Another method: ")
# # print(googleSheetsObj.batchUpdate(spreadsheetId=spreadsheetIDStr, body=requestDictionary).execute())