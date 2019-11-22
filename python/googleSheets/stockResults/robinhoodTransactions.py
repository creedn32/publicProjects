import sys, pathlib
sys.path.append(str(pathlib.Path.cwd().parents[0]))
sys.path.append(str(pathlib.Path.cwd().parents[1]))
from myPythonLibrary import myPythonFunctions
startTime = myPythonFunctions.startCode()

import importlib, datetime
googleSheetsFunctions = importlib.import_module("myGoogleSheetsPythonLibrary.googleSheetsFunctions")
googleSheetsAuthenticate = importlib.import_module("myGoogleSheetsPythonLibrary.googleSheetsAuthenticate")
from pprint import pprint as pp
# from datetime import date


sheetInfoObj = {0:
                    {"name": "Stock Results - Robinhood",
                    "id": "1oisLtuJJOZnU-nMvILNWO43_8w2rCT3V6vq3vMnAnCI",
                     "download":
                         {"Raw Data - Robinhood":
                              {},
                          "Transactions To Add - Robinhood":
                              {},
                          "Stock Name Map":
                              {}
                          }
                     },
                1:
                    {"name": "Stock Results",
                    "id": "1pjhFRIoB9mnbiMOj_hsFwsGth91l1oX_4kmeYrsT5mc"
                    }
                }


rangesToDownload = list(sheetInfoObj[0]["download"].keys())
saveJSONFile = False
googleSheetsObj = googleSheetsAuthenticate.authFunc()
googleSheetsDataWithGrid = googleSheetsFunctions.getDataWithGrid(sheetInfoObj[0]["id"], googleSheetsObj, rangesToDownload)
sleepTime = .7


finishSetupTime = myPythonFunctions.time.time()
print("Comment: Importing modules and setting up variables...Done. " + str(round(finishSetupTime - startTime, 3)) + " seconds")

if saveJSONFile:
    myPythonFunctions.saveFile(googleSheetsDataWithGrid, pathlib.Path(pathlib.Path.cwd().parents[3]/"privateData"/"stockResults"/"googleSheetsDataWithGrid.json"), finishSetupTime)
    print("Comment: Writing data to file...Done. " + str(round(myPythonFunctions.time.time() - finishSetupTime, 3)) + " seconds")



sheetInfoObj[0]["download"]["Raw Data - Robinhood"]["totalRows"] = googleSheetsFunctions.countRows(googleSheetsDataWithGrid, 0)
sheetInfoObj[0]["download"]["Raw Data - Robinhood"]["totalColumns"] = googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, 0)
sheetInfoObj[0]["download"]["Transactions To Add - Robinhood"]["totalRows"] = googleSheetsFunctions.countRows(googleSheetsDataWithGrid, 1)
sheetInfoObj[0]["download"]["Transactions To Add - Robinhood"]["totalColumns"] = googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, 1)
sheetInfoObj[0]["download"]["Stock Name Map"]["totalRows"] = googleSheetsFunctions.countRows(googleSheetsDataWithGrid, 2)
sheetInfoObj[0]["download"]["Stock Name Map"]["totalColumns"] = googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, 2)



#load downloaded sheets into lists

sheetInfoObj[0]["download"]["Raw Data - Robinhood"]["listObj"] = googleSheetsFunctions.extractValuesAndTypes(sheetInfoObj[0]["download"]["Raw Data - Robinhood"]["totalRows"], sheetInfoObj[0]["download"]["Raw Data - Robinhood"]["totalColumns"], googleSheetsDataWithGrid, 0)
sheetInfoObj[0]["download"]["Transactions To Add - Robinhood"]["listObj"] = googleSheetsFunctions.extractValues(sheetInfoObj[0]["download"]["Transactions To Add - Robinhood"]["totalRows"], sheetInfoObj[0]["download"]["Transactions To Add - Robinhood"]["totalColumns"], googleSheetsDataWithGrid, 1)

listToConvert = googleSheetsFunctions.extractValues(sheetInfoObj[0]["download"]["Stock Name Map"]["totalRows"], sheetInfoObj[0]["download"]["Stock Name Map"]["totalColumns"], googleSheetsDataWithGrid, 2)
sheetInfoObj[0]["download"]["Stock Name Map"]["dictObj"] = myPythonFunctions.convertTwoColumnListToDict(listToConvert, 1)



#create Data - Robinhood

subCount = 1
indivTransactionList = []
transactionsList = []

# fieldsObj = {1: "Description", 2: "Date", 3: "Amount", 4: "Details"}


for indexOfRow in range(0, sheetInfoObj[0]["download"]["Raw Data - Robinhood"]["totalRows"]):

    nextValueHasNoShares = True
    currentValue = sheetInfoObj[0]["download"]["Raw Data - Robinhood"]["listObj"][indexOfRow][0]["value"]

    if indexOfRow + 2 <= sheetInfoObj[0]["download"]["Raw Data - Robinhood"]["totalRows"]:
        if len(str(sheetInfoObj[0]["download"]["Raw Data - Robinhood"]["listObj"][indexOfRow + 1][0]["value"]).split(" share")) > 1:
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
    # pp(transaction[2])

    if transaction[2] != "Failed":

        transaction[2] = abs(transaction[2])

        if filterList:
            if transaction[1] > int(myPythonFunctions.convertDateToSerialDate(datetime.datetime(2018, 10, 31))):
                newTransactionsList.append(transaction)
        else:
            newTransactionsList.append(transaction)



transactionsList = newTransactionsList

transactionsList.insert(0, ["Description", "Date", "Amount", "Details", "Shares"])

# valuesToPopulate = {"values": transactionsList}
# googleSheetsObj.values().update(spreadsheetId=sheetInfoObj[0]["id"], range="Data - Robinhood", valueInputOption="USER_ENTERED", body=valuesToPopulate).execute()




#create Transactions - Robinhood

listOfSheetData = [["Date", "Account", "Amount+-", "Transaction Type", "Stock Name", "Broker", "Lot", "Shares"]]
mapLeftObj = {"Dividend from ": {"transactionType": "Dividend", "debitAccount": "Cash", "creditAccount": "Dividend Revenue", "stockNamePosition": 1},
       "Withdrawal to ": {"transactionType": "Owners - Pay", "debitAccount": "Capital Contributions", "creditAccount": "Cash", "stockName": "All Stocks", "lotInfo": "All Lots"},
       "Deposit from ": {"transactionType": "Owners - Receive Cash", "debitAccount": "Cash", "creditAccount": "Capital Contributions", "stockName": "All Stocks", "lotInfo": "All Lots"},
       "Interest Payment": {"transactionType": "Interest", "debitAccount": "Cash", "creditAccount": "Interest Revenue", "stockName": "Cash", "lotInfo": "Cash"},
       "AKS from Robinhood": {"transactionType": "Purchase - Stock Gift", "debitAccount": "Investment Asset", "creditAccount": "Gain On Gift", "stockName": "AKS"}}

mapRightObj = {" Market Buy": {"transactionType": "Purchase", "debitAccount": "Investment Asset", "creditAccount": "Cash", "stockNamePosition": 0}}


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
    elif transaction[0].split(searchString)[locatedObj["stockNamePosition"]] in ["Xperi", "Tessera Technologies, Inc. - Common Stock"]:
        stockName = "Xperi, formerly Tessera"
    else:
        stockName = transaction[0].split(searchString)[locatedObj["stockNamePosition"]]


    if "lotInfo" in locatedObj:
        lot = locatedObj["lotInfo"]
    elif locatedObj["transactionType"] in ["Purchase", "Purchase - Stock Gift", "Purchase - Stock From Merger"]:
        lot = myPythonFunctions.convertSerialDateToDateWithoutDashes(transaction[1])
    else:
        lot = "Lot To Be Determined"

    listOfSheetData.append([transaction[1], locatedObj["debitAccount"], transaction[2], locatedObj["transactionType"], stockName, "Robinhood", lot, transaction[4]])
    listOfSheetData.append([transaction[1], locatedObj["creditAccount"], -transaction[2], locatedObj["transactionType"], stockName, "Robinhood", lot, ""])



listOfSheetData.extend(sheetInfoObj[0]["download"]["Transactions To Add - Robinhood"]["listObj"][1:])


for transaction in listOfSheetData:

    if transaction[6] == "Lot To Be Determined":

        filterForLots = [{1: "Investment Asset", 3: "Purchase", 4: transaction[4]}, {1: "Investment Asset", 3: "Purchase - Stock From Merger", 4: transaction[4]}]

        if len(myPythonFunctions.filterListOfLists(listOfSheetData, filterForLots)) == 1:
            transaction[6] = myPythonFunctions.convertSerialDateToDateWithoutDashes(myPythonFunctions.filterListOfLists(listOfSheetData, filterForLots)[0][0])



unsoldStockSheet = [["Date", "Account", "Amount+-", "Transaction Type", "Stock Name", "Broker", "Lot", "Shares"]]
dateForUnsold = int(myPythonFunctions.convertDateToSerialDate(datetime.datetime.now()))
tranType = "Sale - Hypothetical"
googleSheetsTempData = None

createRequest = {
                          "requests": [
                            {
                              "addSheet": {
                                "properties": {
                                  "title": "tempSheet",
                                  "gridProperties": {
                                    "rowCount": 1,
                                    "columnCount": 1
                                  }
                                }
                              }
                            }
                          ]
                        }


googleSheetsObj.batchUpdate(spreadsheetId=sheetInfoObj[0]["id"], body=createRequest).execute()



for stockToFilter in sheetInfoObj[0]["download"]["Stock Name Map"]["dictObj"]:

    ticker = sheetInfoObj[0]["download"]["Stock Name Map"]["dictObj"][stockToFilter]
    filteredTransactions = myPythonFunctions.filterListOfLists(listOfSheetData, [{1: "Investment Asset", 4: stockToFilter, 5: "Robinhood"}])

    # pp(filteredTransactions)

    for item in filteredTransactions:

        if googleSheetsTempData:

            deleteRowsCols = {
                "requests": [
                    {
                        "deleteDimension": {
                            "range": {
                                "sheetId": googleSheetsTempData["sheets"][0]["properties"]["sheetId"],
                                "dimension": "ROWS",
                                "startIndex": 1,
                                "endIndex": 1000
                            }
                        }
                    },
                    {
                        "deleteDimension": {
                            "range": {
                                "sheetId": googleSheetsTempData["sheets"][0]["properties"]["sheetId"],
                                "dimension": "COLUMNS",
                                "startIndex": 1,
                                "endIndex": 1000
                            }
                        }
                    },
                ],
            }


            myPythonFunctions.time.sleep(sleepTime)
            googleSheetsObj.batchUpdate(spreadsheetId=sheetInfoObj[0]["id"], body=deleteRowsCols).execute()


        myPythonFunctions.time.sleep(sleepTime)
        googleSheetsObj.values().clear(spreadsheetId=sheetInfoObj[0]["id"], range="tempSheet", body={}).execute()


        unsoldLotList = []
        unsoldLotList.append(
            [dateForUnsold, "Cash", "=GOOGLEFINANCE(\"" + ticker + "\")*INDIRECT(\"H\"&ROW())", tranType, stockToFilter,
             "Robinhood", item[6], item[7]])
        unsoldLotList.append(
            [dateForUnsold, "Investment Asset", -item[2], tranType, stockToFilter, "Robinhood", item[6], item[7]])


        myPythonFunctions.time.sleep(sleepTime)
        googleSheetsObj.values().update(spreadsheetId=sheetInfoObj[0]["id"], range="tempSheet", valueInputOption="USER_ENTERED", body={"values": unsoldLotList}).execute()
        
        
        googleSheetsTempData = googleSheetsFunctions.getDataWithGrid(sheetInfoObj[0]["id"], googleSheetsObj, ["tempSheet"])


        listObj = googleSheetsFunctions.extractValues(googleSheetsFunctions.countRows(googleSheetsTempData, 0), googleSheetsFunctions.countColumns(googleSheetsTempData, 0), googleSheetsTempData, 0)
        netSum = myPythonFunctions.sumListOfLists(listObj, 2)

        if netSum < 0:
            account = "Loss On Sale - Hypothetical"
        else:
            account = "Gain On Sale - Hypothetical"


        unsoldLotList[0][2] = listObj[0][2]
        unsoldLotList.append([dateForUnsold, account, -netSum, tranType, stockToFilter, "Robinhood", item[6], item[7]])
        unsoldStockSheet.extend(unsoldLotList)


myPythonFunctions.time.sleep(sleepTime)
valuesToPopulate = {"values": unsoldStockSheet}
googleSheetsObj.values().update(spreadsheetId=sheetInfoObj[0]["id"], range="Transactions - Unsold Stock - Robinhood", valueInputOption="USER_ENTERED", body=valuesToPopulate).execute()




deleteRequest = {
    "requests": [
        {
            "deleteSheet": {
                "sheetId": googleSheetsTempData["sheets"][0]["properties"]["sheetId"]
            }
        }
    ]
}

myPythonFunctions.time.sleep(sleepTime)
googleSheetsObj.batchUpdate(spreadsheetId=sheetInfoObj[0]["id"], body=deleteRequest).execute()



listOfSheetData.extend(unsoldStockSheet[1:])
valuesToPopulate = {"values": listOfSheetData}
googleSheetsObj.values().update(spreadsheetId=sheetInfoObj[1]["id"], range="Transactions - Robinhood", valueInputOption="USER_ENTERED", body=valuesToPopulate).execute()








    # currentValueList = str(sheetInfoObj[0]["download"]["Raw Data - Robinhood"]["listObj"][indexOfRow][0]["value"]).split(" share")
    #
    # if :
    #     nextValueList = str(sheetInfoObj[0]["download"]["Raw Data - Robinhood"]["listObj"][indexOfRow + 1][0]["value"]).split(" share")
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