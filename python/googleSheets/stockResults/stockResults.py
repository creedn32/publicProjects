import sys, pathlib, time
sys.path.append(str(pathlib.Path.cwd().parents[1])) #for myPyLib
from myPyLib import myPyFunc, myGoogleSheetsFunc

startTime = time.time()
print("Comment: Importing modules and setting up variables...")


import robinhoodTransactions
from pprint import pprint as pp

googleSheetsObj = myGoogleSheetsFunc.authFunc()

sheetsToDownload = ["Transactions", "Transactions - Robinhood", "Chart of Accounts", "Ticker Map"]
spreadsheetID = "1pjhFRIoB9mnbiMOj_hsFwsGth91l1oX_4kmeYrsT5mc"
googleSheetsDataWithGrid = myGoogleSheetsFunc.getDataWithGrid(spreadsheetID, googleSheetsObj, sheetsToDownload)

tranDataList = myGoogleSheetsFunc.extractValues(myGoogleSheetsFunc.countRows(googleSheetsDataWithGrid, sheetsToDownload.index("Transactions")), myGoogleSheetsFunc.countColumns(googleSheetsDataWithGrid, sheetsToDownload.index("Transactions")), googleSheetsDataWithGrid, sheetsToDownload.index("Transactions"))
tranRobinhoodDataList = myGoogleSheetsFunc.extractValues(myGoogleSheetsFunc.countRows(googleSheetsDataWithGrid, sheetsToDownload.index("Transactions - Robinhood")), myGoogleSheetsFunc.countColumns(googleSheetsDataWithGrid, sheetsToDownload.index("Transactions - Robinhood")), googleSheetsDataWithGrid, sheetsToDownload.index("Transactions - Robinhood"))
tranDataList.extend(tranRobinhoodDataList[1:len(tranRobinhoodDataList)])
tranDataList = [item for item in tranDataList if item[2] != 0]

chartOfAccountsDict = myGoogleSheetsFunc.createDictMapFromSheet(googleSheetsDataWithGrid, sheetsToDownload.index("Chart of Accounts"))
tickerDict = myGoogleSheetsFunc.createDictMapFromSheet(googleSheetsDataWithGrid, sheetsToDownload.index("Ticker Map"))

tranRowTotal = len(tranDataList)

print("Comment: Importing modules and setting up variables...Done. " + str(round(time.time() - startTime, 3)) + " seconds")



#Scrub Transactions sheet

brokerageMap = {"Mt": "Motif",
                "Rh": "Robinhood"}

multiplyFactor = 1
tranDataListAccountIndex = 1


for indexOfRow in range(1, tranRowTotal):

    tranDataList[indexOfRow][tranDataListAccountIndex] = tranDataList[indexOfRow][tranDataListAccountIndex].replace(" - " + tranDataList[indexOfRow][5], " ")
    tranDataList[indexOfRow][tranDataListAccountIndex] = tranDataList[indexOfRow][tranDataListAccountIndex].replace(
        " - " + str(tranDataList[indexOfRow][6]), " ")
    tranDataList[indexOfRow][tranDataListAccountIndex] = tranDataList[indexOfRow][tranDataListAccountIndex].replace(
        tranDataList[indexOfRow][4] + " - ", "")
    tranDataList[indexOfRow][tranDataListAccountIndex] = tranDataList[indexOfRow][tranDataListAccountIndex].rstrip()

    if tranDataList[indexOfRow][5] in brokerageMap:
        tranDataList[indexOfRow][5] = brokerageMap[tranDataList[indexOfRow][5]]

    ticker = tranDataList[indexOfRow][4]

    if ticker in tickerDict:

        for key in tickerDict[ticker]:
            tranDataList[indexOfRow][4] = tickerDict[ticker][key]

    tranDataList[indexOfRow][2] = tranDataList[indexOfRow][2] * multiplyFactor

    if tranDataList[indexOfRow][7] == "":
        tranDataList[indexOfRow][7] = 0



#use map

for indexOfRow in range(0, tranRowTotal):

    accountName = tranDataList[indexOfRow][tranDataListAccountIndex]

    for i in range(0, len(chartOfAccountsDict[accountName])):
        tranDataList[indexOfRow].insert(tranDataListAccountIndex + 1, list(chartOfAccountsDict[accountName].values())[i])

    if indexOfRow == 0:
        tranDataList[indexOfRow].append("Year")
    else:
        tranDataList[indexOfRow].append(myPyFunc.convertSerialDateToYear(tranDataList[indexOfRow][0]))



myGoogleSheetsFunc.populateSheet(2, 100, "Transactions - Scrubbed", googleSheetsObj, spreadsheetID, tranDataList, False)
