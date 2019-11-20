import sys, pathlib
from pprint import pprint as pp

sys.path.append(str(pathlib.Path.cwd().parents[0]/"myGoogleSheetsPythonLibrary"))
sys.path.append(str(pathlib.Path.cwd().parents[1]))
from myPythonLibrary import myPythonFunctions
startTime = myPythonFunctions.startCode()


spreadsheetID = "1pjhFRIoB9mnbiMOj_hsFwsGth91l1oX_4kmeYrsT5mc" #full spreadsheet
sheetsToDownload = "Transactions - Scrubbed"
downloadedSheetIndex = 0


import googleSheetsFunctions, googleSheetsAuthenticate
import sqlite3

googleSheetsObj = googleSheetsAuthenticate.authFunc()
googleSheetsDataWithGrid = googleSheetsFunctions.getDataWithGrid(spreadsheetID, googleSheetsObj, sheetsToDownload)

tranScrubDataList = googleSheetsFunctions.extractValues(googleSheetsFunctions.countRows(googleSheetsDataWithGrid, downloadedSheetIndex), googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, downloadedSheetIndex), googleSheetsDataWithGrid, downloadedSheetIndex)

finishSetupTime = myPythonFunctions.time.time()
print("Comment: Importing modules and setting up variables...Done. " + str(round(finishSetupTime - startTime, 3)) + " seconds")

pp(tranScrubDataList[0:5])




databaseName = "stockResults.db"
dbPath = pathlib.Path(pathlib.Path.cwd().parents[3]/"privateData"/"stockResults"/databaseName)

sqlConnection = sqlite3.connect(dbPath)
sqlCrsr = sqlConnection.cursor()
tblName = "tblTransactionsScrubbed"
sqlList = []

sqlList.append("drop table if exists " + tblName + ";")
sqlList.append(
    "create table " + tblName + " (tranDate date, account varchar(255), accountType varchar(255), accountCategory varchar(255), amount float, tranType varchar(255), stockName varchar(255), broker varchar(255), lot varchar(255), shares float);")

sqlCommand = "insert into " + tblName + " values "

rangeOfRowsUpperLimit = numberOfRows

for indexOfRow in range(1, rangeOfRowsUpperLimit):

    sqlCommand = sqlCommand + "(" \
 \
            rangeOfColumnsUpperLimit = len(listOfSheetData[0])

    for indexOfColumn in range(0, rangeOfColumnsUpperLimit):

        sqlCommand = sqlCommand + "\""

        if indexOfColumn == 0:
            sqlCommand = sqlCommand + myPythonFunctions.convertSerialDateToMySQLDate(
                listOfSheetData[indexOfRow][indexOfColumn])
        else:
            sqlCommand = sqlCommand + str(listOfSheetData[indexOfRow][indexOfColumn])

        sqlCommand = sqlCommand + "\""

        if indexOfColumn != rangeOfColumnsUpperLimit - 1:
            sqlCommand = sqlCommand + ", "

    sqlCommand = sqlCommand + ")"

    if indexOfRow != rangeOfRowsUpperLimit - 1:
        sqlCommand = sqlCommand + ", "

sqlCommand = sqlCommand + ";"

# pp(sqlCommand)

sqlList.append(sqlCommand)
myPythonFunctions.executeSQLStatements(sqlList, sqlCrsr)

sqlCrsr.execute("select distinct broker, stockName, lot from " + tblName + ";")

ans = sqlCrsr.fetchall()
pp(ans)

sqlConnection.commit()
sqlConnection.close()

# pp(listOfSheetData[0:3])


# if os.path.exists(dbPath):
#   os.remove(dbPath)
# else:
#   print("The file does not exist")



