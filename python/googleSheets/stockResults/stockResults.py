import sys, pathlib
sys.path.append(str(pathlib.Path.cwd().parents[1]))
from myPyLib import myPyFunc, myGoogleSheetsFunc


splitTime = myPyFunc.printElapsedTime(False, "Starting script")

import datetime
from collections import OrderedDict
from pprint import pprint as pp

resultsSpreadsheetID = "1pjhFRIoB9mnbiMOj_hsFwsGth91l1oX_4kmeYrsT5mc"
sqlObj = myPyFunc.createDatabase("stockResults.db", str(pathlib.Path.cwd().parents[3]/"privateData"/"stockResults"))
googleSheetsAPIObj = myGoogleSheetsFunc.authFunc()

splitTime = myPyFunc.printElapsedTime(splitTime, "Finished importing modules and intializing variables")


resultsToDownload = ["Inputs", "Ticker Map", "Raw Data - Robinhood", "Transactions To Add - Robinhood", "Transactions", "Chart of Accounts"]
resultsDownloadedWithGrid = myGoogleSheetsFunc.getDataWithGrid(resultsSpreadsheetID, googleSheetsAPIObj, resultsToDownload)

inputsExtractedValues = myGoogleSheetsFunc.extractValues(myGoogleSheetsFunc.countRows(resultsDownloadedWithGrid, resultsToDownload.index("Inputs")), myGoogleSheetsFunc.countColumns(resultsDownloadedWithGrid, resultsToDownload.index("Inputs")), resultsDownloadedWithGrid, resultsToDownload.index("Inputs"))
tickerMapIndexStockName = inputsExtractedValues[0][1]


tickerMapExtractedValues = myGoogleSheetsFunc.extractValues(myGoogleSheetsFunc.countRows(resultsDownloadedWithGrid, resultsToDownload.index("Ticker Map")), myGoogleSheetsFunc.countColumns(resultsDownloadedWithGrid, resultsToDownload.index("Ticker Map")), resultsDownloadedWithGrid, resultsToDownload.index("Ticker Map"))
tickerMapTickerColIndex = 1
tickerMapStockNameColIndex = 2
tickerMapUniqueExtractedValues = []

for tickerMapItem in tickerMapExtractedValues:

    if tickerMapItem[tickerMapIndexStockName] not in [tickerMapUniqueItem[tickerMapIndexStockName] for tickerMapUniqueItem in tickerMapUniqueExtractedValues]:
        tickerMapUniqueExtractedValues.append(tickerMapItem)

tickerDict = myGoogleSheetsFunc.createDictMapFromSheet(resultsDownloadedWithGrid, resultsToDownload.index("Ticker Map"))

rawDataRobRows = myGoogleSheetsFunc.countRows(resultsDownloadedWithGrid, resultsToDownload.index("Raw Data - Robinhood"))
rawDataRobExtractedValues = myGoogleSheetsFunc.extractValues(rawDataRobRows, myGoogleSheetsFunc.countColumns(resultsDownloadedWithGrid, resultsToDownload.index("Raw Data - Robinhood")), resultsDownloadedWithGrid, resultsToDownload.index("Raw Data - Robinhood"))
transactionsToAddRobExtractedValues = myGoogleSheetsFunc.extractValues(myGoogleSheetsFunc.countRows(resultsDownloadedWithGrid, resultsToDownload.index("Transactions To Add - Robinhood")), myGoogleSheetsFunc.countColumns(resultsDownloadedWithGrid, resultsToDownload.index("Transactions To Add - Robinhood")), resultsDownloadedWithGrid, resultsToDownload.index("Transactions To Add - Robinhood"))


resultsTranScrubExtractedValues = myGoogleSheetsFunc.extractValues(myGoogleSheetsFunc.countRows(resultsDownloadedWithGrid, resultsToDownload.index("Transactions")), myGoogleSheetsFunc.countColumns(resultsDownloadedWithGrid, resultsToDownload.index("Transactions")), resultsDownloadedWithGrid, resultsToDownload.index("Transactions"))
chartOfAccountsDict = myGoogleSheetsFunc.createDictMapFromSheet(resultsDownloadedWithGrid, resultsToDownload.index("Chart of Accounts"))


splitTime = myPyFunc.printElapsedTime(splitTime, "Finished downloading and extracting data")


#create data

newTransRobListCurrColIndex = 0
newTransRobRow = []
newTransRobList = []
newTransRobListDescColIndex = 0
newTransRobListDateColIndex = 1
newTransRobListAmountColIndex = 2
newTransRobListNumSharesColIndex = 4
rawDataRobColumnIndexWithData = 0
rawDataRobLastRowIndex = rawDataRobRows - 1
newTransLengthWithoutShares = newTransRobListAmountColIndex + 1


for rawDataRobIndexOfRow in range(0, rawDataRobRows):

    rawDataRobNextCellValueHasNoShares = True
    robRawDataCurrentCellValue = rawDataRobExtractedValues[rawDataRobIndexOfRow][rawDataRobColumnIndexWithData]

    if rawDataRobIndexOfRow + 1 <= rawDataRobLastRowIndex:
        if len(str(rawDataRobExtractedValues[rawDataRobIndexOfRow + 1][rawDataRobColumnIndexWithData]).split(" share")) > 1:
            rawDataRobNextCellValueHasNoShares = False

    if newTransRobListCurrColIndex == newTransRobListAmountColIndex and robRawDataCurrentCellValue != "Failed":
        newTransRobRow.append(abs(robRawDataCurrentCellValue))
    else:
        newTransRobRow.append(robRawDataCurrentCellValue)



    if (newTransRobListCurrColIndex == newTransRobListAmountColIndex and rawDataRobNextCellValueHasNoShares) or newTransRobListCurrColIndex == 3:
        newTransRobListCurrColIndex = -1

        if len(newTransRobRow) == newTransLengthWithoutShares:
            newTransRobRow.extend(["", ""])
        elif len(newTransRobRow) == newTransRobListNumSharesColIndex:
            newTransRobRow.append(int(str(robRawDataCurrentCellValue).split(" share")[newTransRobListDescColIndex]))


        newTransRobList.append(newTransRobRow)
        newTransRobRow = []

    newTransRobListCurrColIndex = newTransRobListCurrColIndex + 1


newTransRobList.sort(key=lambda item: int(item[newTransRobListDateColIndex]))
splitTime = myGoogleSheetsFunc.populateSheet(1, 1000, "Transactions - Robinhood", googleSheetsAPIObj, resultsSpreadsheetID, newTransRobList, True, dontPopulateSheet=True)



#create transactions

tranRobDoubleEntryList = [["Date", "Account", "Amount+-", "Transaction Type", "Stock Name", "Broker", "Lot", "Shares", "Ticker", "Capital Invested"]]
tranRobDoubleEntryList.extend(transactionsToAddRobExtractedValues[1:])


leftStrMap = {
                "Dividend from ": {"transactionType": "Dividend", "debitAccount": "Cash", "creditAccount": "Dividend Revenue"},
                "Withdrawal to ": {"transactionType": "Owners - Pay", "debitAccount": "Capital Contributions", "creditAccount": "Cash", "stockName": "All Stocks", "lotInfo": "All Lots"},
                "Deposit from ": {"transactionType": "Owners - Receive Cash", "debitAccount": "Cash", "creditAccount": "Capital Contributions", "stockName": "All Stocks", "lotInfo": "All Lots"},
                "Interest Payment": {"transactionType": "Interest", "debitAccount": "Cash", "creditAccount": "Interest Revenue", "stockName": "Cash", "lotInfo": "Cash"},
                "AKS from Robinhood": {"transactionType": "Purchase - Stock Gift", "debitAccount": "Investment Asset", "creditAccount": "Gain On Gift", "stockName": "AKS", "shares": 1}
}

rightStrMap = {" Market Buy": {"transactionType": "Purchase", "debitAccount": "Investment Asset", "creditAccount": "Cash"}}


lastDate = int(myPyFunc.convertDateToSerialDate(datetime.datetime(2013, 10, 31)))    # lastDate = int(myPyFunc.convertDateToSerialDate(datetime.datetime(2018, 10, 31)))


for line in newTransRobList:

    if line[newTransRobListAmountColIndex] != "Failed" and line[newTransRobListDateColIndex] > lastDate:

        mappedTransactionData = {}

        for leftStringToCheckFor in leftStrMap:
            if line[newTransRobListDescColIndex][:len(leftStringToCheckFor)] == leftStringToCheckFor:
                mappedTransactionData = leftStrMap[leftStringToCheckFor]
                mappedTransactionData["strToCheckFor"] = leftStringToCheckFor
                mappedTransactionData["stockNamePosition"] = 1

        if not mappedTransactionData:
            for rightStrToCheckFor in rightStrMap:
                if line[newTransRobListDescColIndex][-len(rightStrToCheckFor):] == rightStrToCheckFor:
                    mappedTransactionData = rightStrMap[rightStrToCheckFor]
                    mappedTransactionData["strToCheckFor"] = rightStrToCheckFor
                    mappedTransactionData["stockNamePosition"] = 0

        # pp(transaction)

        if "stockName" in mappedTransactionData:
            stockName = mappedTransactionData["stockName"]
        elif line[newTransRobListDescColIndex].split(mappedTransactionData["strToCheckFor"])[mappedTransactionData["stockNamePosition"]] in ["Xperi", "Tessera Technologies, Inc. - Common Stock"]:
            stockName = "Xperi, formerly Tessera"
        else:
            stockName = line[newTransRobListDescColIndex].split(mappedTransactionData["strToCheckFor"])[mappedTransactionData["stockNamePosition"]]


        if "lotInfo" in mappedTransactionData:
            lot = mappedTransactionData["lotInfo"]
        elif mappedTransactionData["transactionType"] in ["Purchase", "Purchase - Stock Gift", "Purchase - Stock From Merger"]:
            lot = myPyFunc.convertSerialDateToDateWithoutDashes(line[newTransRobListDateColIndex])
        else:

            filterForLots = [{1: "Investment Asset", 3: "Purchase", 4: stockName},
                             {1: "Investment Asset", 3: "Purchase - Stock From Merger", 4: stockName}]
            filteredList = myPyFunc.filterListOfLists(tranRobDoubleEntryList, filterForLots)

            if len(filteredList) == 1:
                lot = myPyFunc.convertSerialDateToDateWithoutDashes(filteredList[0][0])


        if "shares" in mappedTransactionData:
            shares = mappedTransactionData["shares"]
        else:
            shares = line[newTransRobListNumSharesColIndex]

        tranRobDoubleEntryList.append([line[newTransRobListDateColIndex], mappedTransactionData["debitAccount"], line[newTransRobListAmountColIndex], mappedTransactionData["transactionType"], stockName, "Robinhood", lot, shares, "", ""])
        tranRobDoubleEntryList.append([line[newTransRobListDateColIndex], mappedTransactionData["creditAccount"], -line[newTransRobListAmountColIndex], mappedTransactionData["transactionType"], stockName, "Robinhood", lot, "", "", ""])



splitTime = myPyFunc.printElapsedTime(splitTime, "Finished creating Robinhood double entry transactions")




columnsObj = myPyFunc.createColumnsDict([
    {"tranDate": "date"},
    {"accountName": "varchar(255)"},
    {"amount": "float"},
    {"transactionType": "varchar(255)"},
    {"stockName": "varchar(255)"},
    {"broker": "varchar(255)"},
    {"lot": "varchar(255)"},
    {"shares": "float"},
    {"ticker": "varchar(255)"},
    {"capitalInvested": "varchar(255)"}
])




#
# tickerColumnsObj = OrderedDict()
# tickerColumnsObj["rowNumber"] = "int"
# tickerColumnsObj["Ticker"] = "varchar(255)"
# tickerColumnsObj["stockName"] = "varchar(255)"
#
# myPyFunc.createTable("tblTickerMap", tickerColumnsObj, sqlObj["sqlCursor"])
# myPyFunc.populateTable(len(tickerMapUniqueExtractedValues), len(tickerMapUniqueExtractedValues[0]), "tblTickerMap", tickerMapUniqueExtractedValues, sqlObj["sqlCursor"], [])
# pp(myPyFunc.getQueryResult("select * from tblTickerMap", "tblTickerMap", sqlObj["sqlCursor"], False))


myPyFunc.createAndPopulateTable("tblStockResultsRobinhood", columnsObj, sqlObj["sqlCursor"], len(tranRobDoubleEntryList), len(tranRobDoubleEntryList[0]), tranRobDoubleEntryList, [0])



myPyFunc.createTableAs("tblLots", sqlObj["sqlCursor"], f"select stockName, lot, sum(amount), sum(shares) from tblStockResultsRobinhood where accountName = 'Investment Asset' and broker = 'Robinhood' group by stockName, lot having sum(shares) > 0;")
unsoldStockValuesList = myPyFunc.getQueryResult("select * from tblLots;", sqlObj["sqlCursor"], False)
# myGoogleSheetsFunc.populateSheet(1, 1000, "Lots", googleSheetsAPIObj, resultsSpreadsheetID, unsoldStockValuesList2, True)


# sqlCommand = f"select tblLots.*, tblTickerMap.ticker, '=googlefinance(indirect(\"E\"&row()))*indirect(\"D\"&row())' as googleFin, '=indirect(\"F\"&row())-indirect(\"C\"&row())' as gainLoss from tblLots left outer join tblTickerMap on tblLots.stockName = tblTickerMap.stockName;"
# myGoogleSheetsFunc.populateSheet(3, 1000, "Unsold Stock Values - Robinhood", googleSheetsAPIObj, resultsSpreadsheetID, myPyFunc.getQueryResult(sqlCommand, sqlObj["sqlCursor"], False), True)



tranType = "Sale - Hypothetical"
priceDate = int(myPyFunc.convertDateToSerialDate(datetime.datetime.now()))
# unsoldStockValuesDataWithGrid = myGoogleSheetsFunc.getDataWithGrid(resultsSpreadsheetID, googleSheetsAPIObj, ["Unsold Stock Values - Robinhood"])
# unsoldStockValuesList = myGoogleSheetsFunc.extractValues(myGoogleSheetsFunc.countRows(unsoldStockValuesDataWithGrid, 0), myGoogleSheetsFunc.countColumns(unsoldStockValuesDataWithGrid, 0), unsoldStockValuesDataWithGrid, 0)


# doubleEntryUnsoldStockList = []

#
# for lot in unsoldStockValuesList:
#
#     doubleEntryUnsoldStockList.append([priceDate, "Cash", lot[5], tranType, lot[0], "Robinhood", lot[1], "", "", ""])
#     doubleEntryUnsoldStockList.append([priceDate, "Investment Asset", -lot[2], tranType, lot[0], "Robinhood", lot[1], lot[3], "", ""])
#
#     if lot[6] < 0:
#         gainLossAccount = "Loss On Sale - Hypothetical"
#     else:
#         gainLossAccount = "Gain On Sale - Hypothetical"
#
#     doubleEntryUnsoldStockList.append([priceDate, gainLossAccount, -lot[6], tranType, lot[0], "Robinhood", lot[1], "", "", ""])
#




doubleEntryUnsoldStockList = []


for line in unsoldStockValuesList:

    lotStockName = line[0]
    lotFromLotList = line[1]
    lotInvestmentAmount = line[2]
    lotShares = line[3]
    tickerSymbol = ""

    for ticker in tickerMapUniqueExtractedValues:
        if lotStockName == ticker[tickerMapStockNameColIndex]:
            tickerSymbol = ticker[tickerMapTickerColIndex]


    lotCurrentAmount = "googlefinance(indirect(\"I\"&row()))*indirect(\"H\"&row())"

    doubleEntryUnsoldStockList.append([priceDate, "Cash", "=" + lotCurrentAmount, tranType, lotStockName, "Robinhood", lotFromLotList, lotShares, tickerSymbol, ""])
    doubleEntryUnsoldStockList.append([priceDate, "Investment Asset", -lotInvestmentAmount, tranType, lotStockName, "Robinhood", lotFromLotList, lotShares, tickerSymbol, ""])

    doubleEntryUnsoldStockList.append([priceDate, "=if(indirect(\"C\"&row())<0,\"Gain On Sale - Hypothetical\",\"Loss On Sale - Hypothetical\")", "=-" + lotCurrentAmount + "+" + "indirect(\"J\"&row())", tranType, lotStockName, "Robinhood", lotFromLotList, lotShares, tickerSymbol, lotInvestmentAmount])



splitTime = myGoogleSheetsFunc.populateSheet(2, 1000, "Transactions - Unsold Stock", googleSheetsAPIObj, resultsSpreadsheetID, doubleEntryUnsoldStockList, True, dontPopulateSheet=True)



tranRobDoubleEntryList.extend(doubleEntryUnsoldStockList)
splitTime = myGoogleSheetsFunc.populateSheet(2, 1000, "Transactions - Robinhood - Double Entry", googleSheetsAPIObj, resultsSpreadsheetID, tranRobDoubleEntryList, True, dontPopulateSheet=True)


###################################################################################################################


tranDateColIndex = 0
tranAccountColIndex = 1
tranAmountColIndex = 2
tranStockColIndex = 4
tranBrokerColIndex = 5
tranLotColIndex = 6
tranSharesColIndex = 7



resultsTranScrubExtractedValues.extend(tranRobDoubleEntryList[1:len(tranRobDoubleEntryList)])
resultsTranScrubList = resultsTranScrubExtractedValues
resultsTranScrubList = [item for item in resultsTranScrubList if item[tranAmountColIndex] != 0]
resultsTranScrubRowTotal = len(resultsTranScrubList)




#Scrub Transactions sheet

brokerageMap = {"Mt": "Motif",
                "Rh": "Robinhood"}

multiplyFactor = 1



for resultsTranScrubIndexOfRow in range(1, resultsTranScrubRowTotal):

    resultsTranScrubList[resultsTranScrubIndexOfRow][tranAccountColIndex] = resultsTranScrubList[resultsTranScrubIndexOfRow][tranAccountColIndex].replace(" - " + resultsTranScrubList[resultsTranScrubIndexOfRow][tranBrokerColIndex], " ")
    resultsTranScrubList[resultsTranScrubIndexOfRow][tranAccountColIndex] = resultsTranScrubList[resultsTranScrubIndexOfRow][tranAccountColIndex].replace(
        " - " + str(resultsTranScrubList[resultsTranScrubIndexOfRow][tranLotColIndex]), " ")
    resultsTranScrubList[resultsTranScrubIndexOfRow][tranAccountColIndex] = resultsTranScrubList[resultsTranScrubIndexOfRow][tranAccountColIndex].replace(
        resultsTranScrubList[resultsTranScrubIndexOfRow][tranStockColIndex] + " - ", "")
    resultsTranScrubList[resultsTranScrubIndexOfRow][tranAccountColIndex] = resultsTranScrubList[resultsTranScrubIndexOfRow][tranAccountColIndex].rstrip()

    if resultsTranScrubList[resultsTranScrubIndexOfRow][tranBrokerColIndex] in brokerageMap:
        resultsTranScrubList[resultsTranScrubIndexOfRow][tranBrokerColIndex] = brokerageMap[resultsTranScrubList[resultsTranScrubIndexOfRow][tranBrokerColIndex]]

    ticker = resultsTranScrubList[resultsTranScrubIndexOfRow][tranStockColIndex]

    if ticker in tickerDict:

        for key in tickerDict[ticker]:
            resultsTranScrubList[resultsTranScrubIndexOfRow][tranStockColIndex] = tickerDict[ticker][key]

    resultsTranScrubList[resultsTranScrubIndexOfRow][tranAmountColIndex] = resultsTranScrubList[resultsTranScrubIndexOfRow][tranAmountColIndex] * multiplyFactor

    if resultsTranScrubList[resultsTranScrubIndexOfRow][tranSharesColIndex] == "":
        resultsTranScrubList[resultsTranScrubIndexOfRow][tranSharesColIndex] = 0



#use map

# pp(chartOfAccountsDict)

# for resultsTranScrubIndexOfRow in range(0, resultsTranScrubRowTotal):
#
#     accountName = resultsTranScrubList[resultsTranScrubIndexOfRow][tranAccountColIndex]
#
#     for indexOfAccountChartOfAccountsDict in range(0, len(chartOfAccountsDict[accountName])):
#         resultsTranScrubList[resultsTranScrubIndexOfRow].insert(tranAccountColIndex + 1, list(chartOfAccountsDict[accountName].values())[indexOfAccountChartOfAccountsDict])
#
#     if resultsTranScrubIndexOfRow == 0:
#         resultsTranScrubList[resultsTranScrubIndexOfRow].append("Year")
#     else:
#         resultsTranScrubList[resultsTranScrubIndexOfRow].append(myPyFunc.convertSerialDateToYear(resultsTranScrubList[resultsTranScrubIndexOfRow][tranDateColIndex]))
#


# splitTime = myGoogleSheetsFunc.populateSheet(2, 1000, "Transactions - Scrubbed", googleSheetsAPIObj, resultsSpreadsheetID, resultsTranScrubList, False, splitTimeArg=splitTime)
#
#
#
#
# resultsTranScrubRowTotal = len(resultsTranScrubList)
# resultsTranScrubColTotal = len(resultsTranScrubList[0])
#
#
#
#
# firstFieldsDict = {0:
#                        {"field": "stockName",
#                         "alias": "Stock"},
#                    1:
#                        {"field": "broker",
#                         "alias": "Broker"},
#                    2:
#                        {"field": "lot",
#                         "alias": "Lot"}
#                    }
#
#
#
# colDict =   {
#                 0:  {"table": "tblResults",
#                     "excludedFields": []},
#                 1:  {"table": "tblTickerMap",
#                     "excludedFields": ["rowNumber", "stockName"]},
#                 2:  {"table": "tblPurchase",
#                     "excludedFields": ["Stock", "Broker", "Lot"]},
#                 3:  {"table": "tblShares",
#                     "excludedFields": ["Stock", "Broker", "Lot"]},
#                 4:  {"table": "tblSale",
#                     "excludedFields": ["Stock", "Broker", "Lot"]}
#             }
#
#
#
#
#
# columnsObj = OrderedDict()
# columnsObj["tranDate"] = "date"
# columnsObj["account"] = "varchar(255)"
# columnsObj["accountType"] = "varchar(255)"
# columnsObj["accountCategory"] = "varchar(255)"
# columnsObj["amount"] = "float"
# columnsObj["tranType"] = "varchar(255)"
# columnsObj["stockName"] = "varchar(255)"
# columnsObj["broker"] = "varchar(255)"
# columnsObj["lot"] = "varchar(255)"
# columnsObj["shares"] = "float"
# columnsObj["ticker"] = "varchar(255)"
# columnsObj["capitalInvested"] = "varchar(255)"
# columnsObj["dateYear"] = "int"
#
# tblMainName = "tblTScrub"
# myPyFunc.createTable(tblMainName, columnsObj, sqlObj["sqlCursor"])
#
#
# myPyFunc.populateTable(resultsTranScrubRowTotal, resultsTranScrubColTotal, tblMainName, resultsTranScrubList, sqlObj["sqlCursor"], [0])
#
#
# tickerColumnsObj = OrderedDict()
# tickerColumnsObj["rowNumber"] = "int"
# tickerColumnsObj["Ticker"] = "varchar(255)"
# tickerColumnsObj["stockName"] = "varchar(255)"
#
# myPyFunc.createTable("tblTickerMap", tickerColumnsObj, sqlObj["sqlCursor"])
# myPyFunc.populateTable(len(tickerMapUniqueExtractedValues), len(tickerMapUniqueExtractedValues[0]), "tblTickerMap", tickerMapUniqueExtractedValues, sqlObj["sqlCursor"], [])
#
#
#
# fieldAliasStr = myPyFunc.fieldsDictToStr(firstFieldsDict, True, True)
# fieldStr = myPyFunc.fieldsDictToStr(firstFieldsDict, True, False)
# aliasStr = myPyFunc.fieldsDictToStr(firstFieldsDict, False, True)
#
# myPyFunc.createTableAs("tblPurchase", sqlObj["sqlCursor"], f"select {fieldAliasStr}, ltrim(strftime('%m', tranDate), '0') || '/' || ltrim(strftime('%d', tranDate), '0') || '/' || substr(strftime('%Y', tranDate), 3, 2) as 'Purchase Date', -sum(amount) as 'Capital Invested' from {tblMainName} where account = 'Cash' and tranType like '%Purchase%' and tranType not like '%Group Shares%' group by {fieldStr}, tranDate;")
# myPyFunc.createTableAs("tblShares", sqlObj["sqlCursor"], f"select {fieldAliasStr}, sum(shares) as Shares from {tblMainName} where account = 'Investment Asset' and tranType like '%Purchase%' and tranType not like '%Group Shares%' group by {fieldStr};")
# myPyFunc.createTableAs("tblSale", sqlObj["sqlCursor"], f"select {fieldAliasStr}, case when tranType != 'Sale - Hypothetical' then ltrim(strftime('%m', tranDate), '0') || '/' || ltrim(strftime('%d', tranDate), '0') || '/' || substr(strftime('%Y', tranDate), 3, 2) end as 'Sale Date', sum(amount) as 'Last Value', '' as 'To Sell', '=indirect(\"I\"&row())-indirect(\"F\"&row())' as 'Gain (Loss)', '=iferror(indirect(\"J\"&row())/indirect(\"F\"&row()),\"\")' as '% Gain (Loss)' from {tblMainName} where account = 'Cash' and tranType like '%Sale%' and tranType not like '%Group Shares%' group by {fieldStr}, tranDate;")
#
# # strftime('%m/%d', tranDate) + '/' +
# #get list of values to put as the pivot columns
#
#
# pivotColDict = myPyFunc.createPivotColDict("dateYear", 10, "amount", 1, resultsTranScrubList)
# pivotColStr = pivotColDict["pivotColStr"]
# # pp(pivotColStr)
#
# myPyFunc.createTableAs("tblDividends", sqlObj["sqlCursor"], f"select {fieldAliasStr}, {pivotColStr} from {tblMainName} where account = 'Cash' and tranType like '%Dividend%' group by {fieldStr};")
# myPyFunc.createTableAs("tblResults", sqlObj["sqlCursor"], f"select {aliasStr} from tblPurchase union select {aliasStr} from tblSale union select {aliasStr} from tblDividends;")
#
#
# colListStr = myPyFunc.getAllColumns(colDict, sqlObj["sqlCursor"])
# # pp(colListStr)
#
#
#
#
# divColStr = ""
# percentColStr = ""
#
# for colCount in range(0, len(pivotColDict["colList"])):
#
#     currentColName = "tblDividends.'" + str(pivotColDict["colList"][colCount]) + "'"
#     divColStr = divColStr + "case when " + currentColName + " is null then '=if(or(int(left(indirect(\"R1C[0]\",false),4))<year(indirect(\"E\"&row())),int(left(indirect(\"R1C[0]\",false),4))>if(indirect(\"H\"&row())=\"\",year(today()),year(indirect(\"H\"&row())))),\"NO\",\"\")' else " + currentColName + " end as '" + str(pivotColDict["colList"][colCount]) + "'"
#     # =if (
#     # or (M90 <> "", and (AA$2 >= year($G90), AA$2 <= if ($H90="", year(today()), year($H90)))), iferror(M90 / $I90, 0), "")
#
#     percentColStr = percentColStr + "'=if(or(and(indirect(\"R[0]C[-6]\",false)<>\"\",indirect(\"R[0]C[-6]\",false)<>\"NO\"),and(int(left(indirect(\"R1C[0]\",false),4))>=year(indirect(\"E\"&row())),int(left(indirect(\"R1C[0]\",false),4))<=if(indirect(\"H\"&row())=\"\",year(today()),year(indirect(\"H\"&row()))))),iferror(indirect(\"R[0]C[-6]\",false)/indirect(\"F\"&row()),0),\"\")' as '" + str(pivotColDict["colList"][colCount]) + " %'"   #int(left(indirect(\"R1C[0]\",false),4))<year(indirect(\"E\"&row())),int(left(indirect(\"R1C[0]\",false),4))>if(indirect(\"H\"&row())=\"\",year(today()),year(indirect(\"H\"&row())))),\"NO\",\"\")'
#
#     if colCount != len(pivotColDict["colList"]) - 1:
#         divColStr = divColStr + ", "
#         percentColStr = percentColStr + ", "
#
# # pp(divColStr)
#
#
#
#
#
#
# sqlCommand = f"select " + colListStr + ", " + divColStr + ", '', " + percentColStr + ", ' ', '=sum(indirect(\"L\"&row()):indirect(\"Q\"&row()))' as 'Total Dividends', '' as 'Dividend Yield on Cost', '' as 'Forward Dividend', '' as 'Forward Dividend Yield', '' as '% of Portfolio' from tblResults " \
#             "left outer join tblTickerMap on tblResults.Stock = tblTickerMap.stockName " \
#             "left outer join tblPurchase on tblResults.Broker = tblPurchase.Broker and tblResults.Stock = tblPurchase.Stock and tblResults.Lot = tblPurchase.Lot " \
#             "left outer join tblShares on tblResults.Broker = tblShares.Broker and tblResults.Stock = tblShares.Stock and tblResults.Lot = tblShares.Lot " \
#             "left outer join tblSale on tblResults.Broker = tblSale.Broker and tblResults.Stock = tblSale.Stock and tblResults.Lot = tblSale.Lot " \
#             "left outer join tblDividends on tblResults.Broker = tblDividends.Broker and tblResults.Stock = tblDividends.Stock and tblResults.Lot = tblDividends.Lot"
#
# # pp("Blank line")
# # pp(sqlCommand)
#
# myPyFunc.createTableAs("tblResultsJoined", sqlObj["sqlCursor"], sqlCommand)
#
# sqlList = ["update tblResultsJoined set 'Last Value' = '=googlefinance(indirect(\"D\"&row()))*indirect(\"G\"&row())' where tblResultsJoined.'Sale Date' is null;"]
# myPyFunc.executeSQLStatements(sqlList, sqlObj["sqlCursor"])
#
#
# splitTime = myGoogleSheetsFunc.populateSheet(2, 1000, "SQL Query Result - Table", googleSheetsAPIObj, resultsSpreadsheetID, myPyFunc.getQueryResult("select * from tblResultsJoined order by Broker, Stock, Lot", sqlObj["sqlCursor"], True), True, splitTimeArg=splitTime)
#
# splitTime = myGoogleSheetsFunc.populateSheet(2, 1000, "SQL Query Result - Balance Sheet", googleSheetsAPIObj, resultsSpreadsheetID, myPyFunc.getQueryResult("select * from tblResultsJoined order by Broker, Stock, Lot", sqlObj["sqlCursor"], True), True, splitTimeArg=splitTime)
#


myPyFunc.closeDatabase(sqlObj["sqlConnection"])
splitTime = myPyFunc.printElapsedTime(splitTime, "Finished with database")