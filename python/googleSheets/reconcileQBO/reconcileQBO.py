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


    if not sheetInfo[currentSheet]["lastCell"]:
        currentSpreadsheetData = googleSheetsObj.get(spreadsheetId=sheetInfo["currentSpreadsheetID"], includeGridData=True).execute()
        currentEndRange = getLastCell(currentSpreadsheetData, sheetInfo[currentSheet]["name"])
    else:
        currentEndRange = sheetInfo[currentSheet]["lastCell"]
        

    sheetInfo[currentSheet]["obj"] = googleSheetsObj.values().get(spreadsheetId=sheetInfo["currentSpreadsheetID"], range=sheetInfo[currentSheet]["name"] + "!" + sheetInfo["allSheetsBegRange"] + ":" + currentEndRange).execute()
    sheetInfo[currentSheet]["values"] = sheetInfo[currentSheet]["obj"].get("values", [])
    sheetInfo[currentSheet]["shortValues"] = sheetInfo[currentSheet]["values"][indexFirstRowOfData:]

    firstRowToWrite = firstRow

    for cell in sheetInfo[currentSheet]["values"][indexFirstRowOfData - 1]:
        firstRowToWrite.append(cell)

    return [firstRowToWrite]




def endOps(nextSt, vToWrite):

    bodyToWrite = {
        "values": vToWrite
    }

    googleSheetsObj.values().update(spreadsheetId=sheetInfo["currentSpreadsheetID"], range=sheetInfo[nextSt]["name"] + "!" + sheetInfo["allSheetsBegRange"], valueInputOption="USER_ENTERED", body=bodyToWrite).execute()
    print("Comment: Creating " + nextSt + " sheet...Done. " + str(round(time.time() - sheetInfo["startTime"], 3)) + " seconds")





googleSheetsObj = googleSheetsAuthenticate.authFunc()

sheetInfo = {
    startTime: None,
    "currentSpreadsheetID": "1T-DVnBRKYAsA1N_jqdKDMErav-PrrPBdLGS4wiLGCd4",
    "allSheetsBegRange": "A1",
    "first":
        {"name": "firstSheetTest",
         "lastCell": "K17"},
    "second":
        {"name": "secondSheetTest",
         "lastCell": "L13",
         "create?": True},
    "third":
        {"name": "thirdSheetTest",
         "create?": True}
}

# sheetInfo = {
#     originalLastCell: "K29278",
#     v2LastCell: "L19585",
# }





# currentSpreadsheetSheets = {}
# # for sheet in googleSheetsObj.get(spreadsheetId=sheetInfo["currentSpreadsheetID"]).execute()["sheets"]:
# #     currentSpreadsheetSheets[sheet["properties"]["title"]] = sheet
#
#



print("Comment: Importing modules and setting up variables...Done. " + str(round(time.time() - startTime, 3)) + " seconds")




if sheetInfo["second"]["create?"]:

    currentSheet = "first"
    valToWrite = beginOps(currentSheet, "second", ["Transaction Number"])
    lastColForFillDown = 6
    dataToFillDown = {0: "", 1: "", 2: "", 3: "", 4: "", 5: ""}
    transactionNum = 1

    # pprint(sheetInfo[currentSheet]["shortValues"])

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
            dataToFillDown = {0: "", 1: "", 2: "", 3: "", 4: "", 5: ""}

    endOps("second", valToWrite)



if sheetInfo["third"]["create?"]:

    currentSheet = "second"
    valToWrite = beginOps(currentSheet, "third", ["Main Account", "Amount+-"])

    currentTransIndex = 0
    currentAccountIndex = 8
    currentAmountIndex = currentAccountIndex + 1
    currentDebitIndex = currentAccountIndex + 2
    currentCreditIndex = currentAccountIndex + 3
    accountList = []

    for row in sheetInfo[currentSheet]["shortValues"]:
        if row[currentAccountIndex] not in accountList:
            accountList.append(row[currentAccountIndex])

    # accountList = list(dict.fromkeys(accountList))


    for currentAccount in accountList:

        # print(accountList)

        transactionList = []

        for row in sheetInfo[currentSheet]["shortValues"]:
            if row[currentAccountIndex] == currentAccount and row[currentTransIndex] not in transactionList:
                transactionList.append(row[currentTransIndex])

        # transactionList = list(dict.fromkeys(transactionList))


        for currentTrans in transactionList:

            for row in sheetInfo[currentSheet]["shortValues"]:
                if row[currentTransIndex] == currentTrans and row[currentAccountIndex] != currentAccount:

                    row[currentAmountIndex] = convertNumber(row[currentAmountIndex])
                    row[currentDebitIndex] = convertNumber(row[currentDebitIndex])

                    if len(row) > currentCreditIndex:
                        row[currentCreditIndex] = convertNumber(row[currentCreditIndex])
                    else:
                        row.append(0)

                    valToWrite.append([currentAccount, -row[currentDebitIndex] + row[currentCreditIndex]] + row)


    endOps("third", valToWrite)

