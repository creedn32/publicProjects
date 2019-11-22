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


tblName = "tblTScrub"

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


sqlObj = myPythonFunctions.createDatabase("stockResults.db", str(pathlib.Path.cwd().parents[3]/"privateData"/"stockResults"), tblName, columnsObj)
myPythonFunctions.populateTable(tranScrubRowTotal, tranScrubColTotal, tblName, tranScrubDataList, sqlObj["sqlCursor"], [0])


fieldsStr = myPythonFunctions.listToStr(["broker", "stockName", "lot"])


sqlList = ["drop table if exists tblPurchase;", f"create table tblPurchase as select {fieldsStr}, tranDate, sum(amount) as purchaseAmount from {tblName} where account = 'Cash' and tranType like '%Purchase%' and tranType not like '%Group Shares%' group by {fieldsStr}, tranDate;"]
myPythonFunctions.executeSQLStatements(sqlList, sqlObj["sqlCursor"])

sqlList = ["drop table if exists tblSale;", f"create table tblSale as select {fieldsStr}, tranDate, sum(amount) from {tblName} where account = 'Cash' and tranType like '%Sale%' and tranType not like '%Group Shares%' group by {fieldsStr}, tranDate;"]
myPythonFunctions.executeSQLStatements(sqlList, sqlObj["sqlCursor"])


colData = []
colIndex = 10
rowStartIndex = 1
pivotColList = []

for row in tranScrubDataList[rowStartIndex:]:
    colData.append(row[colIndex])

colData = list(set((colData)))
colData.sort()

for colItem in colData:
    pivotColList.append("sum(case when dateYear = '" + str(colItem) + "' then amount end)")

pivotColumns = myPythonFunctions.listToStr(pivotColList)

sqlList = ["drop table if exists tblDividends;", f"create table tblDividends as select {fieldsStr}, {pivotColumns} from {tblName} where account = 'Cash' and tranType like '%Dividend' group by {fieldsStr};"]
myPythonFunctions.executeSQLStatements(sqlList, sqlObj["sqlCursor"])

sqlList = ["drop table if exists tblResults;", f"create table tblResults as select {fieldsStr} from tblPurchase union select {fieldsStr} from tblSale union select {fieldsStr} from tblDividends;"]
myPythonFunctions.executeSQLStatements(sqlList, sqlObj["sqlCursor"])


sqlCommand = ["drop table if exists tblResultsJoined;", f"create table tblResultsJoined as select tblResults.broker, tblResults.stockName, tblResults.lot, tblPurchase.purchaseAmount from tblResults " \
                                                        "left outer join tblPurchase on tblResults.broker = tblPurchase.broker and tblResults.stockName = tblPurchase.stockName and tblResults.lot = tblPurchase.lot;"]

myPythonFunctions.executeSQLStatements(sqlCommand, sqlObj["sqlCursor"])




googleSheetsFunctions.populateSheet(1, 1, "SQL Query Result", googleSheetsObj, spreadsheetID, myPythonFunctions.getQueryResult("select * from tblResultsJoined", sqlObj["sqlCursor"]), True)
myPythonFunctions.closeDatabase(sqlObj["sqlConnection"])


# if os.path.exists(dbPath):
#   os.remove(dbPath)
# else:

#   print("The file does not exist")



