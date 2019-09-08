function columnToLetter(column)
{
  var temp, letter = '';
  while (column > 0)
  {
    temp = (column - 1) % 26;
    letter = String.fromCharCode(temp + 65) + letter;
    column = (column - temp - 1) / 26;
  }
  return letter;
}

function letterToColumn(letter)
{
  var column = 0, length = letter.length;
  for (var i = 0; i < length; i++)
  {
    column += (letter.charCodeAt(i) - 64) * Math.pow(26, length - i - 1);
  }
  return column;
}




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
sheetToWrite = "v2"
firstRowToAppend = []

for cell in currentSheetValues[0]:
    firstRowToAppend.append(cell)

firstRowToAppend.append("Transaction Number")

valuesToWrite = []
valuesToWrite.append(firstRowToAppend)

transactionCount = 2
for rowCount in range(1, len(currentSheetValues)):
    if currentSheetValues[rowCount]:
        rowToAppend = []

        if currentSheetValues[rowCount][0] != "":
            currentDate = currentSheetValues[rowCount][0]

        rowToAppend.append(currentDate)

        for colCount in range(1, len(currentSheetValues[rowCount])):
            rowToAppend.append(currentSheetValues[rowCount][colCount])

        blankCellsToAdd = len(firstRowToAppend) - len(rowToAppend) - 1

        for cell in range(0, blankCellsToAdd):
            rowToAppend.append("")

        rowToAppend.append(transactionCount)
        valuesToWrite.append(rowToAppend)
    else:
        transactionCount = transactionCount + 1

# print(valuesToWrite)


bodyToWrite = {
    "values": valuesToWrite
}

googleSheetsObj.values().update(spreadsheetId=currentSpreadsheetID, range=sheetToWrite + "!A1", valueInputOption="RAW", body=bodyToWrite).execute()




currentSheetName = "v2"
# currentSheetValues = googleSheetsObj.values().get(spreadsheetId=currentSpreadsheetID, range=currentSheetName + "!A1").execute()
# print(currentSheetValues)

# sheetToWrite = "v3"
# firstRowToAppend = ["Account"]
#
# for cell in currentSheetValues[0]:
#     firstRowToAppend.append(cell)
#
# valuesToWrite = []
# valuesToWrite.append(firstRowToAppend)
#
# for rowCount in range(1, len(currentSheetValues)):
#     rowToAppend = [rowCount]
#     valuesToWrite.append(rowToAppend)
#
# #
# #     if currentSheetValues[rowCount]:
# #         rowToAppend = []
# #
# #         if currentSheetValues[rowCount][0] != "":
# #             currentDate = currentSheetValues[rowCount][0]
# #
# #         rowToAppend.append(currentDate)
# #
# #         for colCount in range(1, len(currentSheetValues[rowCount])):
# #             rowToAppend.append(currentSheetValues[rowCount][colCount])
# #
# #         blankCellsToAdd = len(firstRowToAppend) - len(rowToAppend) - 1
# #
# #         for cell in range(0, blankCellsToAdd):
# #             rowToAppend.append("")
# #
# #         rowToAppend.append(transactionCount)
# #         valuesToWrite.append(rowToAppend)
# #     else:
# #         transactionCount = transactionCount + 1
# #
# # print(valuesToWrite)
#
#
# # pprint(currentSheetValues)
#
# print(valuesToWrite)
# bodyToWrite = {
#     "values": valuesToWrite
# }

# googleSheetsObj.values().update(spreadsheetId=currentSpreadsheetID, range=sheetToWrite + "!A1", valueInputOption="RAW", body=bodyToWrite).execute()


