import sys, pathlib, time
sys.path.append(str(pathlib.Path.cwd().parents[1])) #for myPyLib
from myPyLib import myPyFunc, myGoogleSheetsFunc

startTime = time.time()
print("Comment: Importing modules and setting up variables...")

import datetime
from collections import OrderedDict
from pprint import pprint as pp


robinhoodSpreadsheetID = "1oisLtuJJOZnU-nMvILNWO43_8w2rCT3V6vq3vMnAnCI"
stockResultsSpreadsheetID = "1pjhFRIoB9mnbiMOj_hsFwsGth91l1oX_4kmeYrsT5mc"
sheetsToDownload = ["Raw Data - Robinhood", "Transactions To Add - Robinhood"]
googleSheetsObj = myGoogleSheetsFunc.authFunc()
robinhoodDataWithGrid = myGoogleSheetsFunc.getDataWithGrid(robinhoodSpreadsheetID, googleSheetsObj, sheetsToDownload)
stockResultsDataWithGrid = myGoogleSheetsFunc.getDataWithGrid(stockResultsSpreadsheetID, googleSheetsObj, ["Ticker Map"])

print("Comment: Importing modules and setting up variables...Done. " + str(round(time.time() - startTime, 3)) + " seconds")


rawDataRows = myGoogleSheetsFunc.countRows(robinhoodDataWithGrid, sheetsToDownload.index("Raw Data - Robinhood"))
rawDataListData = myGoogleSheetsFunc.extractValues(rawDataRows, myGoogleSheetsFunc.countColumns(robinhoodDataWithGrid, sheetsToDownload.index("Raw Data - Robinhood")), robinhoodDataWithGrid, sheetsToDownload.index("Raw Data - Robinhood"))
transactionsToAddListData = myGoogleSheetsFunc.extractValues(myGoogleSheetsFunc.countRows(robinhoodDataWithGrid, sheetsToDownload.index("Transactions To Add - Robinhood")), myGoogleSheetsFunc.countColumns(robinhoodDataWithGrid, sheetsToDownload.index("Transactions To Add - Robinhood")), robinhoodDataWithGrid, sheetsToDownload.index("Transactions To Add - Robinhood"))

tickerMapListData = myGoogleSheetsFunc.extractValues(myGoogleSheetsFunc.countRows(stockResultsDataWithGrid, 0), myGoogleSheetsFunc.countColumns(stockResultsDataWithGrid, 0), stockResultsDataWithGrid, 0)
tickerUniqueMapListData = []

for stock in tickerMapListData:

    if stock[2] not in [item[2] for item in tickerUniqueMapListData]:
        tickerUniqueMapListData.append(stock)


# pp(tickerUniqueMapListData)



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

# lastDate = int(myPyFunc.convertDateToSerialDate(datetime.datetime(2018, 10, 31)))
lastDate = int(myPyFunc.convertDateToSerialDate(datetime.datetime(2013, 10, 31)))


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
            lot = myPyFunc.convertSerialDateToDateWithoutDashes(transaction[1])
        else:
            filterForLots = [{1: "Investment Asset", 3: "Purchase", 4: stockName},
                             {1: "Investment Asset", 3: "Purchase - Stock From Merger", 4: stockName}]
            filteredList = myPyFunc.filterListOfLists(doubleEntryTransactionList, filterForLots)

            if len(filteredList) == 1:
                lot = myPyFunc.convertSerialDateToDateWithoutDashes(filteredList[0][0])


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


sqlObj = myPyFunc.createDatabase("stockResultsRobinhood.db", str(pathlib.Path.cwd().parents[3]/"privateData"/"stockResults"), tblMainName, columnsObj)
myPyFunc.populateTable(len(doubleEntryTransactionList), len(doubleEntryTransactionList[0]), tblMainName, doubleEntryTransactionList, sqlObj["sqlCursor"], [0])


tickerColumnsObj = OrderedDict()
tickerColumnsObj["rowNumber"] = "int"
tickerColumnsObj["Ticker"] = "varchar(255)"
tickerColumnsObj["stockName"] = "varchar(255)"

myPyFunc.createTable("tblTickerMap", tickerColumnsObj, sqlObj["sqlCursor"])
myPyFunc.populateTable(len(tickerUniqueMapListData), len(tickerUniqueMapListData[0]), "tblTickerMap", tickerUniqueMapListData, sqlObj["sqlCursor"], [])
# pp(myPyFunc.getQueryResult("select * from tblTickerMap", "tblTickerMap", sqlObj["sqlCursor"], False))



myPyFunc.createTableAs("tblLots", sqlObj["sqlCursor"], f"select stockName, lot, sum(amount), sum(shares) from {tblMainName} where accountName = 'Investment Asset' and broker = 'Robinhood' group by stockName, lot having sum(shares) > 0;")

sqlCommand = f"select tblLots.*, tblTickerMap.ticker, '=googlefinance(indirect(\"E\"&row()))*indirect(\"D\"&row())' as googleFin, '=indirect(\"F\"&row())-indirect(\"C\"&row())' as gainLoss from tblLots left outer join tblTickerMap on tblLots.stockName = tblTickerMap.stockName;"
myGoogleSheetsFunc.populateSheet(3, 1, "Unsold Stock Values - Robinhood", googleSheetsObj, robinhoodSpreadsheetID, myPyFunc.getQueryResult(sqlCommand, tblMainName, sqlObj["sqlCursor"], False), True)
myPyFunc.closeDatabase(sqlObj["sqlConnection"])


tranType = "Sale - Hypothetical"
priceDate = int(myPyFunc.convertDateToSerialDate(datetime.datetime.now()))
unsoldStockValuesDataWithGrid = myGoogleSheetsFunc.getDataWithGrid(robinhoodSpreadsheetID, googleSheetsObj, ["Unsold Stock Values - Robinhood"])
unsoldStockValuesList = myGoogleSheetsFunc.extractValues(myGoogleSheetsFunc.countRows(unsoldStockValuesDataWithGrid, 0), myGoogleSheetsFunc.countColumns(unsoldStockValuesDataWithGrid, 0), unsoldStockValuesDataWithGrid, 0)
doubleEntryUnsoldStockList = [] #["Date", "Account", "Amount+-", "Transaction Type", "Stock Name", "Broker", "Lot", "Shares"]]


for lot in unsoldStockValuesList:

    doubleEntryUnsoldStockList.append([priceDate, "Cash", lot[5], tranType, lot[0], "Robinhood", lot[1], ""])
    doubleEntryUnsoldStockList.append([priceDate, "Investment Asset", -lot[2], tranType, lot[0], "Robinhood", lot[1], lot[3]])

    if lot[6] < 0:
        gainLossAccount = "Loss On Sale - Hypothetical"
    else:
        gainLossAccount = "Gain On Sale - Hypothetical"

    doubleEntryUnsoldStockList.append([priceDate, gainLossAccount, -lot[6], tranType, lot[0], "Robinhood", lot[1], ""])



doubleEntryTransactionList.extend(doubleEntryUnsoldStockList)
myGoogleSheetsFunc.populateSheet(2, 100, "Transactions - Robinhood", googleSheetsObj, stockResultsSpreadsheetID, doubleEntryTransactionList, True)