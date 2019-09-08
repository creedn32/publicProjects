print("Comment: Importing modules and setting up variables...")
import time
startTime = time.time()

import sys
sys.path.append("..")
from creed_modules import creedFunctions

from pprint import pprint
import pickle, os.path, googleapiclient.discovery, google_auth_oauthlib.flow, google.auth.transport.requests


credentialsPath = os.path.abspath(os.path.join(os.curdir, "..\\private_data\\googleSheetsTemplate\\googleCredentials.json"))
tokenPath = os.path.abspath(os.path.join(os.curdir, "..\\private_data\\googleSheetsTemplate\\googleToken.pickle"))
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

currentSpreadsheetID = "1T-DVnBRKYAsA1N_jqdKDMErav-PrrPBdLGS4wiLGCd4"

currentSpreadsheetData = googleSheetsObj.get(spreadsheetId=currentSpreadsheetID, includeGridData=True).execute()
currentSpreadsheetSheets = {}
for sheet in googleSheetsObj.get(spreadsheetId=currentSpreadsheetID).execute()["sheets"]:
    currentSpreadsheetSheets[sheet["properties"]["title"]] = sheet

print("Comment: Importing modules and setting up variables...Done. " + str(round(time.time() - startTime, 3)) + " seconds")


currentSheetName = "Original"
currentSheetValues = googleSheetsObj.values().get(spreadsheetId=currentSpreadsheetID, range=currentSheetName).execute()["values"]

for row in currentSheetValues:
    for cell in row:
        print(cell)
