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


sqlObj = myPythonFunctions.createDatabase("stockResults.db", str(pathlib.Path.cwd().parents[3]/"privateData"/"stockResults"), tblName, columnsObj)
myPythonFunctions.populateTable(tranScrubRowTotal, tranScrubColTotal, tblName, tranScrubDataList, sqlObj["sqlCursor"], [0])

sqlList = ["drop table if exists tblPurchase;", "create table tblPurchase as select broker, stockName, lot, tranDate, sum(amount) from tblTScrub where account = 'Cash' and tranType like '%Purchase%' and tranType not like '%Group Shares%' group by broker, stockName, lot, tranDate;"]
myPythonFunctions.executeSQLStatements(sqlList, sqlObj["sqlCursor"])

sqlList = ["drop table if exists tblSale;", "create table tblSale as select broker, stockName, lot, tranDate, sum(amount) from tblTScrub where account = 'Cash' and tranType like '%Sale%' and tranType not like '%Group Shares%' group by broker, stockName, lot, tranDate;"]
myPythonFunctions.executeSQLStatements(sqlList, sqlObj["sqlCursor"])

sqlList = ["drop table if exists tblDividends;", "create table tblDividends as select broker, stockName, lot, sum(amount) from tblTScrub where account = 'Cash' and tranType like '%Dividend' group by broker, stockName, lot;"]
myPythonFunctions.executeSQLStatements(sqlList, sqlObj["sqlCursor"])


googleSheetsFunctions.populateSheet(1, 100, "SQL Query Result", googleSheetsObj, spreadsheetID, myPythonFunctions.getQueryResult("select * from tblDividends", sqlObj["sqlCursor"]), True)
myPythonFunctions.closeDatabase(sqlObj["sqlConnection"])


# if os.path.exists(dbPath):
#   os.remove(dbPath)
# else:

#   print("The file does not exist")



