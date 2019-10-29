import sys, pathlib
sys.path.append(str(pathlib.Path.cwd().parents[1]))
sys.path.append(str(pathlib.Path.cwd().parents[0]))
from creedLibrary import creedFunctions

startTime = creedFunctions.startCode()
import googleSheetsAuthenticate


import time
from pprint import pprint
# import lumpy
# pprint(sys.path)



def getLastCell(currentData, currentSheet):

    for sheet in currentData["sheets"]:

        if sheet["properties"]["title"] == currentSheet:

            totalRows = len(sheet["data"][0]["rowData"])
            totalColumnsByRow = []

            for row in sheet["data"][0]["rowData"]:
                totalColumnsByRow.append(len(row.get("values", [])))

    return creedFunctions.columnToLetter(max(totalColumnsByRow)) + str(totalRows)



def convertNumber(num):
    # try:
        num = creedFunctions.convertEmptyStrToZero(num)
        num = creedFunctions.removeCommaFromStr(num)
        num = float(num)
        return num
    # except BaseException as e:
        print("Error on " + num + " " + str(e))



def beginOps(currentSheet, nextSheet, firstRow):

    print("Comment: Creating " + nextSheet + " sheet...")
    indexFirstRowOfData = 1
    sheetInfo["startTime"] = time.time()

    # if not sheetInfo[currentSheet]["lastCell"]:
    #     currentSpreadsheetData = sheetInfo["googleSheetsObj"].get(spreadsheetId=sheetInfo["currentSpreadsheetID"], includeGridData=True).execute()
    #     currentEndRange = getLastCell(currentSpreadsheetData, sheetInfo[currentSheet]["name"])
    # else:
    #     currentEndRange = sheetInfo[currentSheet]["lastCell"]


    rangeToClear = sheetInfo[nextSheet]["name"] + "!" + sheetInfo["allSheetsBegRange"] + ":" + sheetInfo[nextSheet]["lastCell"]
    sheetInfo["googleSheetsObj"].values().clear(spreadsheetId=sheetInfo["currentSpreadsheetID"], range=rangeToClear, body={}).execute()

    rangeToDownload = sheetInfo[currentSheet]["name"] + "!" + sheetInfo["allSheetsBegRange"] + ":" + sheetInfo[currentSheet]["lastCell"]
    sheetInfo[currentSheet]["obj"] = sheetInfo["googleSheetsObj"].values().get(spreadsheetId=sheetInfo["currentSpreadsheetID"], range=rangeToDownload).execute()
    sheetInfo[currentSheet]["values"] = sheetInfo[currentSheet]["obj"].get("values", [])
    sheetInfo[currentSheet]["shortValues"] = sheetInfo[currentSheet]["values"][indexFirstRowOfData:]


    for row in sheetInfo[currentSheet]["shortValues"]:

        if len(row) < 11 and len(row) > 1:

            columnsToAdd = 11 - len(row)

            for i in range(columnsToAdd):
                row.append("")

    firstRowToWrite = firstRow

    for cell in sheetInfo[currentSheet]["values"][indexFirstRowOfData - 1]:
        firstRowToWrite.append(cell)

    return [firstRowToWrite]




def endOps(nextSt, vToWrite):

    bodyToWrite = {
        "values": vToWrite
    }

    rangeToWrite = sheetInfo[nextSt]["name"] + "!" + sheetInfo["allSheetsBegRange"]
    sheetInfo["googleSheetsObj"].values().update(spreadsheetId=sheetInfo["currentSpreadsheetID"], range=rangeToWrite, valueInputOption="USER_ENTERED", body=bodyToWrite).execute()
    print("Comment: Creating " + nextSt + " sheet...Done. " + str(round(time.time() - sheetInfo["startTime"], 3)) + " seconds")





sheetInfo = {
    startTime: None,
    "googleSheetsObj": googleSheetsAuthenticate.authFunc(),
    "currentSpreadsheetID": "1T-DVnBRKYAsA1N_jqdKDMErav-PrrPBdLGS4wiLGCd4",
    "allSheetsBegRange": "A1",
    "first":
        {"name": "firstSheetTest",
         "lastCell": "K17"},
    "second":
        {"name": "secondSheetTest",
         "lastCell": "L13",
         "create?": True,
         "transIndex": 0,
         "accountIndex": 2,
         "amountIndex": 5,
         "debitIndex": 3,
         "creditIndex": 4},
    "third":
        {"name": "thirdSheetTest",
         "create?": True,
         "lastCell": "N21"}
}

# sheetInfo = {
#     originalLastCell: "K29278",
#     v2LastCell: "L19585",
# }



# currentSpreadsheetSheets = {}
# # for sheet in sheetInfo["googleSheetsObj"].get(spreadsheetId=sheetInfo["currentSpreadsheetID"]).execute()["sheets"]:
# #     currentSpreadsheetSheets[sheet["properties"]["title"]] = sheet



print("Comment: Importing modules and setting up variables...Done. " + str(round(time.time() - startTime, 3)) + " seconds")



if sheetInfo["second"]["create?"]:

    currentSheet = "first"
    nextSheet = "second"
    valToWrite = beginOps(currentSheet, nextSheet, ["Transaction Number"])
    dataToFillDown = {0: "", 6: "", 7: "", 8: "", 9: "", 10: ""}
    transactionNum = 1


    for rowFromCurrentSheet in sheetInfo[currentSheet]["shortValues"]:

        if rowFromCurrentSheet:

            for key in dataToFillDown:
                if rowFromCurrentSheet[key] != "":
                   dataToFillDown[key] = rowFromCurrentSheet[key]

            rowToWrite = [transactionNum]

            for index in range(len(rowFromCurrentSheet)):
                if index in dataToFillDown.keys():
                    rowToWrite.append(dataToFillDown[index])
                else:
                    rowToWrite.append(rowFromCurrentSheet[index])

            valToWrite.append(rowToWrite)

        else:
            transactionNum = transactionNum + 1
            dataToFillDown = {0: "", 6: "", 7: "", 8: "", 9: "", 10: ""}

    endOps("second", valToWrite)



if sheetInfo["third"]["create?"]:

    currentSheet = "second"
    valToWrite = beginOps(currentSheet, "third", ["Main Account", "Amount+-"])

    accountList = []

    for row in sheetInfo[currentSheet]["shortValues"]:
        if row[sheetInfo["second"]["accountIndex"]] not in accountList:
            accountList.append(row[sheetInfo["second"]["accountIndex"]])


    for currentAccount in accountList:

        transactionList = []

        for row in sheetInfo[currentSheet]["shortValues"]:
            if row[sheetInfo["second"]["accountIndex"]] == currentAccount and row[sheetInfo["second"]["transIndex"]] not in transactionList:
                transactionList.append(row[sheetInfo["second"]["transIndex"]])

        for currentTrans in transactionList:

            for row in sheetInfo[currentSheet]["shortValues"]:

                if row[sheetInfo["second"]["transIndex"]] == currentTrans:

                    if row[sheetInfo["second"]["accountIndex"]] != currentAccount:

                        row[sheetInfo["second"]["amountIndex"]] = convertNumber(row[sheetInfo["second"]["amountIndex"]])
                        row[sheetInfo["second"]["debitIndex"]] = convertNumber(row[sheetInfo["second"]["debitIndex"]])
                        row[sheetInfo["second"]["creditIndex"]] = convertNumber(row[sheetInfo["second"]["creditIndex"]])

                        valToWrite.append([currentAccount, -row[sheetInfo["second"]["debitIndex"]] + row[sheetInfo["second"]["creditIndex"]]] + row)


    endOps("third", valToWrite)

