import sys
sys.path.append("..")
import pyautogui, datetime, creed_modules.creed_toolpack, pynput.mouse

# from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
googleScopes = ["https://www.googleapis.com/auth/spreadsheets"]

spreadsheetIDStr = "1uQezYVWkLZEvXzbprJPLRyDdyn04MdO-k6yaiyZPOx8"
rangeName = "Transfers"
credentialsPath = os.path.abspath(os.path.join(os.curdir, "..\\private_data\\post_journal_entries\\googleCredentials.json"))
tokenPath = os.path.abspath(os.path.join(os.curdir, "..\\private_data\\post_journal_entries\\googleToken.pickle"))

def main():

    credentialsObj = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.


    if os.path.exists(tokenPath):
        with open(tokenPath, "rb") as tokenObj:
            credentialsObj = pickle.load(tokenObj)

    # If there are no (valid) credentials available, let the user log in.

    if not credentialsObj or not credentialsObj.valid:
        if credentialsObj and credentialsObj.expired and credentialsObj.refresh_token:
            credentialsObj.refresh(Request())
        else:
            flowObj = InstalledAppFlow.from_client_secrets_file(credentialsPath, googleScopes)
            credentialsObj = flowObj.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tokenPath, "wb") as tokenObj:
            pickle.dump(credentialsObj, tokenObj)

    serviceObj = build("sheets", "v4", credentials=credentialsObj)

    # Call the Sheets API

    googleSheetsObj = serviceObj.spreadsheets()
    result = googleSheetsObj.values().get(spreadsheetId=spreadsheetIDStr, range=rangeName).execute()
    googleSheetCells = result.get("values", [])


    for row in range(1, len(googleSheetCells)):

        print("Row " + str(row) + " will be populated into the Great Plains entry window.")

        # creed_modules.creed_toolpack.repetitiveKeyPress(2, "tab")

        # for col in range(0, 5):
        #     numberTabs = 1
        #     string = googleSheetCells[row][col]
        #     print(string)



    requestDictionary = {}
    print(requestDictionary)

    requestDictionary["requests"] = []
    print(requestDictionary)

    requestDictionary["requests"].append({})
    print(requestDictionary)

    requestDictionary["requests"][0]["repeatCell"] = {}
    print(requestDictionary)

    requestDictionary["requests"][0]["repeatCell"]["range"] = {}
    print(requestDictionary)

    requestDictionary["requests"][0]["repeatCell"]["range"]["sheetId"] = 0
    # requestDictionary["requests"][0]["repeatCell"]["range"]["startRowIndex"] = 0
    requestDictionary["requests"][0]["repeatCell"]["range"]["endRowIndex"] = 1
    print(requestDictionary)

    requestDictionary["requests"][0]["repeatCell"]["cell"] = {}
    print(requestDictionary)

    requestDictionary["requests"][0]["repeatCell"]["cell"]["userEnteredFormat"] = {}
    print(requestDictionary)

    requestDictionary["requests"][0]["repeatCell"]["cell"]["userEnteredFormat"]["backgroundColor"] = {}
    print(requestDictionary)

    requestDictionary["requests"][0]["repeatCell"]["cell"]["userEnteredFormat"]["backgroundColor"]["red"] = 1.0
    # requestDictionary["requests"][0]["repeatCell"]["cell"]["userEnteredFormat"]["backgroundColor"]["green"] = 0.0
    # requestDictionary["requests"][0]["repeatCell"]["cell"]["userEnteredFormat"]["backgroundColor"]["blue"] = 0.0
    print(requestDictionary)

    requestDictionary["requests"][0]["repeatCell"]["fields"] = "userEnteredFormat(backgroundColor)"
    print(str(requestDictionary).replace("'", "\""))


    googleSheetsObj.batchUpdate(spreadsheetId=spreadsheetIDStr, body=requestDictionary).execute()






if __name__ == "__main__":
    main()







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