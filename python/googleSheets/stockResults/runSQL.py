import sys, pathlib
sys.path.append(str(pathlib.Path.cwd().parents[0]/"myGoogleSheetsPythonLibrary"))
sys.path.append(str(pathlib.Path.cwd().parents[1]))
from myPythonLibrary import myPythonFunctions
startTime = myPythonFunctions.startCode()

from pprint import pprint as pp
from collections import OrderedDict
import googleSheetsFunctions, googleSheetsAuthenticate

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



colDict = {0:
               {"table": "tblResults",
                "excludedFields": []},
            2: {"table": "tblPurchase",
                "excludedFields": ["Stock", "Broker", "Lot"]},
            1: {"table": "tblShares",
                "excludedFields": ["Stock", "Broker", "Lot"]},
            3: {"table": "tblSale",
                "excludedFields": ["Stock", "Broker", "Lot"]},
            4: {"table": "tblDividends",
                "excludedFields": ["Stock", "Broker", "Lot"]}}




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


sqlObj = myPythonFunctions.createDatabase("stockResults.db", str(pathlib.Path.cwd().parents[3]/"privateData"/"stockResults"), tblMainName, columnsObj)
myPythonFunctions.populateTable(tranScrubRowTotal, tranScrubColTotal, tblMainName, tranScrubDataList, sqlObj["sqlCursor"], [0])


fieldAliasStr = myPythonFunctions.fieldsDictToStr(firstFieldsDict, True, True)
fieldStr = myPythonFunctions.fieldsDictToStr(firstFieldsDict, True, False)
aliasStr = myPythonFunctions.fieldsDictToStr(firstFieldsDict, False, True)

myPythonFunctions.createTableAs("tblPurchase", sqlObj["sqlCursor"], f"select {fieldAliasStr}, tranDate as 'Purchase Date', -sum(amount) as 'Capital Invested' from {tblMainName} where account = 'Cash' and tranType like '%Purchase%' and tranType not like '%Group Shares%' group by {fieldStr}, tranDate;")
myPythonFunctions.createTableAs("tblShares", sqlObj["sqlCursor"], f"select {fieldAliasStr}, sum(shares) as Shares from {tblMainName} where account = 'Investment Asset' and tranType like '%Purchase%' and tranType not like '%Group Shares%' group by {fieldStr};")
myPythonFunctions.createTableAs("tblSale", sqlObj["sqlCursor"], f"select {fieldAliasStr}, case when tranType != 'Sale - Hypothetical' then tranDate end as 'Sale Date', sum(amount) as 'Last Value', '' as 'Gain (Loss)', '' as '% Gain (Loss)' from {tblMainName} where account = 'Cash' and tranType like '%Sale%' and tranType not like '%Group Shares%' group by {fieldStr}, tranDate;")


#get list of values to put as the pivot columns


pivotColStr = myPythonFunctions.createPivotColStr("dateYear", 10, "amount", 1, tranScrubDataList)
myPythonFunctions.createTableAs("tblDividends", sqlObj["sqlCursor"], f"select {fieldAliasStr}, {pivotColStr} from {tblMainName} where account = 'Cash' and tranType like '%Dividend%' group by {fieldStr};")
myPythonFunctions.createTableAs("tblResults", sqlObj["sqlCursor"], f"select {aliasStr} from tblPurchase union select {aliasStr} from tblSale union select {aliasStr} from tblDividends;")


colListStr = myPythonFunctions.getAllColumns(colDict, sqlObj["sqlCursor"])

sqlCommand = f"select " + colListStr + " from tblResults " \
            "left outer join tblPurchase on tblResults.Broker = tblPurchase.Broker and tblResults.Stock = tblPurchase.Stock and tblResults.Lot = tblPurchase.Lot " \
            "left outer join tblShares on tblResults.Broker = tblShares.Broker and tblResults.Stock = tblShares.Stock and tblResults.Lot = tblShares.Lot " \
            "left outer join tblSale on tblResults.Broker = tblSale.Broker and tblResults.Stock = tblSale.Stock and tblResults.Lot = tblSale.Lot " \
            "left outer join tblDividends on tblResults.Broker = tblDividends.Broker and tblResults.Stock = tblDividends.Stock and tblResults.Lot = tblDividends.Lot"

myPythonFunctions.createTableAs("tblResultsJoined", sqlObj["sqlCursor"], sqlCommand)


googleSheetsFunctions.populateSheet(2, 1, "SQL Query Result", googleSheetsObj, spreadsheetID, myPythonFunctions.getQueryResult("select * from tblResultsJoined", "tblResultsJoined", sqlObj["sqlCursor"], True), True)
myPythonFunctions.closeDatabase(sqlObj["sqlConnection"])



# if os.path.exists(dbPath):
#   os.remove(dbPath)
# else:
#   print("The file does not exist")



