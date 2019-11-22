import sys, pathlib
sys.path.append(str(pathlib.Path.cwd().parents[0]/"myGoogleSheetsPythonLibrary"))
sys.path.append(str(pathlib.Path.cwd().parents[1]))
from myPythonLibrary import myPythonFunctions
startTime = myPythonFunctions.startCode()

# import robinhoodTransactions
import googleSheetsFunctions, googleSheetsAuthenticate
from pprint import pprint as pp

sheetsToDownload = ["Transactions", "Transactions - Robinhood", "Chart of Accounts", "Ticker Map"]
saveJSONFile = False
# spreadsheetID = "1yZfwzel6R3HTUtH5HIv7LEjAaoJDPESG6jCEz-b7jBw" #simple spreadsheet
spreadsheetID = "1pjhFRIoB9mnbiMOj_hsFwsGth91l1oX_4kmeYrsT5mc" #full spreadsheet
multiplyFactor = 1
tranDataListAccountIndex = 1


googleSheetsObj = googleSheetsAuthenticate.authFunc()
googleSheetsDataWithGrid = googleSheetsFunctions.getDataWithGrid(spreadsheetID, googleSheetsObj, sheetsToDownload)


finishSetupTime = myPythonFunctions.time.time()
print("Comment: Importing modules and setting up variables...Done. " + str(round(finishSetupTime - startTime, 3)) + " seconds")

if saveJSONFile:
    myPythonFunctions.saveFile(googleSheetsDataWithGrid, pathlib.Path(pathlib.Path.cwd().parents[3]/"privateData"/"stockResults"/"googleSheetsDataWithGrid.json"))
    print("Comment: Writing data to file...Done. " + str(round(myPythonFunctions.time.time() - finishSetupTime, 3)) + " seconds")


tranDataList = googleSheetsFunctions.extractValues(googleSheetsFunctions.countRows(googleSheetsDataWithGrid, sheetsToDownload.index("Transactions")), googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, sheetsToDownload.index("Transactions")), googleSheetsDataWithGrid, sheetsToDownload.index("Transactions"))
tranRobinhoodDataList = googleSheetsFunctions.extractValues(googleSheetsFunctions.countRows(googleSheetsDataWithGrid, sheetsToDownload.index("Transactions - Robinhood")), googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, sheetsToDownload.index("Transactions - Robinhood")), googleSheetsDataWithGrid, sheetsToDownload.index("Transactions - Robinhood"))
tranDataList.extend(tranRobinhoodDataList[1:len(tranRobinhoodDataList)])

tranRowTotal = len(tranDataList)
tranColTotal = len(tranDataList[0])

brokerageMap = {"Mt": "Motif",
                "Rh": "Robinhood"}


tickerDict = googleSheetsFunctions.createDictMapFromSheet(googleSheetsDataWithGrid, sheetsToDownload.index("Ticker Map"))
chartOfAccountsDict = googleSheetsFunctions.createDictMapFromSheet(googleSheetsDataWithGrid, sheetsToDownload.index("Chart of Accounts"))


#Scrub Transactions sheet

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
        tranDataList[indexOfRow].append(myPythonFunctions.convertSerialDateToYear(tranDataList[indexOfRow][0]))



googleSheetsFunctions.populateSheet(2, 100, "Transactions - Scrubbed", googleSheetsObj, spreadsheetID, tranDataList, False)

