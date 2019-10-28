print("Comment: Importing modules and setting up variables...")

import sys, pathlib, time
startTime = time.time()
# print(pathlib.Path.cwd().parents[0])
sys.path.append(str(pathlib.Path.cwd().parents[1]))
sys.path.append(str(pathlib.Path.cwd().parents[0]))


from creedLibrary import creedFunctions
import googleSheetsAuthenticate
from pprint import pprint
# import lumpy
pprint(sys.path)

# for p in sys.path:
#     print(p)


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


def prepareSheet(sht):

    startTime = time.time()
    print("Comment: Creating " + sht + " sheet...")




settingsObj = {
    "firstSheet": "firstSheetTest",
    "secondSheet": "secondSheetTest",
    "thirdSheet": "thirdSheetTest",
    "firstSheetLastCell": "K12",
    "secondSheetLastCell": "L9"
}

# settingsObj = {
#     originalLastCell: "K29278",
#     v2LastCell: "L19585",
# }



googleSheetsObj = googleSheetsAuthenticate.authFunc()
currentSpreadsheetID = "1T-DVnBRKYAsA1N_jqdKDMErav-PrrPBdLGS4wiLGCd4"
indexFirstRowOfData = 1
copyToSecondSheet = True
copyToThirdSheet = True



# currentSpreadsheetSheets = {}
# # for sheet in googleSheetsObj.get(spreadsheetId=currentSpreadsheetID).execute()["sheets"]:
# #     currentSpreadsheetSheets[sheet["properties"]["title"]] = sheet
#
#



print("Comment: Importing modules and setting up variables...Done. " + str(round(time.time() - startTime, 3)) + " seconds")


if copyToSecondSheet:

    prepareSheet("second")

    currentSheetName = settingsObj["firstSheet"]
    sheetToWrite = settingsObj["secondSheet"]
    currentBegRange = "A1"

    if not settingsObj["firstSheetLastCell"]:
        currentSpreadsheetData = googleSheetsObj.get(spreadsheetId=currentSpreadsheetID, includeGridData=True).execute()
        currentEndRange = getLastCell(currentSpreadsheetData, currentSheetName)
    else:
        currentEndRange = settingsObj["firstSheetLastCell"]


    currentSheetObj = googleSheetsObj.values().get(spreadsheetId=currentSpreadsheetID, range=currentSheetName + "!" + currentBegRange + ":" + currentEndRange).execute()
    currentSheetValues = currentSheetObj.get("values", [])
    firstRowToAppend = []

    pprint(currentSheetValues)

    for cell in currentSheetValues[indexFirstRowOfData - 1]:
        firstRowToAppend.append(cell)

    firstRowToAppend.insert(0, "Transaction Number")

    valuesToWrite = []
    valuesToWrite.append(firstRowToAppend)

    lastColForFillDown = 6
    currentData = {0: "", 1: "", 2: "", 3: "", 4: "", 5: ""}
    transactionNum = 1

    for row in currentSheetValues[indexFirstRowOfData:]:

        if row:
            rowToAppend = []
            rowToAppend.append(transactionNum)

            for colNum in range(0, lastColForFillDown):
                if row[colNum] != "":
                   currentData[colNum] = row[colNum]

            # print(currentData)

            for key in currentData:
                rowToAppend.append(currentData[key])


            for index, col in enumerate(row[lastColForFillDown:]):
                rowToAppend.append(col)

            valuesToWrite.append(rowToAppend)

        else:
            transactionNum = transactionNum + 1
            currentData = {0: "", 1: "", 2: "", 3: "", 4: "", 5: ""}



    bodyToWrite = {
        "values": valuesToWrite
    }

    googleSheetsObj.values().update(spreadsheetId=currentSpreadsheetID, range=sheetToWrite + "!A1", valueInputOption="USER_ENTERED", body=bodyToWrite).execute()


    print("Comment: Creating v2 sheet...Done. " + str(round(time.time() - startTime, 3)) + " seconds")


if copyToThirdSheet:

    startTime = time.time()
    print("Comment: Creating v3 sheet...")

    currentSheetName = settingsObj["secondSheet"]
    sheetToWrite = settingsObj["thirdSheet"]
    currentBegRange = "A1"

    if not settingsObj["secondSheetLastCell"]:
        currentSpreadsheetData = googleSheetsObj.get(spreadsheetId=currentSpreadsheetID, includeGridData=True).execute()
        currentEndRange = getLastCell(currentSpreadsheetData, currentSheetName)
    else:
        currentEndRange = settingsObj["secondSheetLastCell"]


    currentSheetObj = googleSheetsObj.values().get(spreadsheetId=currentSpreadsheetID, range=currentSheetName + "!" + currentBegRange + ":" + currentEndRange).execute()
    currentSheetValues = currentSheetObj.get("values", [])
    currentTransIndex = 0
    currentAccountIndex = 8
    currentAmountIndex = currentAccountIndex + 1
    currentDebitIndex = currentAccountIndex + 2
    currentCreditIndex = currentAccountIndex + 3
    firstRowToAppend = ["Main Account", "Amount+-"]
    accountList = []

    for cell in currentSheetValues[indexFirstRowOfData - 1]:
        firstRowToAppend.append(cell)

    valuesToWrite = []
    valuesToWrite.append(firstRowToAppend)


    if not accountList:

        for row in currentSheetValues[indexFirstRowOfData:]:
            accountList.append(row[currentAccountIndex])

        accountList = list(dict.fromkeys(accountList))



    for currentAccount in accountList:

        # print(accountList)

        transactionList = []

        for row in currentSheetValues[indexFirstRowOfData:]:
            if row[currentAccountIndex] == currentAccount:
                transactionList.append(row[currentTransIndex])

        transactionList = list(dict.fromkeys(transactionList))


        for currentTrans in transactionList:

            for row in currentSheetValues[indexFirstRowOfData:]:
                if row[currentTransIndex] == currentTrans and row[currentAccountIndex] != currentAccount:

                    # print(row)

                    convertedNumbers = {
                        currentAmountIndex: convertNumber(row[currentAmountIndex]),
                        currentDebitIndex: convertNumber(row[currentDebitIndex]),
                        currentCreditIndex: convertNumber(creedFunctions.convertOutOfRangeToZero(row, currentCreditIndex))
                    }


                    rowToAppend = [currentAccount, -convertedNumbers[currentDebitIndex] + convertedNumbers[currentCreditIndex]]

                    for index, col in enumerate(row):
                        if index in convertedNumbers.keys():
                            rowToAppend.append(convertedNumbers[index])
                        else:
                            rowToAppend.append(col)

                    valuesToWrite.append(rowToAppend)

                    # fileForPrintObj = open(os.path.abspath(os.path.join(os.curdir, "..\\private_data\\reconcileQBO\\fileForPrint")), 'w+')
                    # fileForPrintObj.write(str(rowToAppend))
                    # fileForPrintObj.close()


    bodyToWrite = {
        "values": valuesToWrite
    }

    googleSheetsObj.values().update(spreadsheetId=currentSpreadsheetID, range=sheetToWrite + "!A1", valueInputOption="USER_ENTERED", body=bodyToWrite).execute()


    print("Comment: Creating v3 sheet...Done. " + str(round(time.time() - startTime, 3)) + " seconds")

