print("Comment: Importing modules and setting up variables...")
import time
startTime = time.time()

import sys
sys.path.append("..")
from creed_modules import creedFunctions

from pprint import pprint
import pickle, os.path, googleapiclient.discovery, google_auth_oauthlib.flow, google.auth.transport.requests


def getLastCell(currentData, currentSheet):

    for sheet in currentData["sheets"]:

        if sheet["properties"]["title"] == currentSheet:

            totalRows = len(sheet["data"][0]["rowData"])
            totalColumnsByRow = []

            for row in sheet["data"][0]["rowData"]:
                totalColumnsByRow.append(len(row.get("values", [])))


    return creedFunctions.columnToLetter(max(totalColumnsByRow)) + str(totalRows)



def filterFunc(element):
    pass
#     if



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

# currentSpreadsheetSheets = {}
# for sheet in googleSheetsObj.get(spreadsheetId=currentSpreadsheetID).execute()["sheets"]:
#     currentSpreadsheetSheets[sheet["properties"]["title"]] = sheet

print("Comment: Importing modules and setting up variables...Done. " + str(round(time.time() - startTime, 3)) + " seconds")



currentSpreadsheetData = googleSheetsObj.get(spreadsheetId=currentSpreadsheetID, includeGridData=True).execute()
currentSheetName = "Original"
currentBegRange = "A1"
currentEndRange = getLastCell(currentSpreadsheetData, currentSheetName)


currentSheetValues = googleSheetsObj.values().get(spreadsheetId=currentSpreadsheetID, range=currentSheetName + "!" + currentBegRange + ":" + currentEndRange).execute()["values"]
sheetToWrite = "v2"
firstRowToAppend = []

for cell in currentSheetValues[0]:
    firstRowToAppend.append(cell)

firstRowToAppend.insert(0, "Transaction Number")

valuesToWrite = []
valuesToWrite.append(firstRowToAppend)


transactionCount = 2
for rowCount in range(1, len(currentSheetValues)):
    if currentSheetValues[rowCount]:
        rowToAppend = []

        rowToAppend.append(transactionCount)

        if currentSheetValues[rowCount][0] != "":
            currentDate = currentSheetValues[rowCount][0]

        rowToAppend.append(currentDate)

        for colCount in range(1, len(currentSheetValues[rowCount])):
            rowToAppend.append(currentSheetValues[rowCount][colCount])

        blankCellsToAdd = len(firstRowToAppend) - len(rowToAppend) - 1

        for cell in range(0, blankCellsToAdd):
            rowToAppend.append("")

        valuesToWrite.append(rowToAppend)

    else:

        transactionCount = transactionCount + 1

# print(valuesToWrite)


bodyToWrite = {
    "values": valuesToWrite
}

googleSheetsObj.values().update(spreadsheetId=currentSpreadsheetID, range=sheetToWrite + "!A1", valueInputOption="RAW", body=bodyToWrite).execute()



currentSpreadsheetData = googleSheetsObj.get(spreadsheetId=currentSpreadsheetID, includeGridData=True).execute()
currentSheetName = "v2"
currentBegRange = "A1"
currentEndRange = getLastCell(currentSpreadsheetData, currentSheetName)


currentSheetValues = googleSheetsObj.values().get(spreadsheetId=currentSpreadsheetID, range=currentSheetName + "!" + currentBegRange + ":" + currentEndRange).execute()["values"]
sheetToWrite = "v3"
firstRowToAppend = ["Account"]


for cell in currentSheetValues[0]:
    firstRowToAppend.append(cell)

valuesToWrite = []
valuesToWrite.append(firstRowToAppend)


accountList = []

for rowCount in range(1, len(currentSheetValues)):
    accountList.append(currentSheetValues[rowCount][2])


accountList = list(dict.fromkeys(accountList))



for row in currentSheetValues:
    currentTransaction = row[0]
    print(currentTransaction)



for acc in accountList:
    rowToAppend = []
    rowToAppend.append(acc)
    valuesToWrite.append(rowToAppend)


# print(valuesToWrite)



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



bodyToWrite = {
    "values": valuesToWrite
}

googleSheetsObj.values().update(spreadsheetId=currentSpreadsheetID, range=sheetToWrite + "!A1", valueInputOption="RAW", body=bodyToWrite).execute()





