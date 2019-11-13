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
from datetime import date


googleSheetsObj = googleSheetsAuthenticate.authFunc()
googleSheetsDataWithGrid = googleSheetsFunctions.getDataWithGrid(spreadsheetID, googleSheetsObj, rangesToDownload)


finishSetupTime = myPythonFunctions.time.time()
print("Comment: Importing modules and setting up variables...Done. " + str(round(finishSetupTime - startTime, 3)) + " seconds")

# if saveJSONFile: myPythonFunctions.saveFile(googleSheetsDataWithGrid, pathlib.Path(pathlib.Path.cwd().parents[3]/"privateData"/"stockResults"/"googleSheetsDataWithGrid.json"), finishSetupTime)


numberOfRows = googleSheetsFunctions.countRows(googleSheetsDataWithGrid, 0)
numberOfColumns = googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, 0)



#get raw data from Google Sheets and put into listObj

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

    nextValueHasNoShares = True
    currentValue = listObj[indexOfRow][0]["value"]

    if indexOfRow + 2 <= numberOfRows:
        if len(str(listObj[indexOfRow + 1][0]["value"]).split(" share")) > 1:
            nextValueHasNoShares = False

    indivTransactionList.append(currentValue)

    # pp("indexofRow: " + str(indexOfRow))
    # pp("subcount:" + str(subCount))
    # pp(nextValueHasNoShares)

    if subCount == 3 and nextValueHasNoShares or subCount == 4:
        subCount = 0

        if len(indivTransactionList) == 3:
            indivTransactionList.extend(["", ""])
        elif len(indivTransactionList) == 4:
            indivTransactionList.append(int(str(currentValue).split(" share")[0]))

        transactionsList.append(indivTransactionList)
        indivTransactionList = []

    subCount = subCount + 1


transactionsList.sort(key=lambda x: int(x[1]))
filterList = False




newTransactionsList = []

for transaction in transactionsList:

    # transaction[2] = abs(transaction[2])
    pp(transaction[2])

    if transaction[2] != "Failed":

        transaction[2] = abs(transaction[2])

        if filterList:
            if transaction[1] > 43404:
                newTransactionsList.append(transaction)
        else:
            newTransactionsList.append(transaction)



transactionsList = newTransactionsList

transactionsList.insert(0, ["Description", "Date", "Amount", "Details", "Shares"])

valuesToWrite = {"values": transactionsList}
googleSheetsObj.values().update(spreadsheetId=spreadsheetID, range=destRange, valueInputOption="USER_ENTERED", body=valuesToWrite).execute()




#create double entry accounting table

listOfSheetData = [["Date", "Account", "Amount+-", "Transaction Type", "Stock Name", "Broker", "Lot", "Shares"]]
destRange = "Robinhood - Transactions"
mapLeftObj = {"Dividend from ": {"transactionType": "Receive Dividend", "debitAccount": "Cash", "creditAccount": "Dividend Revenue", "stockNamePosition": 1},
       "Withdrawal to ": {"transactionType": "Cash To Owners", "debitAccount": "Capital Contributions", "creditAccount": "Cash", "stockName": "All Stocks", "lotInfo": "All Lots"},
       "Deposit from ": {"transactionType": "Cash From Owners", "debitAccount": "Cash", "creditAccount": "Capital Contributions", "stockName": "All Stocks", "lotInfo": "All Lots"},
       "Interest Payment": {"transactionType": "Receive Interest", "debitAccount": "Cash", "creditAccount": "Interest Revenue", "stockName": "Cssh", "lotInfo": "Cash"},
       "AKS from Robinhood": {"transactionType": "Receive Stock Gift", "debitAccount": "Investment Asset", "creditAccount": "Gain On Gift", "stockName": "AKS"}}

mapRightObj = {" Market Buy": {"transactionType": "Purchase Stock", "debitAccount": "Investment Asset", "creditAccount": "Cash", "stockNamePosition": 0}}


for transaction in transactionsList[1:]:

    locatedObj = {}
    searchString = ""

    for mapping in mapLeftObj:
        if transaction[0][:len(mapping)] == mapping:
            locatedObj = mapLeftObj[mapping]
            searchString = mapping

    if not locatedObj:
        for mapping in mapRightObj:
            if transaction[0][-len(mapping):] == mapping:
                locatedObj = mapRightObj[mapping]
                searchString = mapping

    # pp(transaction)

    if "stockName" in locatedObj:
        stockName = locatedObj["stockName"]
    else:
        stockName = transaction[0].split(searchString)[locatedObj["stockNamePosition"]]

    if "lotInfo" in locatedObj:
        lot = locatedObj["lotInfo"]
    elif locatedObj["transactionType"] == "Purchase Stock":
        lot = myPythonFunctions.convertSerialDate(transaction[1])
    else:
        lot = "Lot To Be Determined"

    listOfSheetData.append([transaction[1], locatedObj["debitAccount"], transaction[2], locatedObj["transactionType"], stockName, "Robinhood", lot, transaction[4]])
    listOfSheetData.append([transaction[1], locatedObj["creditAccount"], -transaction[2], locatedObj["transactionType"], stockName, "Robinhood", lot, ""])



for transaction in listOfSheetData:

    if transaction[6] == "Lot To Be Determined":
        filterFor = {1: "Investment Asset", 3: "Purchase Stock", 4: transaction[4]}

        if len(myPythonFunctions.filterListOfLists(listOfSheetData, filterFor)) == 1:
            transaction[6] = myPythonFunctions.convertSerialDate(myPythonFunctions.filterListOfLists(listOfSheetData, filterFor)[0][0])
            # pp(myPythonFunctions.filterListOfLists(listOfSheetData, filterFor))


valuesToWrite = {"values": listOfSheetData}
googleSheetsObj.values().update(spreadsheetId=spreadsheetID, range=destRange, valueInputOption="USER_ENTERED", body=valuesToWrite).execute()











    # currentValueList = str(listObj[indexOfRow][0]["value"]).split(" share")
    #
    # if :
    #     nextValueList = str(listObj[indexOfRow + 1][0]["value"]).split(" share")
    #
    # # pp(str(currentValueList) + " " + str(nextValueList))
    #
    # indivTransactionList.append(currentValue)
    #
    # if (len(nextValueList) != 2 and subCount == 3) or (len(currentValueList) == 2 and subCount == 4):
    #     subCount = 1
    #     # transactionsList.append(indivTransactionList)
    # #     pp(indivTransactionList)
    #     pp(indivTransactionList)
    #     indivTransactionList = []






#
#
#     if subCount > 3 and not matchObj:
#         subCount = 1
#
#         if len(indivTransactionList) == 3:
#             indivTransactionList.append("")
#             indivTransactionList.append("")
#
#         transactionsList.append(indivTransactionList)
#         indivTransactionList = []
#
#     indivTransactionList.append(currentValue)
#
#     if subCount > 3 and matchObj:
#         indivTransactionList.append(int(matchObj.group(0).split(" share")[0]))
#
#
#     subCount = subCount + 1
#
#
#
# transactionsList.append(indivTransactionList)
# # pp(transactionsList)
#