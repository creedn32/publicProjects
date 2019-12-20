import sys, pathlib
sys.path.append(str(pathlib.Path.cwd().parents[1]))
from myPyLib import myPyFunc, myGoogleSheetsFunc


splitTime = myPyFunc.printElapsedTime(False, "Starting script")

import datetime
from collections import OrderedDict
from pprint import pprint as pp

resultsSpreadsheetID = "1pjhFRIoB9mnbiMOj_hsFwsGth91l1oX_4kmeYrsT5mc"
sqlObj = myPyFunc.createDatabase("stockResults.db", str(pathlib.Path.cwd().parents[3]/"privateData"/"stockResults"))
sqlCursor = sqlObj["sqlCursor"]
googleSheetsAPIObj = myGoogleSheetsFunc.authFunc()

splitTime = myPyFunc.printElapsedTime(splitTime, "Finished importing modules and intializing variables")


resultsToDownload = ["Inputs", "Ticker Map", "Raw Data - Robinhood", "Transactions To Add - Robinhood", "Transactions - Motif", "Chart of Accounts"]
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

# tickerDict = myGoogleSheetsFunc.createDictMapFromSheet(resultsDownloadedWithGrid, resultsToDownload.index("Ticker Map"))

rawDataRobRows = myGoogleSheetsFunc.countRows(resultsDownloadedWithGrid, resultsToDownload.index("Raw Data - Robinhood"))
rawDataRobExtractedValues = myGoogleSheetsFunc.extractValues(rawDataRobRows, myGoogleSheetsFunc.countColumns(resultsDownloadedWithGrid, resultsToDownload.index("Raw Data - Robinhood")), resultsDownloadedWithGrid, resultsToDownload.index("Raw Data - Robinhood"))
transactionsToAddRobExtractedValues = myGoogleSheetsFunc.extractValues(myGoogleSheetsFunc.countRows(resultsDownloadedWithGrid, resultsToDownload.index("Transactions To Add - Robinhood")), myGoogleSheetsFunc.countColumns(resultsDownloadedWithGrid, resultsToDownload.index("Transactions To Add - Robinhood")), resultsDownloadedWithGrid, resultsToDownload.index("Transactions To Add - Robinhood"))

resultsTranScrubList = myGoogleSheetsFunc.extractValues(myGoogleSheetsFunc.countRows(resultsDownloadedWithGrid, resultsToDownload.index("Transactions - Motif")), myGoogleSheetsFunc.countColumns(resultsDownloadedWithGrid, resultsToDownload.index("Transactions - Motif")), resultsDownloadedWithGrid, resultsToDownload.index("Transactions - Motif"))
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
splitTime = myGoogleSheetsFunc.populateSheet(1, 1000, "Transactions - Robinhood", googleSheetsAPIObj, resultsSpreadsheetID, newTransRobList, True, writeToSheet=False, splitTimeArg=splitTime)



#create transactions

tranRobDoubleEntryList = [["Date", "Account", "Amount+-", "Transaction Type", "Stock Name", "Broker", "Lot", "Shares", "Ticker", "Capital Invested"]]
tranRobDoubleEntryList.extend(transactionsToAddRobExtractedValues[1:])


leftStrMap = {
                "Dividend from ": {"tranType": "Dividend", "debitAccount": "Cash", "creditAccount": "Dividend Revenue"},
                "Withdrawal to ": {"tranType": "Owners - Pay", "debitAccount": "Capital Contributions", "creditAccount": "Cash", "stockName": "All Stocks", "lotInfo": "All Lots"},
                "Deposit from ": {"tranType": "Owners - Receive Cash", "debitAccount": "Cash", "creditAccount": "Capital Contributions", "stockName": "All Stocks", "lotInfo": "All Lots"},
                "Interest Payment": {"tranType": "Interest", "debitAccount": "Cash", "creditAccount": "Interest Revenue", "stockName": "Cash", "lotInfo": "Cash"},
                "AKS from Robinhood": {"tranType": "Purchase - Stock Gift", "debitAccount": "Investment Asset", "creditAccount": "Gain On Gift", "stockName": "AKS", "shares": 1}
}

rightStrMap = {" Market Buy": {"tranType": "Purchase", "debitAccount": "Investment Asset", "creditAccount": "Cash"}}


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
        elif mappedTransactionData["tranType"] in ["Purchase", "Purchase - Stock Gift", "Purchase - Stock From Merger"]:
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

        tranRobDoubleEntryList.append([line[newTransRobListDateColIndex], mappedTransactionData["debitAccount"], line[newTransRobListAmountColIndex], mappedTransactionData["tranType"], stockName, "Robinhood", lot, shares, "", ""])
        tranRobDoubleEntryList.append([line[newTransRobListDateColIndex], mappedTransactionData["creditAccount"], -line[newTransRobListAmountColIndex], mappedTransactionData["tranType"], stockName, "Robinhood", lot, "", "", ""])



splitTime = myPyFunc.printElapsedTime(splitTime, "Finished creating Robinhood double entry transactions")




tblRobinhoodColumns = myPyFunc.createColumnsDict([
    {"\"Date\"": "date"},
    {"\"Account\"": "varchar(255)"},
    {"\"Amount+-\"": "float"},
    {"\"Transaction Type\"": "varchar(255)"},
    {"\"Stock Name\"": "varchar(255)"},
    {"\"Broker\"": "varchar(255)"},
    {"\"Lot\"": "varchar(255)"},
    {"\"Shares\"": "float"},
    {"\"Ticker\"": "varchar(255)"},
    {"\"Capital Invested\"": "varchar(255)"}
])




#
# tickerColumnsObj = OrderedDict()
# tickerColumnsObj["rowNumber"] = "int"
# tickerColumnsObj["Ticker"] = "varchar(255)"
# tickerColumnsObj["stockName"] = "varchar(255)"
#
# myPyFunc.createTable("tblTickerMap", tickerColumnsObj, sqlCursor)
# myPyFunc.populateTable(len(tickerMapUniqueExtractedValues), len(tickerMapUniqueExtractedValues[0]), "tblTickerMap", tickerMapUniqueExtractedValues, sqlCursor, [])
# pp(myPyFunc.getQueryResult("select * from tblTickerMap", "tblTickerMap", sqlCursor, False))


myPyFunc.createAndPopulateTable("tblRobinhood", tblRobinhoodColumns, sqlCursor, len(tranRobDoubleEntryList), len(tranRobDoubleEntryList[0]), tranRobDoubleEntryList, [0])



# myPyFunc.createTableAs("tblLots", sqlCursor, f"select stockName, lot, sum(amount), sum(shares) from tblRobinhood where account = 'Investment Asset' and broker = 'Robinhood' group by stockName, lot having sum(shares) > 0;")
unsoldStockValuesList = myPyFunc.getQueryResult("select \"Stock\", \"Lot\", sum(\"Amount+-\"), sum(\"Shares\") from tblRobinhood where \"Account\" = 'Investment Asset' and \"Broker\" = 'Robinhood' group by \"Stock\", \"Lot\" having sum(\"Shares\") > 0;", sqlCursor, False)
# myGoogleSheetsFunc.populateSheet(1, 1000, "Lots", googleSheetsAPIObj, resultsSpreadsheetID, unsoldStockValuesList2, True)


# sqlCommand = f"select tblLots.*, tblTickerMap.ticker, '=googlefinance(indirect(\"E\"&row()))*indirect(\"D\"&row())' as googleFin, '=indirect(\"F\"&row())-indirect(\"C\"&row())' as gainLoss from tblLots left outer join tblTickerMap on tblLots.stockName = tblTickerMap.stockName;"
# myGoogleSheetsFunc.populateSheet(3, 1000, "Unsold Stock Values - Robinhood", googleSheetsAPIObj, resultsSpreadsheetID, myPyFunc.getQueryResult(sqlCommand, sqlCursor, False), True)



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
tranType = "Sale - Hypothetical"
priceDate = int(myPyFunc.convertDateToSerialDate(datetime.datetime.now()))
gainLossAccount = "=if(indirect(\"r[0]c[1]\",false)<0,\"Gain On Sale - Hypothetical\",\"Loss On Sale - Hypothetical\")"


for line in unsoldStockValuesList:

    lotStockName = line[0]
    lotFromLotList = line[1]
    lotInvestmentAmount = line[2]
    lotShares = line[3]
    tickerSymbol = ""

    for ticker in tickerMapUniqueExtractedValues:
        if lotStockName == ticker[tickerMapStockNameColIndex]:
            tickerSymbol = ticker[tickerMapTickerColIndex]


    lotCurrentAmount = "googlefinance(indirect(\"r[0]c[6]\",false))*indirect(\"r[0]c[5]\",false)"

    doubleEntryUnsoldStockList.append([priceDate, "Cash", "=" + lotCurrentAmount, tranType, lotStockName, "Robinhood", lotFromLotList, lotShares, tickerSymbol, ""])
    doubleEntryUnsoldStockList.append([priceDate, "Investment Asset", -lotInvestmentAmount, tranType, lotStockName, "Robinhood", lotFromLotList, lotShares, tickerSymbol, ""])
    doubleEntryUnsoldStockList.append([priceDate, gainLossAccount, "=-" + lotCurrentAmount + "+" + "indirect(\"r[0]c[7]\",false)", tranType, lotStockName, "Robinhood", lotFromLotList, lotShares, tickerSymbol, lotInvestmentAmount])



tranRobDoubleEntryList.extend(doubleEntryUnsoldStockList)
splitTime = myGoogleSheetsFunc.populateSheet(2, 1000, "Transactions - Robinhood - Double Entry", googleSheetsAPIObj, resultsSpreadsheetID, tranRobDoubleEntryList, True, writeToSheet=False, splitTimeArg=splitTime)



tranDateColIndex = 0
tranAccountColIndex = 1
# tranAmountColIndex = 2
# tranStockColIndex = 4
# tranBrokerColIndex = 5
# tranLotColIndex = 6
# tranSharesColIndex = 7



# resultsTranScrubList = transMotifExtractedValues
# resultsTranScrubList = [item for item in resultsTranScrubList if item[tranAmountColIndex] != 0]




#Scrub Transactions sheet

# brokerageMap = {"Mt": "Motif",
#                 "Rh": "Robinhood"}
#
# multiplyFactor = 1



# for resultsTranScrubIndexOfRow in range(1, resultsTranScrubRowTotal):

    # resultsTranScrubList[resultsTranScrubIndexOfRow][tranAccountColIndex] = resultsTranScrubList[resultsTranScrubIndexOfRow][tranAccountColIndex].replace(" - " + resultsTranScrubList[resultsTranScrubIndexOfRow][tranBrokerColIndex], " ")
    # resultsTranScrubList[resultsTranScrubIndexOfRow][tranAccountColIndex] = resultsTranScrubList[resultsTranScrubIndexOfRow][tranAccountColIndex].replace(
    #     " - " + str(resultsTranScrubList[resultsTranScrubIndexOfRow][tranLotColIndex]), " ")
    # resultsTranScrubList[resultsTranScrubIndexOfRow][tranAccountColIndex] = resultsTranScrubList[resultsTranScrubIndexOfRow][tranAccountColIndex].replace(
    #     resultsTranScrubList[resultsTranScrubIndexOfRow][tranStockColIndex] + " - ", "")
    # resultsTranScrubList[resultsTranScrubIndexOfRow][tranAccountColIndex] = resultsTranScrubList[resultsTranScrubIndexOfRow][tranAccountColIndex].rstrip()
    #
    # if resultsTranScrubList[resultsTranScrubIndexOfRow][tranBrokerColIndex] in brokerageMap:
    #     resultsTranScrubList[resultsTranScrubIndexOfRow][tranBrokerColIndex] = brokerageMap[resultsTranScrubList[resultsTranScrubIndexOfRow][tranBrokerColIndex]]

    # ticker = resultsTranScrubList[resultsTranScrubIndexOfRow][tranStockColIndex]

    # if ticker in tickerDict:
    #
    #     for key in tickerDict[ticker]:
    #         resultsTranScrubList[resultsTranScrubIndexOfRow][tranStockColIndex] = tickerDict[ticker][key]

    # resultsTranScrubList[resultsTranScrubIndexOfRow][tranAmountColIndex] = resultsTranScrubList[resultsTranScrubIndexOfRow][tranAmountColIndex] * multiplyFactor
    #
    # if resultsTranScrubList[resultsTranScrubIndexOfRow][tranSharesColIndex] == "":
    #     resultsTranScrubList[resultsTranScrubIndexOfRow][tranSharesColIndex] = 0


# splitTime = myGoogleSheetsFunc.populateSheet(1, 1000, "1", googleSheetsAPIObj, resultsSpreadsheetID, resultsTranScrubList, True)

resultsTranScrubList.extend(tranRobDoubleEntryList[1:len(tranRobDoubleEntryList)])
resultsTranScrubRowTotal = len(resultsTranScrubList)
accountDataPointsToMap = 2




#use map


for resultsTranScrubIndexOfRow in range(0, resultsTranScrubRowTotal):

    accountName = resultsTranScrubList[resultsTranScrubIndexOfRow][tranAccountColIndex]

    for indexOfAccountMap in range(0, accountDataPointsToMap):
        # pp(chartOfAccountsDict[accountName].values())

        if accountName == gainLossAccount:
            mappedAccountData = "=vlookup(indirect(\"r[0]c[-" + str(indexOfAccountMap + 9) + "]\",false),indirect(\"Chart of Accounts!r1c1:r" + str(len(chartOfAccountsDict)) + "c" + str(accountDataPointsToMap + 1) + "\",false)," + str(indexOfAccountMap + 2) + ",)"                   #"=vlookup(indirect(\"r[0]c[-9]\",false),'Chart of Accounts'!$A$1:$C$26," + "2" + ",)"
        else:
            mappedAccountData = list(chartOfAccountsDict[accountName].values())[indexOfAccountMap]
        resultsTranScrubList[resultsTranScrubIndexOfRow].append(mappedAccountData)

    if resultsTranScrubIndexOfRow == 0:
        resultsTranScrubList[resultsTranScrubIndexOfRow].append("Year")
    else:
        resultsTranScrubList[resultsTranScrubIndexOfRow].append(myPyFunc.convertSerialDateToYear(resultsTranScrubList[resultsTranScrubIndexOfRow][tranDateColIndex]))



splitTime = myGoogleSheetsFunc.populateSheet(2, 1000, "Transactions - Scrubbed", googleSheetsAPIObj, resultsSpreadsheetID, resultsTranScrubList, False, writeToSheet=True, splitTimeArg=splitTime)


resultsTranScrubRowTotal = len(resultsTranScrubList)
resultsTranScrubColTotal = len(resultsTranScrubList[0])
# pp(resultsTranScrubRowTotal)
# pp(resultsTranScrubColTotal)



scrubTranToDownload = ["Transactions - Scrubbed"]
scrubTranDownloadedWithGrid = myGoogleSheetsFunc.getDataWithGrid(resultsSpreadsheetID, googleSheetsAPIObj, scrubTranToDownload)
resultsTranScrubList = myGoogleSheetsFunc.extractValues(myGoogleSheetsFunc.countRows(scrubTranDownloadedWithGrid, scrubTranToDownload.index("Transactions - Scrubbed")), myGoogleSheetsFunc.countColumns(scrubTranDownloadedWithGrid, scrubTranToDownload.index("Transactions - Scrubbed")), scrubTranDownloadedWithGrid, scrubTranToDownload.index("Transactions - Scrubbed"))





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



tblScrubbedColumns = myPyFunc.createColumnsDict([
    {"\"Date\"": "date"},
    {"\"Account\"": "varchar(255)"},
    {"\"Amount+-\"": "float"},
    {"\"Transaction Type\"": "varchar(255)"},
    {"\"Stock Name\"": "varchar(255)"},
    {"\"Broker\"": "varchar(255)"},
    {"\"Lot\"": "varchar(255)"},
    {"\"Shares\"": "float"},
    {"\"Ticker\"": "varchar(255)"},
    {"\"Capital Invested\"": "varchar(255)"},
    {"\"Account Type\"": "varchar(255)"},
    {"\"Account Category\"": "varchar(255)"},
    {"\"Year\"": "int"}
])



myPyFunc.createTable("tblScrubbed", tblScrubbedColumns, sqlCursor)
myPyFunc.populateTable(resultsTranScrubRowTotal, resultsTranScrubColTotal, "tblScrubbed", resultsTranScrubList, sqlCursor, [0])



# tickerColumnsObj = OrderedDict()
# tickerColumnsObj["rowNumber"] = "int"
# tickerColumnsObj["Ticker"] = "varchar(255)"
# tickerColumnsObj["stockName"] = "varchar(255)"
#
# myPyFunc.createTable("tblTickerMap", tickerColumnsObj, sqlCursor)
# myPyFunc.populateTable(len(tickerMapUniqueExtractedValues), len(tickerMapUniqueExtractedValues[0]), "tblTickerMap", tickerMapUniqueExtractedValues, sqlCursor, [])




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


# fieldAliasStr = myPyFunc.fieldsDictToStr(firstFieldsDict, True, True)
# fieldStr = myPyFunc.fieldsDictToStr(firstFieldsDict, True, False)
# aliasStr = myPyFunc.fieldsDictToStr(firstFieldsDict, False, True)


fieldStr = "\"Stock Name\", \"Broker\", \"Lot\""

sqlCommand = f"select {fieldStr}, ltrim(strftime('%m', \"Date\"), '0') || '/' || ltrim(strftime('%d', \"Date\"), '0') || '/' || substr(strftime('%Y', \"Date\"), 3, 2) as 'Purchase Date', -sum(\"Amount\") as 'Capital Invested' from tblScrubbed where \"Account\" = 'Cash' and \"Transaction Type\" like '%Purchase%' and \"Transaction Type\" not like '%Group Shares%' group by {fieldStr}, \"Date\";"
myPyFunc.createTableAs("tblPurchase", sqlCursor, sqlCommand)

sqlCommand = f"select {fieldStr}, sum(/"Shares/") from tblScrubbed where /"Account/" = 'Investment Asset' and /"Transaction Type/" like %Purchase%' and \"Transaction Type\" not like '%Group Shares%' group by {fieldStr};"
pp(sqlCommand)
# myPyFunc.createTableAs("tblShares", sqlCursor, sqlCommand)
# myPyFunc.createTableAs("tblSale", sqlCursor, f"select {fieldAliasStr}, case when tranType != 'Sale - Hypothetical' then ltrim(strftime('%m', tranDate), '0') || '/' || ltrim(strftime('%d', tranDate), '0') || '/' || substr(strftime('%Y', tranDate), 3, 2) end as 'Sale Date', sum(amount) as 'Last Value', '' as 'To Sell', '=indirect(\"I\"&row())-indirect(\"F\"&row())' as 'Gain (Loss)', '=iferror(indirect(\"J\"&row())/indirect(\"F\"&row()),\"\")' as '% Gain (Loss)' from {tblMainName} where account = 'Cash' and tranType like '%Sale%' and tranType not like '%Group Shares%' group by {fieldStr}, tranDate;")
#
# # strftime('%m/%d', tranDate) + '/' +
# #get list of values to put as the pivot columns
#
#
# pivotColDict = myPyFunc.createPivotColDict("yearOfDate", 10, "amount", 1, resultsTranScrubList)
# pivotColStr = pivotColDict["pivotColStr"]
# # pp(pivotColStr)
#
# myPyFunc.createTableAs("tblDividends", sqlCursor, f"select {fieldAliasStr}, {pivotColStr} from {tblMainName} where account = 'Cash' and tranType like '%Dividend%' group by {fieldStr};")
# myPyFunc.createTableAs("tblResults", sqlCursor, f"select {aliasStr} from tblPurchase union select {aliasStr} from tblSale union select {aliasStr} from tblDividends;")
#
#
# colListStr = myPyFunc.getAllColumns(colDict, sqlCursor)
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
# myPyFunc.createTableAs("tblResultsJoined", sqlCursor, sqlCommand)
#
# sqlList = ["update tblResultsJoined set 'Last Value' = '=googlefinance(indirect(\"D\"&row()))*indirect(\"G\"&row())' where tblResultsJoined.'Sale Date' is null;"]
# myPyFunc.executeSQLStatements(sqlList, sqlCursor)
#
#


splitTime = myGoogleSheetsFunc.populateSheet(2, 1000, "SQL Query Result - Table", googleSheetsAPIObj, resultsSpreadsheetID, myPyFunc.getQueryResult("select * from tblResultsJoined order by Broker, Stock, Lot", sqlCursor, True), True, writeToSheet=True, splitTimeArg=splitTime)

splitTime = myGoogleSheetsFunc.populateSheet(2, 1000, "SQL Query Result - Balance Sheet", googleSheetsAPIObj, resultsSpreadsheetID, myPyFunc.getQueryResult("select * from tblResultsJoined order by Broker, Stock, Lot", sqlCursor, True), True, writeToSheet=True, splitTimeArg=splitTime)



myPyFunc.closeDatabase(sqlObj["sqlConnection"])
splitTime = myPyFunc.printElapsedTime(splitTime, "Finished with database")