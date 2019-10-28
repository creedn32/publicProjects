print("Comment: Importing modules and setting up variables...")
import sys, pathlib, time
mDataObj = {"startTime": time.time()}
sys.path.append(str(pathlib.Path.cwd().parents[1]))
sys.path.append(str(pathlib.Path.cwd().parents[0]))


from creedLibrary import creedFunctions
import googleSheetsAuthenticate
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
    mDataObj["startTime"] = time.time()
    currentSheetName = sheetInfo[currentSheet]["name"]
    mDataObj["nextSheetName"] = sheetInfo[nextSheet]["name"]

    if not sheetInfo[currentSheet]["lastCell"]:
        currentSpreadsheetData = googleSheetsObj.get(spreadsheetId=currentSpreadsheetID, includeGridData=True).execute()
        mDataObj["currentEndRange"] = getLastCell(currentSpreadsheetData, currentSheetName)
    else:
        mDataObj["currentEndRange"] = sheetInfo[currentSheet]["lastCell"]
        

    mDataObj["currentSheetObj"] = googleSheetsObj.values().get(spreadsheetId=currentSpreadsheetID, range=currentSheetName + "!" + sheetInfo["allSheetsBegRange"] + ":" + mDataObj["currentEndRange"]).execute()
    mDataObj["currentSheetValues"] = mDataObj["currentSheetObj"].get("values", [])

    firstRowToAppend = firstRow

    for cell in mDataObj["currentSheetValues"][indexFirstRowOfData - 1]:
        firstRowToAppend.append(cell)

    mDataObj["valuesToWrite"] = []
    mDataObj["valuesToWrite"].append(firstRowToAppend)




def endOps(nextSt):

    bodyToWrite = {
        "values": mDataObj["valuesToWrite"]
    }

    googleSheetsObj.values().update(spreadsheetId=currentSpreadsheetID, range=sheetInfo[nextSt]["name"] + "!" + sheetInfo["allSheetsBegRange"], valueInputOption="USER_ENTERED", body=bodyToWrite).execute()
    print("Comment: Creating " + nextSt + " sheet...Done. " + str(round(time.time() - mDataObj["startTime"], 3)) + " seconds")





googleSheetsObj = googleSheetsAuthenticate.authFunc()
currentSpreadsheetID = "1T-DVnBRKYAsA1N_jqdKDMErav-PrrPBdLGS4wiLGCd4"
indexFirstRowOfData = 1
copyToSecondSheet = True
copyToThirdSheet = True




sheetInfo = {
    "allSheetsBegRange": "A1",
    "first":
        {"name": "firstSheetTest",
         "lastCell": "K12"},
    "second":
        {"name": "secondSheetTest",
         "lastCell": "L9"},
    "third":
        {"name": "thirdSheetTest"}
}

# sheetInfo = {
#     originalLastCell: "K29278",
#     v2LastCell: "L19585",
# }




# currentSpreadsheetSheets = {}
# # for sheet in googleSheetsObj.get(spreadsheetId=currentSpreadsheetID).execute()["sheets"]:
# #     currentSpreadsheetSheets[sheet["properties"]["title"]] = sheet
#
#



print("Comment: Importing modules and setting up variables...Done. " + str(round(time.time() - mDataObj["startTime"], 3)) + " seconds")


if copyToSecondSheet:

    beginOps("first", "second", ["Transaction Number"])

    lastColForFillDown = 6
    currentData = {0: "", 1: "", 2: "", 3: "", 4: "", 5: ""}
    transactionNum = 1

    for row in mDataObj["currentSheetValues"][indexFirstRowOfData:]:

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

            mDataObj["valuesToWrite"].append(rowToAppend)

        else:
            transactionNum = transactionNum + 1
            currentData = {0: "", 1: "", 2: "", 3: "", 4: "", 5: ""}

    endOps("second")


if copyToThirdSheet:

    beginOps("second", "third", ["Main Account", "Amount+-"])


    currentTransIndex = 0
    currentAccountIndex = 8
    currentAmountIndex = currentAccountIndex + 1
    currentDebitIndex = currentAccountIndex + 2
    currentCreditIndex = currentAccountIndex + 3
    accountList = []


    if not accountList:

        for row in mDataObj["currentSheetValues"][indexFirstRowOfData:]:
            accountList.append(row[currentAccountIndex])

        accountList = list(dict.fromkeys(accountList))



    for currentAccount in accountList:

        # print(accountList)

        transactionList = []

        for row in mDataObj["currentSheetValues"][indexFirstRowOfData:]:
            if row[currentAccountIndex] == currentAccount:
                transactionList.append(row[currentTransIndex])

        transactionList = list(dict.fromkeys(transactionList))


        for currentTrans in transactionList:

            for row in mDataObj["currentSheetValues"][indexFirstRowOfData:]:
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

                    mDataObj["valuesToWrite"].append(rowToAppend)

                    # fileForPrintObj = open(os.path.abspath(os.path.join(os.curdir, "..\\private_data\\reconcileQBO\\fileForPrint")), 'w+')
                    # fileForPrintObj.write(str(rowToAppend))
                    # fileForPrintObj.close()

    endOps("third")

