import sys, pathlib
sys.path.append(str(pathlib.Path.cwd().parents[0]))
sys.path.append(str(pathlib.Path.cwd().parents[1]))
from myPythonLibrary import myPythonFunctions
startTime = myPythonFunctions.startCode()

# multiplyFactor = 1
# accountColumn = 1
# listOfSheetData = []
# destRange = "Scrubbed Transactions"
rangesToDownload = ["Robinhood - Raw Data"]
# saveJSONFile = False
spreadsheetID = "1oisLtuJJOZnU-nMvILNWO43_8w2rCT3V6vq3vMnAnCI"


import importlib, re
googleSheetsFunctions = importlib.import_module("myGoogleSheetsPythonLibrary.googleSheetsFunctions")
googleSheetsAuthenticate = importlib.import_module("myGoogleSheetsPythonLibrary.googleSheetsAuthenticate")
from pprint import pprint as pp


googleSheetsObj = googleSheetsAuthenticate.authFunc()
googleSheetsDataWithGrid = googleSheetsFunctions.getDataWithGrid(spreadsheetID, googleSheetsObj, rangesToDownload)


finishSetupTime = myPythonFunctions.time.time()
print("Comment: Importing modules and setting up variables...Done. " + str(round(finishSetupTime - startTime, 3)) + " seconds")

# if saveJSONFile: myPythonFunctions.saveFile(googleSheetsDataWithGrid, pathlib.Path(pathlib.Path.cwd().parents[3]/"privateData"/"stockResults"/"googleSheetsDataWithGrid.json"), finishSetupTime)


numberOfRows = googleSheetsFunctions.countRows(googleSheetsDataWithGrid, 0)
numberOfColumns = googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, 0)



#get raw data from Google Sheets

listObj = []

for indexOfRow in range(0, numberOfRows):
    currentRowData = []

    for indexOfColumn in range(0, numberOfColumns):
        dict = googleSheetsFunctions.getCellValueEffective(googleSheetsDataWithGrid, 0, indexOfRow, indexOfColumn)
        dictKey = list(dict.keys())[0]
        currentRowData.append({"value": dict[dictKey], "type": dictKey, })

    listObj.append(currentRowData)






#put data into table

subCount = 1
indivTransactionList = []
transactionsList = []
destRange = "Robinhood - Data"
# fieldsObj = {1: "Description", 2: "Date", 3: "Amount", 4: "Details"}


for indexOfRow in range(0, numberOfRows):
    val = listObj[indexOfRow][0]["value"]
    matchObj = re.search("[0-9]+ share", str(val))


    if subCount > 3 and not matchObj:
        subCount = 1

        if len(indivTransactionList) == 3:
            indivTransactionList.append("")
            indivTransactionList.append("")

        transactionsList.append(indivTransactionList)
        indivTransactionList = []

    indivTransactionList.append(val)

    if subCount > 3 and matchObj:
        indivTransactionList.append(int(matchObj.group(0).split(" share")[0]))


    subCount = subCount + 1


transactionsList.append(indivTransactionList)


transactionsList.sort(key=lambda x: int(x[1]))

newTransactionsList = []

for transaction in transactionsList:
    if transaction[1] > 43404:
        newTransactionsList.append(transaction)


transactionsList = newTransactionsList
transactionsList.insert(0, ["Description", "Date", "Amount", "Details", "Shares"])

valuesToWrite = {"values": transactionsList}
googleSheetsObj.values().update(spreadsheetId=spreadsheetID, range=destRange, valueInputOption="USER_ENTERED", body=valuesToWrite).execute()




#iterate over table

listOfSheetData = [["Date", "Account", "Amount+-", "Transaction Type", "Stock Name", "Broker", "Lot", "Shares"]]
destRange = "Robinhood - Transactions"
mapLeftObj = {"Dividend from ": {"transactionType": "Receive Dividend", "debitAccount": "Cash", "creditAccount": "Dividend Revenue", "stockName": "Stock Name"},
       "Withdrawal to ": {"transactionType": "Cash To Owners", "debitAccount": "Capital Contributions", "creditAccount": "Cash", "stockName": "All Stocks"},
       "Deposit from ": {"transactionType": "Cash From Owners", "debitAccount": "Cash", "creditAccount": "Capital Contributions", "stockName": "All Stocks"},
       "Interest Payment": {"transactionType": "Receive Interest", "debitAccount": "Cash", "creditAccount": "Interest Revenue", "stockName": "All Stocks"},
       "AKS from Robinhood": {"transactionType": "Receive Stock Gift", "debitAccount": "Investment Asset", "creditAccount": "Gain On Gift", "stockName": "AKS"}}

mapRightObj = {" Market Buy": {"transactionType": "Purchase Stock", "debitAccount": "Investment Asset", "creditAccount": "Cash", "stockName": "Stock Name"}}


for transaction in transactionsList[1:]:

    locatedObj = {}

    for mapping in mapLeftObj:
        if transaction[0][:len(mapping)] == mapping:
            locatedObj = mapLeftObj[mapping]

    if not locatedObj:
        for mapping in mapRightObj:
            if transaction[0][-len(mapping):] == mapping:
                locatedObj = mapRightObj[mapping]

    # pp(transaction)

    listOfSheetData.append([transaction[1], locatedObj["debitAccount"], transaction[2], locatedObj["transactionType"], locatedObj["stockName"], "Robinhood", "Lot", transaction[4]])
    listOfSheetData.append([transaction[1], locatedObj["creditAccount"], -transaction[2], locatedObj["transactionType"], locatedObj["stockName"], "Robinhood", "Lot", ""])


valuesToWrite = {"values": listOfSheetData}
googleSheetsObj.values().update(spreadsheetId=spreadsheetID, range=destRange, valueInputOption="USER_ENTERED", body=valuesToWrite).execute()
