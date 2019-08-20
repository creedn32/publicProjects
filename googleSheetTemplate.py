print("Comment: Importing modules and setting up variables...")
import time
startTime = time.time()

import sys
sys.path.append("..")


from creed_modules import creed_toolpack
import pickle, os.path, googleapiclient.discovery, google_auth_oauthlib.flow, google.auth.transport.requests


#ID of public Google Sheet
spreadsheetIDStr = "1uQezYVWkLZEvXzbprJPLRyDdyn04MdO-k6yaiyZPOx8"
#ID of private Google Sheet
# spreadsheetIDStr = "1nR8wJISZjeJh6DCBf1OTpiG6rdY5DyyUtDI763axGhg"


sheetName = "Bank Transfers"
credentialsPath = os.path.abspath(os.path.join(os.curdir, "..\\private_data\\googleCredentials\\googleCredentials.json"))
tokenPath = os.path.abspath(os.path.join(os.curdir, "..\\private_data\\googleCredentials\\googleToken.pickle"))
googleScopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentialsObj = None



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


# googleSheetsDictionary = {}
# for sheet in googleSheetsObj.get(spreadsheetId=spreadsheetIDStr).execute()["sheets"]:
#     googleSheetsDictionary[sheet["properties"]["title"]] = sheet

googleSheetValues = googleSheetsObj.values().get(spreadsheetId=spreadsheetIDStr, range=sheetName).execute()["values"]



print("Comment: Importing modules and setting up variables...Done. " + str(round(time.time() - startTime, 3)) + " seconds")




for sheet in googleSheetsData["sheets"]:

    if sheet["properties"]["title"] == sheetName:

        rowCount = 1

        for row in sheet["data"][0]["rowData"]:

            # print(rowCount)

            if rowCount in range(2, len(googleSheetValues) + 1):

                print("row: " + str(rowCount))

            rowCount = rowCount + 1
