import sys, pathlib
sys.path.append(str(pathlib.Path.cwd().parents[1]))
from myPyLib import myPyFunc, myGoogleSheetsFunc


startTime = myPyFunc.printElapsedTime(False, "Starting script")
from pprint import pprint as pp

spreadsheetID = "1jbV5jjW-iWlCoBgwB0mmywbfTRcMK7XaOF-u79mLVv8"
sqlObj = myPyFunc.createDatabase("accountingCycle.db", str(pathlib.Path.cwd().parents[3]/"privateData"/"accountingCycle"))
sqlCursor = sqlObj["sqlCursor"]
googleSheetsAPIObj = myGoogleSheetsFunc.authFunc()

splitTime = myPyFunc.printElapsedTime(startTime, "Finished importing modules and intializing variables")

toDownload = ["Journal"]
journalDownloadedWithGrid = myGoogleSheetsFunc.getDataWithGrid(spreadsheetID, googleSheetsAPIObj, toDownload)
journalList = myGoogleSheetsFunc.extractValues(journalDownloadedWithGrid, toDownload, "Journal")


colTblJournal = myPyFunc.createColumnsDict([
    {"`Date`": "date"},
    {"`Account`": "varchar(255)"},
    {"Debit": "varchar(255)"},
    {"Credit": "varchar(255)"}
])


myPyFunc.createAndPopulateTable("tblJournal", colTblJournal, sqlCursor, journalList, [0])


pp(journalList)
