print("Comment: Importing modules and setting up variables...")
import time
startTime = time.time()




import sys
sys.path.append("..")


# from pprint import pprint
from creed_modules import creed_toolpack
import pyautogui, datetime, pynput.mouse


import pickle, os.path, googleapiclient.discovery, google_auth_oauthlib.flow, google.auth.transport.requests


#ID of public Google Sheet
spreadsheetIDStr = "1uQezYVWkLZEvXzbprJPLRyDdyn04MdO-k6yaiyZPOx8"
#ID of private Google Sheet
# spreadsheetIDStr = "1nR8wJISZjeJh6DCBf1OTpiG6rdY5DyyUtDI763axGhg"


changeCellColor = False
sheetName = "Bank Transfers"
credentialsPath = os.path.abspath(os.path.join(os.curdir, "..\\private_data\\googleCredentials\\googleCredentials.json"))
tokenPath = os.path.abspath(os.path.join(os.curdir, "..\\private_data\\googleCredentials\\googleToken.pickle"))
googleScopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentialsObj = None
pyautogui.PAUSE = 0



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


print("Comment: Importing modules and setting up variables...Done. " + str(round(time.time() - startTime, 3)) + " seconds")


with pynput.mouse.Listener(on_click=creed_toolpack.functionOnClick) as listenerObj:
    print("Click on 'Clear' to begin posting...")
    listenerObj.join()




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


                if cellColorTotal == 3:

                    # print("First cell in this row is white")
                    # time.sleep(1)

                    print("Row " + str(rowCount) + " will be populated into the Great Plains entry window.")

                    creed_toolpack.repetitiveKeyPress(2, "tab")

                    for col in range(1, 6):

                        numberTabs = 1
                        string = googleSheetValues[rowCount - 1][col - 1]


                        if col == 1:
                            dateObj = datetime.datetime.strptime(string, "%m/%d/%Y")
                            # print(dateObj.strftime('%m').lstrip('0'))
                            # print(dateObj.strftime('%m'))
                            # print(dateObj.strftime('%d').lstrip('0'))
                            # print(dateObj.strftime('%d'))
                            # print(dateObj.strftime('%Y'))

                            string = dateObj.strftime("%m%d%Y")

                        elif col == 3:
                            numberTabs = 2

                        elif col == 4:

                            if len(string.split(".")) == 1:
                                string = string + "00"

                            string = string.lstrip("$").replace(".", "").replace(",", "")


                        for letter in string:

                            if ord(letter) in (
                                    list(range(123, 127)) + list(range(94, 96)) + list(range(62, 91)) + [60, 58] + list(
                                    range(40, 44)) + list(range(33, 39))):

                                pyautogui.PAUSE = .0000000000001
                                pyautogui.keyDown("shift")
                                pyautogui.press(letter)
                                pyautogui.keyUp("shift")
                                pyautogui.PAUSE = 0

                            else:
                                pyautogui.press(letter)


                        creed_toolpack.repetitiveKeyPress(numberTabs, "tab")



                    with pynput.mouse.Listener(on_click=creed_toolpack.functionOnClick) as listenerObj:
                        print("Click on 'Post' or 'Clear' to continue with this entry...")
                        listenerObj.join()

                    requestDictionary["requests"][0]["repeatCell"]["range"]["startRowIndex"] = rowCount - 1
                    requestDictionary["requests"][0]["repeatCell"]["range"]["endRowIndex"] = rowCount

                    if changeCellColor:
                        googleSheetsObj.batchUpdate(spreadsheetId=spreadsheetIDStr, body=requestDictionary).execute()


            rowCount = rowCount + 1
