import sys, pathlib
sys.path.append(str(pathlib.Path.cwd().parents[1]))
from myPyLib import myPyFunc, myGoogleSheetsFunc


splitTime = myPyFunc.printElapsedTime(False, "Starting script")

import datetime
from collections import OrderedDict
from pprint import pprint as pp

robSpreadsheetID = "1oisLtuJJOZnU-nMvILNWO43_8w2rCT3V6vq3vMnAnCI"
resultsSpreadsheetID = "1pjhFRIoB9mnbiMOj_hsFwsGth91l1oX_4kmeYrsT5mc"
googleSheetsAPIObj = myGoogleSheetsFunc.authFunc()

splitTime = myPyFunc.printElapsedTime(splitTime, "Finished importing modules and intializing variables")

###########################################################################################

resultsToDownload = ["Inputs", "Ticker Map"]
resultsDownloadedWithGrid = myGoogleSheetsFunc.getDataWithGrid(resultsSpreadsheetID, googleSheetsAPIObj, resultsToDownload)
inputsExtractedValues = myGoogleSheetsFunc.extractValues(myGoogleSheetsFunc.countRows(resultsDownloadedWithGrid, resultsToDownload.index("Inputs")), myGoogleSheetsFunc.countColumns(resultsDownloadedWithGrid, resultsToDownload.index("Inputs")), resultsDownloadedWithGrid, resultsToDownload.index("Inputs"))
tickerMapIndexStockName = inputsExtractedValues[0][1]


tickerMapExtractedValues = myGoogleSheetsFunc.extractValues(myGoogleSheetsFunc.countRows(resultsDownloadedWithGrid, resultsToDownload.index("Ticker Map")), myGoogleSheetsFunc.countColumns(resultsDownloadedWithGrid, resultsToDownload.index("Ticker Map")), resultsDownloadedWithGrid, resultsToDownload.index("Ticker Map"))
tickerMapUniqueExtractedValues = []

for tickerMapItem in tickerMapExtractedValues:

    if tickerMapItem[tickerMapIndexStockName] not in [tickerMapUniqueItem[tickerMapIndexStockName] for tickerMapUniqueItem in tickerMapUniqueExtractedValues]:
        tickerMapUniqueExtractedValues.append(tickerMapItem)


robToDownload = ["Raw Data - Robinhood", "Transactions To Add - Robinhood"]
robDownloadedWithGrid = myGoogleSheetsFunc.getDataWithGrid(robSpreadsheetID, googleSheetsAPIObj, robToDownload)

robRawDataRows = myGoogleSheetsFunc.countRows(robDownloadedWithGrid, robToDownload.index("Raw Data - Robinhood"))
robRawDataExtractedValues = myGoogleSheetsFunc.extractValues(robRawDataRows, myGoogleSheetsFunc.countColumns(robDownloadedWithGrid, robToDownload.index("Raw Data - Robinhood")), robDownloadedWithGrid, robToDownload.index("Raw Data - Robinhood"))
robTransactionsToAddExtractedValues = myGoogleSheetsFunc.extractValues(myGoogleSheetsFunc.countRows(robDownloadedWithGrid, robToDownload.index("Transactions To Add - Robinhood")), myGoogleSheetsFunc.countColumns(robDownloadedWithGrid, robToDownload.index("Transactions To Add - Robinhood")), robDownloadedWithGrid, robToDownload.index("Transactions To Add - Robinhood"))




#create data

robNewTransListCurrColIndex = 0
robNewTransRow = []
robNewTransList = []
robRawDataColumnIndexWithData = 0
robRawDataLastRowIndex = robRawDataRows - 1

for robRawDataIndexOfRow in range(0, robRawDataRows):

    robRawDataNextCellValueHasNoShares = True
    robRawDataCurrentCellValue = robRawDataExtractedValues[robRawDataIndexOfRow][robRawDataColumnIndexWithData]

    if robRawDataIndexOfRow + 1 <= robRawDataLastRowIndex:
        if len(str(robRawDataExtractedValues[robRawDataIndexOfRow + 1][robRawDataColumnIndexWithData]).split(" share")) > 1:
            robRawDataNextCellValueHasNoShares = False

    if robNewTransListCurrColIndex == 2 and robRawDataCurrentCellValue != "Failed":
        robNewTransRow.append(abs(robRawDataCurrentCellValue))
    else:
        robNewTransRow.append(robRawDataCurrentCellValue)



    if (robNewTransListCurrColIndex == 2 and robRawDataNextCellValueHasNoShares) or robNewTransListCurrColIndex == 3:
        robNewTransListCurrColIndex = -1

        if len(robNewTransRow) == 3:
            robNewTransRow.extend(["", ""])
        elif len(robNewTransRow) == 4:
            robNewTransRow.append(int(str(robRawDataCurrentCellValue).split(" share")[0]))


        robNewTransList.append(robNewTransRow)
        robNewTransRow = []

    robNewTransListCurrColIndex = robNewTransListCurrColIndex + 1


robNewTransList.sort(key=lambda x: int(x[1]))

# pp(robNewTransList)


#create transactions

doubleEntryTransactionList = [["Date", "Account", "Amount+-", "Transaction Type", "Stock Name", "Broker", "Lot", "Shares"]]
doubleEntryTransactionList.extend(robTransactionsToAddExtractedValues[1:])


leftStrMap = {"Dividend from ": {"transactionType": "Dividend", "debitAccount": "Cash", "creditAccount": "Dividend Revenue"},
       "Withdrawal to ": {"transactionType": "Owners - Pay", "debitAccount": "Capital Contributions", "creditAccount": "Cash", "stockName": "All Stocks", "lotInfo": "All Lots"},
       "Deposit from ": {"transactionType": "Owners - Receive Cash", "debitAccount": "Cash", "creditAccount": "Capital Contributions", "stockName": "All Stocks", "lotInfo": "All Lots"},
       "Interest Payment": {"transactionType": "Interest", "debitAccount": "Cash", "creditAccount": "Interest Revenue", "stockName": "Cash", "lotInfo": "Cash"},
       "AKS from Robinhood": {"transactionType": "Purchase - Stock Gift", "debitAccount": "Investment Asset", "creditAccount": "Gain On Gift", "stockName": "AKS", "shares": 1}}

rightStrMap = {" Market Buy": {"transactionType": "Purchase", "debitAccount": "Investment Asset", "creditAccount": "Cash"}}


lastDate = int(myPyFunc.convertDateToSerialDate(datetime.datetime(2013, 10, 31)))    # lastDate = int(myPyFunc.convertDateToSerialDate(datetime.datetime(2018, 10, 31)))


for transaction in robNewTransList:

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
myPyFunc.populateTable(len(tickerMapUniqueExtractedValues), len(tickerMapUniqueExtractedValues[0]), "tblTickerMap", tickerMapUniqueExtractedValues, sqlObj["sqlCursor"], [])
# pp(myPyFunc.getQueryResult("select * from tblTickerMap", "tblTickerMap", sqlObj["sqlCursor"], False))



myPyFunc.createTableAs("tblLots", sqlObj["sqlCursor"], f"select stockName, lot, sum(amount), sum(shares) from {tblMainName} where accountName = 'Investment Asset' and broker = 'Robinhood' group by stockName, lot having sum(shares) > 0;")

sqlCommand = f"select tblLots.*, tblTickerMap.ticker, '=googlefinance(indirect(\"E\"&row()))*indirect(\"D\"&row())' as googleFin, '=indirect(\"F\"&row())-indirect(\"C\"&row())' as gainLoss from tblLots left outer join tblTickerMap on tblLots.stockName = tblTickerMap.stockName;"
myGoogleSheetsFunc.populateSheet(3, 1, "Unsold Stock Values - Robinhood", googleSheetsAPIObj, robSpreadsheetID, myPyFunc.getQueryResult(sqlCommand, tblMainName, sqlObj["sqlCursor"], False), True)
myPyFunc.closeDatabase(sqlObj["sqlConnection"])


tranType = "Sale - Hypothetical"
priceDate = int(myPyFunc.convertDateToSerialDate(datetime.datetime.now()))
unsoldStockValuesDataWithGrid = myGoogleSheetsFunc.getDataWithGrid(robSpreadsheetID, googleSheetsAPIObj, ["Unsold Stock Values - Robinhood"])
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
myGoogleSheetsFunc.populateSheet(2, 100, "Transactions - Robinhood", googleSheetsAPIObj, resultsSpreadsheetID, doubleEntryTransactionList, True)



splitTime = myPyFunc.printElapsedTime(splitTime, "Finished processing Robinhood")

###########################################################################################





stockResultsSheetsToDownload = ["Transactions", "Transactions - Robinhood", "Chart of Accounts", "Ticker Map"]
googleSheetsDataWithGrid = myGoogleSheetsFunc.getDataWithGrid(resultsSpreadsheetID, googleSheetsAPIObj, stockResultsSheetsToDownload)

tranDataList = myGoogleSheetsFunc.extractValues(myGoogleSheetsFunc.countRows(googleSheetsDataWithGrid, stockResultsSheetsToDownload.index("Transactions")), myGoogleSheetsFunc.countColumns(googleSheetsDataWithGrid, stockResultsSheetsToDownload.index("Transactions")), googleSheetsDataWithGrid, stockResultsSheetsToDownload.index("Transactions"))
tranRobinhoodDataList = myGoogleSheetsFunc.extractValues(myGoogleSheetsFunc.countRows(googleSheetsDataWithGrid, stockResultsSheetsToDownload.index("Transactions - Robinhood")), myGoogleSheetsFunc.countColumns(googleSheetsDataWithGrid, stockResultsSheetsToDownload.index("Transactions - Robinhood")), googleSheetsDataWithGrid, stockResultsSheetsToDownload.index("Transactions - Robinhood"))
tranDataList.extend(tranRobinhoodDataList[1:len(tranRobinhoodDataList)])
tranDataList = [item for item in tranDataList if item[2] != 0]

chartOfAccountsDict = myGoogleSheetsFunc.createDictMapFromSheet(googleSheetsDataWithGrid, stockResultsSheetsToDownload.index("Chart of Accounts"))
tickerDict = myGoogleSheetsFunc.createDictMapFromSheet(googleSheetsDataWithGrid, stockResultsSheetsToDownload.index("Ticker Map"))

tranRowTotal = len(tranDataList)

splitTime = myPyFunc.printElapsedTime(splitTime, "Finished setting up Stock Results")


#Scrub Transactions sheet

brokerageMap = {"Mt": "Motif",
                "Rh": "Robinhood"}

multiplyFactor = 1
tranDataListAccountIndex = 1


for indexOfRow in range(1, tranRowTotal):

    tranDataList[indexOfRow][tranDataListAccountIndex] = tranDataList[indexOfRow][tranDataListAccountIndex].replace(" - " + tranDataList[indexOfRow][5], " ")
    tranDataList[indexOfRow][tranDataListAccountIndex] = tranDataList[indexOfRow][tranDataListAccountIndex].replace(
        " - " + str(tranDataList[indexOfRow][6]), " ")
    tranDataList[indexOfRow][tranDataListAccountIndex] = tranDataList[indexOfRow][tranDataListAccountIndex].replace(
        tranDataList[indexOfRow][4] + " - ", "")
    tranDataList[indexOfRow][tranDataListAccountIndex] = tranDataList[indexOfRow][tranDataListAccountIndex].rstrip()

    if tranDataList[indexOfRow][5] in brokerageMap:
        tranDataList[indexOfRow][5] = brokerageMap[tranDataList[indexOfRow][5]]

    ticker = tranDataList[indexOfRow][4]

    if ticker in tickerDict:

        for key in tickerDict[ticker]:
            tranDataList[indexOfRow][4] = tickerDict[ticker][key]

    tranDataList[indexOfRow][2] = tranDataList[indexOfRow][2] * multiplyFactor

    if tranDataList[indexOfRow][7] == "":
        tranDataList[indexOfRow][7] = 0



#use map

for indexOfRow in range(0, tranRowTotal):

    accountName = tranDataList[indexOfRow][tranDataListAccountIndex]

    for i in range(0, len(chartOfAccountsDict[accountName])):
        tranDataList[indexOfRow].insert(tranDataListAccountIndex + 1, list(chartOfAccountsDict[accountName].values())[i])

    if indexOfRow == 0:
        tranDataList[indexOfRow].append("Year")
    else:
        tranDataList[indexOfRow].append(myPyFunc.convertSerialDateToYear(tranDataList[indexOfRow][0]))



myGoogleSheetsFunc.populateSheet(2, 100, "Transactions - Scrubbed", googleSheetsAPIObj, resultsSpreadsheetID, tranDataList, False)












#############################################################################################################



stockResultsSheetsToDownload = ["Transactions - Scrubbed", "Ticker Map"]
downloadedSheetIndex = 0
resultsDownloadedWithGrid = myGoogleSheetsFunc.getDataWithGrid(resultsSpreadsheetID, googleSheetsAPIObj, stockResultsSheetsToDownload)
resultsTranScrubRowTotal = myGoogleSheetsFunc.countRows(resultsDownloadedWithGrid, stockResultsSheetsToDownload.index("Transactions - Scrubbed"))
resultsTranScrubColTotal = myGoogleSheetsFunc.countColumns(resultsDownloadedWithGrid, stockResultsSheetsToDownload.index("Transactions - Scrubbed"))
resultsTranScrubExtractedValues = myGoogleSheetsFunc.extractValues(resultsTranScrubRowTotal, resultsTranScrubColTotal, resultsDownloadedWithGrid, stockResultsSheetsToDownload.index("Transactions - Scrubbed"))

tickerMapExtractedValues = myGoogleSheetsFunc.extractValues(myGoogleSheetsFunc.countRows(resultsDownloadedWithGrid, stockResultsSheetsToDownload.index("Ticker Map")), myGoogleSheetsFunc.countColumns(resultsDownloadedWithGrid, stockResultsSheetsToDownload.index("Ticker Map")), resultsDownloadedWithGrid, stockResultsSheetsToDownload.index("Ticker Map"))
tickerMapUniqueExtractedValues = []

for stock in tickerMapExtractedValues:

    if stock[2] not in [item[2] for item in tickerMapUniqueExtractedValues]:
        tickerMapUniqueExtractedValues.append(stock)




firstFieldsDict = {0:
                       {"field": "stockName",
                        "alias": "Stock"},
                   1:
                       {"field": "broker",
                        "alias": "Broker"},
                   2:
                       {"field": "lot",
                        "alias": "Lot"}
                   }



colDict =   {
                0:  {"table": "tblResults",
                    "excludedFields": []},
                1:  {"table": "tblTickerMap",
                    "excludedFields": ["rowNumber", "stockName"]},
                2:  {"table": "tblPurchase",
                    "excludedFields": ["Stock", "Broker", "Lot"]},
                3:  {"table": "tblShares",
                    "excludedFields": ["Stock", "Broker", "Lot"]},
                4:  {"table": "tblSale",
                    "excludedFields": ["Stock", "Broker", "Lot"]}
            }



tblMainName = "tblTScrub"

columnsObj = OrderedDict()
columnsObj["tranDate"] = "date"
columnsObj["account"] = "varchar(255)"
columnsObj["accountType"] = "varchar(255)"
columnsObj["accountCategory"] = "varchar(255)"
columnsObj["amount"] = "float"
columnsObj["tranType"] = "varchar(255)"
columnsObj["stockName"] = "varchar(255)"
columnsObj["broker"] = "varchar(255)"
columnsObj["lot"] = "varchar(255)"
columnsObj["shares"] = "float"
columnsObj["dateYear"] = "int"


sqlObj = myPyFunc.createDatabase("stockResults.db", str(pathlib.Path.cwd().parents[3]/"privateData"/"stockResults"), tblMainName, columnsObj)
myPyFunc.populateTable(resultsTranScrubRowTotal, resultsTranScrubColTotal, tblMainName, resultsTranScrubExtractedValues, sqlObj["sqlCursor"], [0])


tickerColumnsObj = OrderedDict()
tickerColumnsObj["rowNumber"] = "int"
tickerColumnsObj["Ticker"] = "varchar(255)"
tickerColumnsObj["stockName"] = "varchar(255)"

myPyFunc.createTable("tblTickerMap", tickerColumnsObj, sqlObj["sqlCursor"])
myPyFunc.populateTable(len(tickerMapUniqueExtractedValues), len(tickerMapUniqueExtractedValues[0]), "tblTickerMap", tickerMapUniqueExtractedValues, sqlObj["sqlCursor"], [])



fieldAliasStr = myPyFunc.fieldsDictToStr(firstFieldsDict, True, True)
fieldStr = myPyFunc.fieldsDictToStr(firstFieldsDict, True, False)
aliasStr = myPyFunc.fieldsDictToStr(firstFieldsDict, False, True)

myPyFunc.createTableAs("tblPurchase", sqlObj["sqlCursor"], f"select {fieldAliasStr}, ltrim(strftime('%m', tranDate), '0') || '/' || ltrim(strftime('%d', tranDate), '0') || '/' || substr(strftime('%Y', tranDate), 3, 2) as 'Purchase Date', -sum(amount) as 'Capital Invested' from {tblMainName} where account = 'Cash' and tranType like '%Purchase%' and tranType not like '%Group Shares%' group by {fieldStr}, tranDate;")
myPyFunc.createTableAs("tblShares", sqlObj["sqlCursor"], f"select {fieldAliasStr}, sum(shares) as Shares from {tblMainName} where account = 'Investment Asset' and tranType like '%Purchase%' and tranType not like '%Group Shares%' group by {fieldStr};")
myPyFunc.createTableAs("tblSale", sqlObj["sqlCursor"], f"select {fieldAliasStr}, case when tranType != 'Sale - Hypothetical' then ltrim(strftime('%m', tranDate), '0') || '/' || ltrim(strftime('%d', tranDate), '0') || '/' || substr(strftime('%Y', tranDate), 3, 2) end as 'Sale Date', sum(amount) as 'Last Value', '' as 'To Sell', '=indirect(\"I\"&row())-indirect(\"F\"&row())' as 'Gain (Loss)', '=iferror(indirect(\"J\"&row())/indirect(\"F\"&row()),\"\")' as '% Gain (Loss)' from {tblMainName} where account = 'Cash' and tranType like '%Sale%' and tranType not like '%Group Shares%' group by {fieldStr}, tranDate;")

# strftime('%m/%d', tranDate) + '/' +
#get list of values to put as the pivot columns


pivotColDict = myPyFunc.createPivotColDict("dateYear", 10, "amount", 1, resultsTranScrubExtractedValues)
pivotColStr = pivotColDict["pivotColStr"]
# pp(pivotColStr)

myPyFunc.createTableAs("tblDividends", sqlObj["sqlCursor"], f"select {fieldAliasStr}, {pivotColStr} from {tblMainName} where account = 'Cash' and tranType like '%Dividend%' group by {fieldStr};")
myPyFunc.createTableAs("tblResults", sqlObj["sqlCursor"], f"select {aliasStr} from tblPurchase union select {aliasStr} from tblSale union select {aliasStr} from tblDividends;")


colListStr = myPyFunc.getAllColumns(colDict, sqlObj["sqlCursor"])
# pp(colListStr)




divColStr = ""
percentColStr = ""

for colCount in range(0, len(pivotColDict["colList"])):

    currentColName = "tblDividends.'" + str(pivotColDict["colList"][colCount]) + "'"
    divColStr = divColStr + "case when " + currentColName + " is null then '=if(or(int(left(indirect(\"R1C[0]\",false),4))<year(indirect(\"E\"&row())),int(left(indirect(\"R1C[0]\",false),4))>if(indirect(\"H\"&row())=\"\",year(today()),year(indirect(\"H\"&row())))),\"NO\",\"\")' else " + currentColName + " end as '" + str(pivotColDict["colList"][colCount]) + "'"
    # =if (
    # or (M90 <> "", and (AA$2 >= year($G90), AA$2 <= if ($H90="", year(today()), year($H90)))), iferror(M90 / $I90, 0), "")

    percentColStr = percentColStr + "'=if(or(and(indirect(\"R[0]C[-6]\",false)<>\"\",indirect(\"R[0]C[-6]\",false)<>\"NO\"),and(int(left(indirect(\"R1C[0]\",false),4))>=year(indirect(\"E\"&row())),int(left(indirect(\"R1C[0]\",false),4))<=if(indirect(\"H\"&row())=\"\",year(today()),year(indirect(\"H\"&row()))))),iferror(indirect(\"R[0]C[-6]\",false)/indirect(\"F\"&row()),0),\"\")' as '" + str(pivotColDict["colList"][colCount]) + " %'"   #int(left(indirect(\"R1C[0]\",false),4))<year(indirect(\"E\"&row())),int(left(indirect(\"R1C[0]\",false),4))>if(indirect(\"H\"&row())=\"\",year(today()),year(indirect(\"H\"&row())))),\"NO\",\"\")'

    if colCount != len(pivotColDict["colList"]) - 1:
        divColStr = divColStr + ", "
        percentColStr = percentColStr + ", "

# pp(divColStr)






sqlCommand = f"select " + colListStr + ", " + divColStr + ", '', " + percentColStr + ", ' ', '=sum(indirect(\"L\"&row()):indirect(\"Q\"&row()))' as 'Total Dividends', '' as 'Dividend Yield on Cost', '' as 'Forward Dividend', '' as 'Forward Dividend Yield', '' as '% of Portfolio' from tblResults " \
            "left outer join tblTickerMap on tblResults.Stock = tblTickerMap.stockName " \
            "left outer join tblPurchase on tblResults.Broker = tblPurchase.Broker and tblResults.Stock = tblPurchase.Stock and tblResults.Lot = tblPurchase.Lot " \
            "left outer join tblShares on tblResults.Broker = tblShares.Broker and tblResults.Stock = tblShares.Stock and tblResults.Lot = tblShares.Lot " \
            "left outer join tblSale on tblResults.Broker = tblSale.Broker and tblResults.Stock = tblSale.Stock and tblResults.Lot = tblSale.Lot " \
            "left outer join tblDividends on tblResults.Broker = tblDividends.Broker and tblResults.Stock = tblDividends.Stock and tblResults.Lot = tblDividends.Lot"

# pp("Blank line")
# pp(sqlCommand)

myPyFunc.createTableAs("tblResultsJoined", sqlObj["sqlCursor"], sqlCommand)

sqlList = ["update tblResultsJoined set 'Last Value' = '=googlefinance(indirect(\"D\"&row()))*indirect(\"G\"&row())' where tblResultsJoined.'Sale Date' is null;"]
myPyFunc.executeSQLStatements(sqlList, sqlObj["sqlCursor"])


myGoogleSheetsFunc.populateSheet(2, 1000, "SQL Query Result - Table", googleSheetsAPIObj, resultsSpreadsheetID, myPyFunc.getQueryResult("select * from tblResultsJoined order by Broker, Stock, Lot", "tblResultsJoined", sqlObj["sqlCursor"], True), True)
myPyFunc.closeDatabase(sqlObj["sqlConnection"])
