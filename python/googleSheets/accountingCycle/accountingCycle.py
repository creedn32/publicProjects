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
uniqueAccountList = myPyFunc.getQueryResult("select distinct `Account` from tblJournal", sqlCursor, False)
splitTime = myGoogleSheetsFunc.populateSheet(2, 1, "tblJournalAccounts", googleSheetsAPIObj, spreadsheetID, uniqueAccountList, True, writeToSheet=False, splitTimeArg=splitTime, columnRow=False)


ledgerData = {}

for account in uniqueAccountList:
    accountName = account[0]
    ledgerData[accountName] = [[accountName, ""]]
    sqlCommand = "select * from tblJournal where `Account` = '" + accountName + "'"
    accountTransactionList = myPyFunc.getQueryResult(sqlCommand, sqlCursor, False)
    for transaction in accountTransactionList:
        ledgerData[accountName].append(transaction[-2:])



ledgerList = ledgerData["Cash"]


cellFormattingRequest = [{
                    "repeatCell": {
                        "range": {
                            "sheetId": myGoogleSheetsFunc.getSheetID("Ledger", googleSheetsAPIObj, spreadsheetID),
                            "startRowIndex": 0,
                            "endRowIndex": 1
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "textFormat": {
                                    "bold": True
                                }
                            }
                        },
                        "fields": "userEnteredFormat(textFormat)"
                    }
                }]

splitTime = myGoogleSheetsFunc.populateSheet(2, 1, "Ledger", googleSheetsAPIObj, spreadsheetID, ledgerList, True, writeToSheet=True, splitTimeArg=splitTime, columnRow=False, cellFormattingRequest=cellFormattingRequest)





