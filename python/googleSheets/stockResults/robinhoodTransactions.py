import sys, pathlib
sys.path.append(str(pathlib.Path.cwd().parents[0]/"myGoogleSheetsPythonLibrary"))
sys.path.append(str(pathlib.Path.cwd().parents[1]))
from myPythonLibrary import myPythonFunctions
startTime = myPythonFunctions.startCode()

import datetime
from collections import OrderedDict
import googleSheetsFunctions, googleSheetsAuthenticate
from pprint import pprint as pp

#
# sheetInfoObj = {0:
#                     {"name": "Stock Results - Robinhood",
#                     "id": "1oisLtuJJOZnU-nMvILNWO43_8w2rCT3V6vq3vMnAnCI",
#                      "download":
#                          {"Raw Data - Robinhood":
#                               {},
#                           "Transactions To Add - Robinhood":
#                               {},
#                           "Stock Name Map":
#                               {}
#                           }
#                      },
#                 1:
#                     {"name": "Stock Results",
#                     "id": "1pjhFRIoB9mnbiMOj_hsFwsGth91l1oX_4kmeYrsT5mc"
#                     }
#                 }


robinhoodSpreadsheetID = "1oisLtuJJOZnU-nMvILNWO43_8w2rCT3V6vq3vMnAnCI"
stockResultsSpreadsheetID = "1pjhFRIoB9mnbiMOj_hsFwsGth91l1oX_4kmeYrsT5mc"
sheetsToDownload = ["Raw Data - Robinhood", "Transactions To Add - Robinhood", "Stock Name Map"]
saveJSONFile = False
googleSheetsObj = googleSheetsAuthenticate.authFunc()
googleSheetsDataWithGrid = googleSheetsFunctions.getDataWithGrid(robinhoodSpreadsheetID, googleSheetsObj, sheetsToDownload)
# sleepTime = .8


finishSetupTime = myPythonFunctions.time.time()
print("Comment: Importing modules and setting up variables...Done. " + str(round(finishSetupTime - startTime, 3)) + " seconds")

if saveJSONFile:
    myPythonFunctions.saveFile(googleSheetsDataWithGrid, pathlib.Path(pathlib.Path.cwd().parents[3]/"privateData"/"stockResults"/"googleSheetsDataWithGrid.json"), finishSetupTime)
    print("Comment: Writing data to file...Done. " + str(round(myPythonFunctions.time.time() - finishSetupTime, 3)) + " seconds")



rawDataRows = googleSheetsFunctions.countRows(googleSheetsDataWithGrid, sheetsToDownload.index("Raw Data - Robinhood"))
rawDataColumns = googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, sheetsToDownload.index("Raw Data - Robinhood"))
transactionsToAddRows = googleSheetsFunctions.countRows(googleSheetsDataWithGrid, sheetsToDownload.index("Transactions To Add - Robinhood"))
transactionsToAddColumns = googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, sheetsToDownload.index("Transactions To Add - Robinhood"))
stockNameMapRows = googleSheetsFunctions.countRows(googleSheetsDataWithGrid, sheetsToDownload.index("Stock Name Map"))
stockNameMapColumns = googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, sheetsToDownload.index("Stock Name Map"))



#load downloaded sheets into lists

# rawDataListDataWithTypes = googleSheetsFunctions.extractValuesAndTypes(rawDataRows, rawDataColumns, googleSheetsDataWithGrid, sheetsToDownload.index("Raw Data - Robinhood"))
rawDataListData = googleSheetsFunctions.extractValues(rawDataRows, rawDataColumns, googleSheetsDataWithGrid, sheetsToDownload.index("Raw Data - Robinhood"))
transactionsToAddListData = googleSheetsFunctions.extractValues(transactionsToAddRows, transactionsToAddColumns, googleSheetsDataWithGrid, sheetsToDownload.index("Transactions To Add - Robinhood"))
stockNameListData = googleSheetsFunctions.extractValues(stockNameMapRows, stockNameMapColumns, googleSheetsDataWithGrid, sheetsToDownload.index("Stock Name Map"))

# listToConvert = googleSheetsFunctions.extractValues(stockNameMapRows, stockNameMapColumns, googleSheetsDataWithGrid, 2)
# sheetInfoObj[0]["download"]["Stock Name Map"]["dictObj"] = myPythonFunctions.convertTwoColumnListToDict(listToConvert, 1)
# stockNameDict = googleSheetsFunctions.createDictMapFromSheet(googleSheetsDataWithGrid, sheetsToDownload.index("Stock Name Map"))


#create Data - Robinhood

newTransactionListCurrentColumnIndex = 0
newTransactionListToAppend = []
transactionList = []
rawDataColumnWithData = 0

# fieldsObj = {1: "Description", 2: "Date", 3: "Amount", 4: "Details"}
# pp(rawDataListData)


lastIndex = rawDataRows - 1

for indexOfRow in range(0, rawDataRows):

    nextCellValueHasNoShares = True
    currentCellValue = rawDataListData[indexOfRow][rawDataColumnWithData]

    if indexOfRow + 1 <= lastIndex:
        if len(str(rawDataListData[indexOfRow + 1][rawDataColumnWithData]).split(" share")) > 1:
            nextCellValueHasNoShares = False

    if newTransactionListCurrentColumnIndex == 2 and currentCellValue != "Failed":
        newTransactionListToAppend.append(abs(currentCellValue))
    else:
        newTransactionListToAppend.append(currentCellValue)



    # pp("indexofRow: " + str(indexOfRow))
    # pp("newTransactionListCurrentColumnIndex:" + str(newTransactionListCurrentColumnIndex))
    # pp(nextValueHasNoShares)

    if (newTransactionListCurrentColumnIndex == 2 and nextCellValueHasNoShares) or newTransactionListCurrentColumnIndex == 3:
        newTransactionListCurrentColumnIndex = -1

        if len(newTransactionListToAppend) == 3:
            newTransactionListToAppend.extend(["", ""])
        elif len(newTransactionListToAppend) == 4:
            newTransactionListToAppend.append(int(str(currentCellValue).split(" share")[0]))


        transactionList.append(newTransactionListToAppend)
        # pp(transactionList)
        newTransactionListToAppend = []

    newTransactionListCurrentColumnIndex = newTransactionListCurrentColumnIndex + 1


transactionList.sort(key=lambda x: int(x[1]))
# googleSheetsFunctions.populateSheet(1, 1, "Trial", googleSheetsObj, robinhoodSpreadsheetID, transactionList, True)

# transactionList.insert(0, ["Description", "Date", "Amount", "Details", "Shares"])


# valuesToPopulate = {"values": transactionList}
# googleSheetsObj.values().update(spreadsheetId=sheetInfoObj[0]["id"], range="Data - Robinhood", valueInputOption="USER_ENTERED", body=valuesToPopulate).execute()


#create Transactions - Robinhood


doubleEntryTransactionList = [["Date", "Account", "Amount+-", "Transaction Type", "Stock Name", "Broker", "Lot", "Shares"]]
doubleEntryTransactionList.extend(transactionsToAddListData[1:])


leftStrMap = {"Dividend from ": {"transactionType": "Dividend", "debitAccount": "Cash", "creditAccount": "Dividend Revenue"},
       "Withdrawal to ": {"transactionType": "Owners - Pay", "debitAccount": "Capital Contributions", "creditAccount": "Cash", "stockName": "All Stocks", "lotInfo": "All Lots"},
       "Deposit from ": {"transactionType": "Owners - Receive Cash", "debitAccount": "Cash", "creditAccount": "Capital Contributions", "stockName": "All Stocks", "lotInfo": "All Lots"},
       "Interest Payment": {"transactionType": "Interest", "debitAccount": "Cash", "creditAccount": "Interest Revenue", "stockName": "Cash", "lotInfo": "Cash"},
       "AKS from Robinhood": {"transactionType": "Purchase - Stock Gift", "debitAccount": "Investment Asset", "creditAccount": "Gain On Gift", "stockName": "AKS", "shares": 1}}

rightStrMap = {" Market Buy": {"transactionType": "Purchase", "debitAccount": "Investment Asset", "creditAccount": "Cash"}}

# lastDate = int(myPythonFunctions.convertDateToSerialDate(datetime.datetime(2018, 10, 31)))
lastDate = int(myPythonFunctions.convertDateToSerialDate(datetime.datetime(2013, 10, 31)))


for transaction in transactionList:


    if transaction[2] != "Failed" and transaction[1] > lastDate:

        mappedTransactionData = {}

        for leftStringToCheckFor in leftStrMap:
            if transaction[0][:len(leftStringToCheckFor)] == leftStringToCheckFor:
                mappedTransactionData = leftStrMap[leftStringToCheckFor]
                mappedTransactionData["strToCheckFor"] = leftStringToCheckFor
                mappedTransactionData["stockNamePosition"] = 1

        if not mappedTransactionData:
            for rightStrToCheckFor in rightStrMap:
                if transaction[0][-len(rightStrToCheckFor):] == rightStrToCheckFor:
                    mappedTransactionData = rightStrMap[rightStrToCheckFor]
                    mappedTransactionData["strToCheckFor"] = rightStrToCheckFor
                    mappedTransactionData["stockNamePosition"] = 0

        # pp(transaction)

        if "stockName" in mappedTransactionData:
            stockName = mappedTransactionData["stockName"]
        elif transaction[0].split(mappedTransactionData["strToCheckFor"])[mappedTransactionData["stockNamePosition"]] in ["Xperi", "Tessera Technologies, Inc. - Common Stock"]:
            stockName = "Xperi, formerly Tessera"
        else:
            stockName = transaction[0].split(mappedTransactionData["strToCheckFor"])[mappedTransactionData["stockNamePosition"]]


        if "lotInfo" in mappedTransactionData:
            lot = mappedTransactionData["lotInfo"]
        elif mappedTransactionData["transactionType"] in ["Purchase", "Purchase - Stock Gift", "Purchase - Stock From Merger"]:
            lot = myPythonFunctions.convertSerialDateToDateWithoutDashes(transaction[1])
        else:
            filterForLots = [{1: "Investment Asset", 3: "Purchase", 4: stockName},
                             {1: "Investment Asset", 3: "Purchase - Stock From Merger", 4: stockName}]
            filteredList = myPythonFunctions.filterListOfLists(doubleEntryTransactionList, filterForLots)

            if len(filteredList) == 1:
                lot = myPythonFunctions.convertSerialDateToDateWithoutDashes(filteredList[0][0])


        if "shares" in mappedTransactionData:
            shares = mappedTransactionData["shares"]
        else:
            shares = transaction[4]

        doubleEntryTransactionList.append([transaction[1], mappedTransactionData["debitAccount"], transaction[2], mappedTransactionData["transactionType"], stockName, "Robinhood", lot, shares])
        doubleEntryTransactionList.append([transaction[1], mappedTransactionData["creditAccount"], -transaction[2], mappedTransactionData["transactionType"], stockName, "Robinhood", lot, ""])




# googleSheetsFunctions.populateSheet(3, 8, "Trial", googleSheetsObj, robinhoodSpreadsheetID, doubleEntryTransactionList, True)








# dateForUnsold = int(myPythonFunctions.convertDateToSerialDate(datetime.datetime.now()))

# googleSheetsTempData = None

# createRequest = {
#                           "requests": [
#                             {
#                               "addSheet": {
#                                 "properties": {
#                                   "title": "unsoldStockUpdateSheet",
#                                   "gridProperties": {
#                                     "rowCount": 1,
#                                     "columnCount": 1
#                                   }
#                                 }
#                               }
#                             }
#                           ]
#                         }


# googleSheetsObj.batchUpdate(spreadsheetId=robinhoodSpreadsheetID, body=createRequest).execute()


tblMainName = "tblStockResultsRobinhood"
tblStockMapName = "tblStockMap"

columnsObj = OrderedDict()
columnsObj["tranDate"] = "date"
columnsObj["accountName"] = "varchar(255)"
columnsObj["amount"] = "float"
columnsObj["transactionType"] = "varchar(255)"
columnsObj["stockName"] = "varchar(255)"
columnsObj["broker"] = "varchar(255)"
columnsObj["lot"] = "varchar(255)"
columnsObj["shares"] = "float"

stockColumnsObj = OrderedDict()
stockColumnsObj["stockName"] = "varchar(255)"
stockColumnsObj["ticker"] = "varchar(255)"

doubleEntryUnsoldStockList = [] #["Date", "Account", "Amount+-", "Transaction Type", "Stock Name", "Broker", "Lot", "Shares"]]


sqlObj = myPythonFunctions.createDatabase("stockResultsRobinhood.db", str(pathlib.Path.cwd().parents[3]/"privateData"/"stockResults"), tblMainName, columnsObj)
myPythonFunctions.populateTable(len(doubleEntryTransactionList), len(doubleEntryTransactionList[0]), tblMainName, doubleEntryTransactionList, sqlObj["sqlCursor"], [0])
myPythonFunctions.createTable(tblStockMapName, stockColumnsObj, sqlObj["sqlCursor"])
myPythonFunctions.populateTable(stockNameMapRows, stockNameMapColumns, tblStockMapName, stockNameListData, sqlObj["sqlCursor"], [])
# pp(myPythonFunctions.getQueryResult(f"select * from {tblStockMapName}", tblStockMapName, sqlObj["sqlCursor"], False))


sqlList = ["drop table if exists tblLots;", f"create table tblLots as select stockName, lot, sum(amount), sum(shares) from {tblMainName} where accountName = 'Investment Asset' and broker = 'Robinhood' group by stockName, lot having sum(shares) > 0;"]
myPythonFunctions.executeSQLStatements(sqlList, sqlObj["sqlCursor"])


sqlCommand = f"select tblLots.*, {tblStockMapName}.ticker, '=googlefinance(indirect(\"E\"&row()))*indirect(\"D\"&row())' as googleFinForm, '=indirect(\"F\"&row())-indirect(\"C\"&row())' as gainLoss from tblLots left outer join {tblStockMapName} on tblLots.stockName = {tblStockMapName}.stockName;"
googleSheetsFunctions.populateSheet(3, 1, "Unsold Stock Values - Robinhood", googleSheetsObj, robinhoodSpreadsheetID, myPythonFunctions.getQueryResult(sqlCommand, tblMainName, sqlObj["sqlCursor"], False), True)
myPythonFunctions.closeDatabase(sqlObj["sqlConnection"])


tranType = "Sale - Hypothetical"
priceDate = int(myPythonFunctions.convertDateToSerialDate(datetime.datetime.now()))
googleSheetsDataWithGrid = googleSheetsFunctions.getDataWithGrid(robinhoodSpreadsheetID, googleSheetsObj, ["Unsold Stock Values - Robinhood"])
unsoldStockValuesList = googleSheetsFunctions.extractValues(googleSheetsFunctions.countRows(googleSheetsDataWithGrid, 0), googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, 0), googleSheetsDataWithGrid, 0)

for lot in unsoldStockValuesList:

    doubleEntryUnsoldStockList.append([priceDate, "Cash", lot[5], tranType, lot[0], "Robinhood", lot[1], ""])
    doubleEntryUnsoldStockList.append([priceDate, "Investment Asset", -lot[2], tranType, lot[0], "Robinhood", lot[1], lot[3]])

    if lot[6] < 0:
        gainLossAccount = "Loss On Sale - Hypothetical"
    else:
        gainLossAccount = "Gain On Sale - Hypothetical"

    doubleEntryUnsoldStockList.append([priceDate, gainLossAccount, -lot[6], tranType, lot[0], "Robinhood", lot[1], ""])




doubleEntryTransactionList.extend(doubleEntryUnsoldStockList)
googleSheetsFunctions.populateSheet(2, 100, "Transactions - Robinhood", googleSheetsObj, stockResultsSpreadsheetID, doubleEntryTransactionList, True)






# for stockToFilter in stockNameDict:
#
#
#     filteredTransactions =
    # pp(stockToFilter)
    # pp(filteredTransactions)


#     # pp(filteredTransactions)
#
#     for lot in filteredTransactions:
#
#         if googleSheetsTempData:
#
#             deleteRowsCols = {
#                 "requests": [
#                     {
#                         "deleteDimension": {
#                             "range": {
#                                 "sheetId": googleSheetsTempData["sheets"][0]["properties"]["sheetId"],
#                                 "dimension": "ROWS",
#                                 "startIndex": 1,
#                                 "endIndex": 1000
#                             }
#                         }
#                     },
#                     {
#                         "deleteDimension": {
#                             "range": {
#                                 "sheetId": googleSheetsTempData["sheets"][0]["properties"]["sheetId"],
#                                 "dimension": "COLUMNS",
#                                 "startIndex": 1,
#                                 "endIndex": 1000
#                             }
#                         }
#                     },
#                 ],
#             }
#
#
#             myPythonFunctions.time.sleep(sleepTime)
#             googleSheetsObj.batchUpdate(spreadsheetId=sheetInfoObj[0]["id"], body=deleteRowsCols).execute()
#
#
#         myPythonFunctions.time.sleep(sleepTime)
#         googleSheetsObj.values().clear(spreadsheetId=sheetInfoObj[0]["id"], range="unsoldStockUpdateSheet", body={}).execute()
#
#
#         unsoldLotList = []
#         unsoldLotList.append(
#             [dateForUnsold, "Cash", "=GOOGLEFINANCE(\"" + ticker + "\")*INDIRECT(\"H\"&ROW())", tranType, stockToFilter,
#              "Robinhood", lot[6], lot[7]])
#         unsoldLotList.append(
#             [dateForUnsold, "Investment Asset", -lot[2], tranType, stockToFilter, "Robinhood", lot[6], lot[7]])
#
#
#         myPythonFunctions.time.sleep(sleepTime)
#         googleSheetsObj.values().update(spreadsheetId=sheetInfoObj[0]["id"], range="unsoldStockUpdateSheet", valueInputOption="USER_ENTERED", body={"values": unsoldLotList}).execute()
#
#
#         googleSheetsTempData = googleSheetsFunctions.getDataWithGrid(sheetInfoObj[0]["id"], googleSheetsObj, ["unsoldStockUpdateSheet"])
#
#
#         listObj = googleSheetsFunctions.extractValues(googleSheetsFunctions.countRows(googleSheetsTempData, 0), googleSheetsFunctions.countColumns(googleSheetsTempData, 0), googleSheetsTempData, 0)
#         netSum = myPythonFunctions.sumListOfLists(listObj, 2)
#
#         if netSum < 0:
#             account = "Loss On Sale - Hypothetical"
#         else:
#             account = "Gain On Sale - Hypothetical"
#
#
#         unsoldLotList[0][2] = listObj[0][2]
#         unsoldLotList.append([dateForUnsold, account, -netSum, tranType, stockToFilter, "Robinhood", lot[6], lot[7]])
#         doubleEntryUnsoldStockList.extend(unsoldLotList)
#
#
# myPythonFunctions.time.sleep(sleepTime)
# valuesToPopulate = {"values": doubleEntryUnsoldStockList}
# googleSheetsObj.values().update(spreadsheetId=sheetInfoObj[0]["id"], range="Transactions - Unsold Stock - Robinhood", valueInputOption="USER_ENTERED", body=valuesToPopulate).execute()
#
#
#
#
# deleteRequest = {
#     "requests": [
#         {
#             "deleteSheet": {
#                 "sheetId": googleSheetsTempData["sheets"][0]["properties"]["sheetId"]
#             }
#         }
#     ]
# }
#
# myPythonFunctions.time.sleep(sleepTime)
# googleSheetsObj.batchUpdate(spreadsheetId=sheetInfoObj[0]["id"], body=deleteRequest).execute()

