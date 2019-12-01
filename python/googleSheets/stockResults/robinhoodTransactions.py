import sys, pathlib
sys.path.append(str(pathlib.Path.cwd().parents[0]/"myGoogleSheetsPythonLibrary"))
sys.path.append(str(pathlib.Path.cwd().parents[1]))
from myPythonLibrary import myPythonFunctions
startTime = myPythonFunctions.startCode()

import datetime
from collections import OrderedDict
import googleSheetsFunctions, googleSheetsAuthenticate
from pprint import pprint as pp


robinhoodSpreadsheetID = "1oisLtuJJOZnU-nMvILNWO43_8w2rCT3V6vq3vMnAnCI"
stockResultsSpreadsheetID = "1pjhFRIoB9mnbiMOj_hsFwsGth91l1oX_4kmeYrsT5mc"
sheetsToDownload = ["Raw Data - Robinhood", "Transactions To Add - Robinhood", "Stock Name Map"]
googleSheetsObj = googleSheetsAuthenticate.authFunc()
googleSheetsDataWithGrid = googleSheetsFunctions.getDataWithGrid(robinhoodSpreadsheetID, googleSheetsObj, sheetsToDownload)


finishSetupTime = myPythonFunctions.time.time()
print("Comment: Importing modules and setting up variables...Done. " + str(round(finishSetupTime - startTime, 3)) + " seconds")


rawDataRows = googleSheetsFunctions.countRows(googleSheetsDataWithGrid, sheetsToDownload.index("Raw Data - Robinhood"))
stockNameMapRows = googleSheetsFunctions.countRows(googleSheetsDataWithGrid, sheetsToDownload.index("Stock Name Map"))
stockNameMapColumns = googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, sheetsToDownload.index("Stock Name Map"))


rawDataListData = googleSheetsFunctions.extractValues(rawDataRows, googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, sheetsToDownload.index("Raw Data - Robinhood")), googleSheetsDataWithGrid, sheetsToDownload.index("Raw Data - Robinhood"))
transactionsToAddListData = googleSheetsFunctions.extractValues(googleSheetsFunctions.countRows(googleSheetsDataWithGrid, sheetsToDownload.index("Transactions To Add - Robinhood")), googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, sheetsToDownload.index("Transactions To Add - Robinhood")), googleSheetsDataWithGrid, sheetsToDownload.index("Transactions To Add - Robinhood"))
stockNameListData = googleSheetsFunctions.extractValues(stockNameMapRows, stockNameMapColumns, googleSheetsDataWithGrid, sheetsToDownload.index("Stock Name Map"))


#create data

newTransactionListCurrentColumnIndex = 0
newTransactionListToAppend = []
transactionList = []
rawDataColumnWithData = 0


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


#create transactions

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




tblMainName = "tblStockResultsRobinhood"


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
myPythonFunctions.createTable("tblStockMap", stockColumnsObj, sqlObj["sqlCursor"])
myPythonFunctions.populateTable(stockNameMapRows, stockNameMapColumns, "tblStockMap", stockNameListData, sqlObj["sqlCursor"], [])
# pp(myPythonFunctions.getQueryResult(f"select * from {tblStockMapName}", tblStockMapName, sqlObj["sqlCursor"], False))


myPythonFunctions.createTableAs("tblLots", sqlObj["sqlCursor"], f"select stockName, lot, sum(amount), sum(shares) from {tblMainName} where accountName = 'Investment Asset' and broker = 'Robinhood' group by stockName, lot having sum(shares) > 0;")

sqlCommand = f"select tblLots.*, tblStockMap.ticker, '=googlefinance(indirect(\"E\"&row()))*indirect(\"D\"&row())' as googleFin, '=indirect(\"F\"&row())-indirect(\"C\"&row())' as gainLoss from tblLots left outer join tblStockMap on tblLots.stockName = tblStockMap.stockName;"
googleSheetsFunctions.populateSheet(3, 1, "Unsold Stock Values - Robinhood", googleSheetsObj, robinhoodSpreadsheetID, myPythonFunctions.getQueryResult(sqlCommand, tblMainName, sqlObj["sqlCursor"], False), True)
myPythonFunctions.closeDatabase(sqlObj["sqlConnection"])


tranType = "Sale - Hypothetical"
priceDate = int(myPythonFunctions.convertDateToSerialDate(datetime.datetime.now()))
unsoldStockValuesDataWithGrid = googleSheetsFunctions.getDataWithGrid(robinhoodSpreadsheetID, googleSheetsObj, ["Unsold Stock Values - Robinhood"])
unsoldStockValuesList = googleSheetsFunctions.extractValues(googleSheetsFunctions.countRows(unsoldStockValuesDataWithGrid, 0), googleSheetsFunctions.countColumns(unsoldStockValuesDataWithGrid, 0), unsoldStockValuesDataWithGrid, 0)

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