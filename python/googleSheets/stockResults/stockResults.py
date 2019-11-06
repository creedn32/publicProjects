import sys, pathlib
sys.path.append(str(pathlib.Path.cwd().parents[0]))
sys.path.append(str(pathlib.Path.cwd().parents[1]))
from myPythonLibrary import myPythonFunctions
startTime = myPythonFunctions.startCode()

import importlib
googleSheetsFunctions = importlib.import_module("myGoogleSheetsPythonLibrary.googleSheetsFunctions")
googleSheetsAuthenticate = importlib.import_module("myGoogleSheetsPythonLibrary.googleSheetsAuthenticate")
from pprint import pprint as pp


# spreadsheetID = "1yZfwzel6R3HTUtH5HIv7LEjAaoJDPESG6jCEz-b7jBw" #simple spreadsheet
spreadsheetID = "1pjhFRIoB9mnbiMOj_hsFwsGth91l1oX_4kmeYrsT5mc" #full spreadsheet


googleSheetsObj = googleSheetsAuthenticate.authFunc()
googleSheetsDataWithGrid = googleSheetsFunctions.getDataWithGrid(spreadsheetID, googleSheetsObj)
# googleSheetsFunctions.saveFile(googleSheetsDataWithGrid, pathlib.Path(pathlib.Path.cwd().parents[3]/"privateData"/"stockResults"/"googleSheetsDataWithGrid.json"))


print("Comment: Importing modules and setting up variables...Done. " + str(round(myPythonFunctions.time.time() - startTime, 3)) + " seconds")



numberOfRows = googleSheetsFunctions.countRows(googleSheetsDataWithGrid, 0)
numberOfColumns = googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, 0)
accountColumn = 1
listOfSheetData = []

for indexOfRow in range(0, numberOfRows):
    currentRowData = []

    for indexOfColumn in range(0, numberOfColumns):
        currentRowData.append(googleSheetsFunctions.getCellValue(googleSheetsDataWithGrid, 0, indexOfRow, indexOfColumn))

    listOfSheetData.append(currentRowData)


# for indexOfRow in range(0, numberOfRows):
#     if listOfSheetData[indexOfRow][1] == "Cash":
#         listOfSheetData[indexOfRow][1] = "Cash (General)"


for indexOfRow in range(0, numberOfRows):
    listOfSheetData[indexOfRow][accountColumn] = listOfSheetData[indexOfRow][accountColumn].replace(" - " + listOfSheetData[indexOfRow][5], " ")

for indexOfRow in range(0, numberOfRows):
    listOfSheetData[indexOfRow][accountColumn] = listOfSheetData[indexOfRow][accountColumn].replace(" - " + listOfSheetData[indexOfRow][6], " ")

for indexOfRow in range(0, numberOfRows):
    listOfSheetData[indexOfRow][accountColumn] = listOfSheetData[indexOfRow][accountColumn].replace(listOfSheetData[indexOfRow][4] + " - ", "")

for indexOfRow in range(0, numberOfRows):
    listOfSheetData[indexOfRow][accountColumn] = listOfSheetData[indexOfRow][accountColumn].rstrip()


numberOfRowsChartOfAccounts = googleSheetsFunctions.countRows(googleSheetsDataWithGrid, 2)
numberOfColumnsChartOfAccounts = googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, 2)
chartOfAccountsDict = {}

for indexOfRow in range(1, numberOfRowsChartOfAccounts):

    mapDict = {}

    for indexOfColumn in range(1, numberOfColumnsChartOfAccounts + 1):
        mapDict[googleSheetsFunctions.getCellValue(googleSheetsDataWithGrid, 2, 0, indexOfColumn)] = googleSheetsFunctions.getCellValue(googleSheetsDataWithGrid, 2, indexOfRow, indexOfColumn)



    # mapDict = {
    #             googleSheetsFunctions.getCellValue(googleSheetsDataWithGrid, 2, 0, 1): googleSheetsFunctions.getCellValue(googleSheetsDataWithGrid, 2, indexOfRow, 1),
    #             googleSheetsFunctions.getCellValue(googleSheetsDataWithGrid, 2, 0, 2): googleSheetsFunctions.getCellValue(googleSheetsDataWithGrid, 2, indexOfRow, 2)}

    chartOfAccountsDict[googleSheetsFunctions.getCellValue(googleSheetsDataWithGrid, 2, indexOfRow, 0)] = mapDict

for columnToMap in range(numberOfColumnsChartOfAccounts - 1, 0, -1):

    columnHeading = googleSheetsFunctions.getCellValue(googleSheetsDataWithGrid, 2, 0, columnToMap)

    for indexOfRow in range(0, numberOfRows):
        if indexOfRow == 0:
            listOfSheetData[indexOfRow].insert(accountColumn + 1, columnHeading)
        else:
            listOfSheetData[indexOfRow].insert(accountColumn + 1, chartOfAccountsDict[listOfSheetData[indexOfRow][accountColumn]][columnHeading])



valuesToWrite = {"values": listOfSheetData}
googleSheetsObj.values().update(spreadsheetId=spreadsheetID, range="Formatted Transactions!A1", valueInputOption="USER_ENTERED", body=valuesToWrite).execute()






# def convertNumber(num):
#     # try:
#         num = creedFunctions.convertEmptyStrToZero(num)
#         num = creedFunctions.removeCommaFromStr(num)
#         num = float(num)
#         return num
#     # except BaseException as e:
#         print("Error on " + num + " " + str(e))
#
#
#
# def beginOps(currentSheet, nextSheet, firstRow):
#
#     sheetInfo["startTime"] = time.time()
#     print("Comment: Creating " + nextSheet + " sheet...")
#
#
#     for sheetToSearch in [currentSheet, nextSheet]:
#         for sheetWithGridInfo in sheetInfo["sheetsGridInfoObj"]["sheets"]:
#             if sheetWithGridInfo["properties"]["title"] == sheetInfo[sheetToSearch]["name"]:
#                 sheetInfo[sheetToSearch]["lastCell"] = creedFunctions.columnToLetter(sheetWithGridInfo["properties"]["gridProperties"]["columnCount"]) + str(sheetWithGridInfo["properties"]["gridProperties"]["rowCount"])
#                 sheetInfo[sheetToSearch]["numberOfColumns"] = sheetWithGridInfo["properties"]["gridProperties"]["columnCount"]
#
#     rangeToClear = sheetInfo[nextSheet]["name"] + "!" + sheetInfo["allSheets"]["begRange"] + ":" + sheetInfo[nextSheet]["lastCell"]
#     sheetInfo["googleSheetsObj"].values().clear(spreadsheetId=sheetInfo["currentSpreadsheetID"], range=rangeToClear, body={}).execute()
#
#
#     rangeToDownload = sheetInfo[currentSheet]["name"] + "!" + sheetInfo["allSheets"]["begRange"] + ":" + sheetInfo[currentSheet]["lastCell"]
#     sheetInfo[currentSheet]["obj"] = sheetInfo["googleSheetsObj"].values().get(spreadsheetId=sheetInfo["currentSpreadsheetID"], range=rangeToDownload).execute()
#     sheetInfo[currentSheet]["values"] = sheetInfo[currentSheet]["obj"].get("values", [])
#     sheetInfo[currentSheet]["shortValues"] = sheetInfo[currentSheet]["values"][sheetInfo["allSheets"]["indexOfFirstRowOfData"]:]
#
#
#
#     if currentSheet == "first":
#
#         for row in sheetInfo[currentSheet]["shortValues"]:
#
#             if len(row) < sheetInfo[currentSheet]["numberOfColumns"] and len(row) > 1:
#
#                 columnsToAdd = sheetInfo[currentSheet]["numberOfColumns"] - len(row)
#
#                 for i in range(columnsToAdd):
#                     row.append("")
#
#
#     firstRowToWrite = firstRow
#
#     for cell in sheetInfo[currentSheet]["values"][sheetInfo["allSheets"]["indexOfFirstRowOfData"] - 1]:
#         firstRowToWrite.append(cell)
#
#     return [firstRowToWrite]
#
#
#
#
# def endOps(nextSt, vToWrite):
#
#     bodyToWrite = {
#         "values": vToWrite
#     }
#
#     rangeToWrite = sheetInfo[nextSt]["name"] + "!" + sheetInfo["allSheets"]["begRange"]
#     sheetInfo["googleSheetsObj"].values().update(spreadsheetId=sheetInfo["currentSpreadsheetID"], range=rangeToWrite, valueInputOption="USER_ENTERED", body=bodyToWrite).execute()
#     print("Comment: Creating " + nextSt + " sheet...Done. " + str(round(time.time() - sheetInfo["startTime"], 3)) + " seconds")



#
#
# sheetInfo = {
#     startTime: None,
#     "googleSheetsObj": googleSheetsAuthenticate.authFunc(),
#     "currentSpreadsheetID": "1pjhFRIoB9mnbiMOj_hsFwsGth91l1oX_4kmeYrsT5mc",
#     "allSheets": {"begRange": "A1",
#                   "indexOfFirstRowOfData": 1},
#     # "first":
#     #     {"name": "firstSheetTest"},
#     # "second":
#     #     {"name": "secondSheetTest",
#     #      "create?": True,
#     #      "transIndex": 0,
#     #      "accountIndex": 2},
#     # "third":
#     #     {"name": "thirdSheetTest",
#     #      "create?": True}
# }


# sheetInfo["second"]["amountIndex"] = sheetInfo["second"]["accountIndex"] + 3
# sheetInfo["second"]["debitIndex"] = sheetInfo["second"]["accountIndex"] + 1
# sheetInfo["second"]["creditIndex"] = sheetInfo["second"]["accountIndex"] + 2
#
#
# sheetInfo["sheetsGridInfoObj"] = sheetInfo["googleSheetsObj"].get(spreadsheetId=sheetInfo["currentSpreadsheetID"], fields="sheets(properties(title,gridProperties))").execute()

# print(sheetInfo["sheetsGridInfoObj"])





# currentSheet = "first"
# nextSheet = "second"
#
# if sheetInfo[nextSheet]["create?"]:
#
#     valToWrite = beginOps(currentSheet, nextSheet, ["Transaction Number"])
#     dataToFillDown = {0: "", 6: "", 7: "", 8: "", 9: "", 10: ""}
#     transactionNum = 1
#
#     for rowFromCurrentSheet in sheetInfo[currentSheet]["shortValues"]:
#
#         if rowFromCurrentSheet:
#
#             for key in dataToFillDown:
#                 if rowFromCurrentSheet[key] != "":
#                    dataToFillDown[key] = rowFromCurrentSheet[key]
#
#             rowToWrite = [transactionNum]
#
#             for index in range(len(rowFromCurrentSheet)):
#                 if index in dataToFillDown.keys():
#                     rowToWrite.append(dataToFillDown[index])
#                 else:
#                     rowToWrite.append(rowFromCurrentSheet[index])
#
#             valToWrite.append(rowToWrite)
#
#         else:
#             transactionNum = transactionNum + 1
#             dataToFillDown = {0: "", 6: "", 7: "", 8: "", 9: "", 10: ""}
#
#     endOps(nextSheet, valToWrite)
#
#
#
# currentSheet = "second"
# nextSheet = "third"
#
# if sheetInfo[nextSheet]["create?"]:
#
#     valToWrite = beginOps(currentSheet, nextSheet, ["Main Account", "Amount+-"])
#
#     accountList = []
#
#     for row in sheetInfo[currentSheet]["shortValues"]:
#         if row[sheetInfo[currentSheet]["accountIndex"]] not in accountList:
#             accountList.append(row[sheetInfo[currentSheet]["accountIndex"]])
#
#
#     for currentAccount in accountList:
#
#         transactionList = []
#
#         for row in sheetInfo[currentSheet]["shortValues"]:
#             if row[sheetInfo[currentSheet]["accountIndex"]] == currentAccount and row[sheetInfo[currentSheet]["transIndex"]] not in transactionList:
#                 transactionList.append(row[sheetInfo[currentSheet]["transIndex"]])
#
#         for currentTrans in transactionList:
#
#             for row in sheetInfo[currentSheet]["shortValues"]:
#
#                 if row[sheetInfo[currentSheet]["transIndex"]] == currentTrans:
#
#                     if row[sheetInfo[currentSheet]["accountIndex"]] != currentAccount:
#
#                         row[sheetInfo[currentSheet]["amountIndex"]] = convertNumber(row[sheetInfo[currentSheet]["amountIndex"]])
#                         row[sheetInfo[currentSheet]["debitIndex"]] = convertNumber(row[sheetInfo[currentSheet]["debitIndex"]])
#                         row[sheetInfo[currentSheet]["creditIndex"]] = convertNumber(row[sheetInfo[currentSheet]["creditIndex"]])
#
#                         valToWrite.append([currentAccount, -row[sheetInfo[currentSheet]["debitIndex"]] + row[sheetInfo[currentSheet]["creditIndex"]]] + row)
#
#
#     endOps(nextSheet, valToWrite)








# def myfunc():
#     global time
#     import time
#     # print(time.time())
#
#
# myfunc()
# print(time.time())
