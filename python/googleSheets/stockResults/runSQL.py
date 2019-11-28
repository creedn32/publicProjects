import sys, pathlib
sys.path.append(str(pathlib.Path.cwd().parents[0]/"myGoogleSheetsPythonLibrary"))
sys.path.append(str(pathlib.Path.cwd().parents[1]))
from myPythonLibrary import myPythonFunctions
startTime = myPythonFunctions.startCode()

from pprint import pprint as pp
from collections import OrderedDict
import googleSheetsFunctions, googleSheetsAuthenticate, sqlite3

spreadsheetID = "1pjhFRIoB9mnbiMOj_hsFwsGth91l1oX_4kmeYrsT5mc" #full spreadsheet
sheetsToDownload = "Transactions - Scrubbed"
downloadedSheetIndex = 0
googleSheetsObj = googleSheetsAuthenticate.authFunc()
googleSheetsDataWithGrid = googleSheetsFunctions.getDataWithGrid(spreadsheetID, googleSheetsObj, sheetsToDownload)
tranScrubRowTotal = googleSheetsFunctions.countRows(googleSheetsDataWithGrid, downloadedSheetIndex)
tranScrubColTotal = googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, downloadedSheetIndex)
tranScrubDataList = googleSheetsFunctions.extractValues(tranScrubRowTotal, tranScrubColTotal, googleSheetsDataWithGrid, downloadedSheetIndex)

finishSetupTime = myPythonFunctions.time.time()
print("Comment: Importing modules and setting up variables...Done. " + str(round(finishSetupTime - startTime, 3)) + " seconds")


tblMainName = "tblTScrub"

columnsObj = OrderedDict()
columnsObj["tranDate"] = "date"
columnsObj["account"] = "varchar(255)"
columnsObj["accountType"] = "varchar(255)"
columnsObj["accountCategory"] = "varchar(255)"
columnsObj["amount"] = "float"
columnsObj["tranType"] = "varchar(255)"
columnsObj["tranType"] = "varchar(255)"
columnsObj["stockName"] = "varchar(255)"
columnsObj["broker"] = "varchar(255)"
columnsObj["lot"] = "varchar(255)"
columnsObj["shares"] = "float"
columnsObj["dateYear"] = "int"


sqlObj = myPythonFunctions.createDatabase("stockResults.db", str(pathlib.Path.cwd().parents[3]/"privateData"/"stockResults"), tblMainName, columnsObj)
myPythonFunctions.populateTable(tranScrubRowTotal, tranScrubColTotal, tblMainName, tranScrubDataList, sqlObj["sqlCursor"], [0])


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


fieldAliasStr = myPythonFunctions.fieldsDictToStr(firstFieldsDict, True, True)
fieldStr = myPythonFunctions.fieldsDictToStr(firstFieldsDict, True, False)
aliasStr = myPythonFunctions.fieldsDictToStr(firstFieldsDict, False, True)

sqlList = ["drop table if exists tblPurchase;", f"create table tblPurchase as select {fieldAliasStr}, tranDate as purchaseDate, -sum(amount) as purchaseAmount from {tblMainName} where account = 'Cash' and tranType like '%Purchase%' and tranType not like '%Group Shares%' group by {fieldStr}, tranDate;"]
myPythonFunctions.executeSQLStatements(sqlList, sqlObj["sqlCursor"])

sqlList = ["drop table if exists tblShares;", f"create table tblShares as select {fieldAliasStr}, sum(shares) as Shares from {tblMainName} where account = 'Investment Asset' and tranType like '%Purchase%' and tranType not like '%Group Shares%' group by {fieldStr};"]
myPythonFunctions.executeSQLStatements(sqlList, sqlObj["sqlCursor"])

sqlList = ["drop table if exists tblSale;", f"create table tblSale as select {fieldAliasStr}, case when tranType != 'Sale - Hypothetical' then tranDate end as saleDate, '' as blankCol, sum(amount) as saleAmount from {tblMainName} where account = 'Cash' and tranType like '%Sale%' and tranType not like '%Group Shares%' group by {fieldStr}, tranDate;"]
myPythonFunctions.executeSQLStatements(sqlList, sqlObj["sqlCursor"])


#get list of values to put as the pivot columns

colData = []
colIndex = 10
rowStartIndex = 1

for row in tranScrubDataList[rowStartIndex:]:
    colData.append(row[colIndex])

colData = list(set((colData)))
colData.sort()


#create formula for each column

pivotColStr = ""

for colItem in colData:
    pivotColStr = pivotColStr + "sum(case when dateYear = '" + str(colItem) + "' then amount end) as div" + str(colItem)

    if colItem != colData[len(colData) - 1]:
        pivotColStr = pivotColStr + ", "

sqlList = ["drop table if exists tblDividends;", f"create table tblDividends as select {fieldAliasStr}, {pivotColStr} from {tblMainName} where account = 'Cash' and tranType like '%Dividend%' group by {fieldStr};"]
myPythonFunctions.executeSQLStatements(sqlList, sqlObj["sqlCursor"])

sqlList = ["drop table if exists tblResults;", f"create table tblResults as select {aliasStr} from tblPurchase union select {aliasStr} from tblSale union select {aliasStr} from tblDividends;"]
myPythonFunctions.executeSQLStatements(sqlList, sqlObj["sqlCursor"])


colDict = {0:
               {"table": "tblResults",
                "excludedFields": []},
            1: {"table": "tblPurchase",
                "excludedFields": ["Stock", "Broker", "Lot"]},
            2: {"table": "tblShares",
                "excludedFields": ["Stock", "Broker", "Lot"]},
            3: {"table": "tblSale",
                "excludedFields": ["Stock", "Broker", "Lot"]},
            4: {"table": "tblDividends",
                "excludedFields": ["Stock", "Broker", "Lot"]}}


colList = []

for i in range(0, len(colDict)):

    tableColNamesList = myPythonFunctions.getSQLColNamesList(sqlObj["sqlCursor"], colDict[i]["table"])

    tableColNamesExcl = []

    for col in tableColNamesList:

        for excludedField in colDict[i]["excludedFields"]:
            pass

        excludedField = "Stock"

        if "." + excludedField not in col:
            tableColNamesExcl.append(col)


    # compList = [item for item in tableColNamesList if item in ["tblResults.Stock"]]

    colList.extend(tableColNamesExcl)


colListStr = myPythonFunctions.listToStr(colList)

pp(colListStr)


sqlCommand = ["drop table if exists tblResultsJoined;", f"create table tblResultsJoined as select " + colListStr + " from tblResults " \
                                                        "left outer join tblPurchase on tblResults.Broker = tblPurchase.Broker and tblResults.Stock = tblPurchase.Stock and tblResults.Lot = tblPurchase.Lot " \
                                                        "left outer join tblShares on tblResults.Broker = tblShares.Broker and tblResults.Stock = tblShares.Stock and tblResults.Lot = tblShares.Lot " \
                                                        "left outer join tblSale on tblResults.Broker = tblSale.Broker and tblResults.Stock = tblSale.Stock and tblResults.Lot = tblSale.Lot " \
                                                        "left outer join tblDividends on tblResults.Broker = tblDividends.Broker and tblResults.Stock = tblDividends.Stock and tblResults.Lot = tblDividends.Lot"]

myPythonFunctions.executeSQLStatements(sqlCommand, sqlObj["sqlCursor"])


googleSheetsFunctions.populateSheet(2, 100, "SQL Query Result", googleSheetsObj, spreadsheetID, myPythonFunctions.getQueryResult("select * from tblResultsJoined", "tblResultsJoined", sqlObj["sqlCursor"]), True)
myPythonFunctions.closeDatabase(sqlObj["sqlConnection"])



# if os.path.exists(dbPath):
#   os.remove(dbPath)
# else:

#   print("The file does not exist")



