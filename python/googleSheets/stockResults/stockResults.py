import sys, pathlib
sys.path.append(str(pathlib.Path.cwd().parents[0]/"myGoogleSheetsPythonLibrary"))
sys.path.append(str(pathlib.Path.cwd().parents[1]))
from myPythonLibrary import myPythonFunctions
startTime = myPythonFunctions.startCode()

# import robinhoodTransactions
import googleSheetsFunctions, googleSheetsAuthenticate
from pprint import pprint as pp

sheetsToDownload = ["Transactions", "Transactions - Scrubbed", "Chart of Accounts", "Transactions - Robinhood", "Ticker Map"]
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
# tranRobinhoodDataList = googleSheetsFunctions.extractValues(googleSheetsFunctions.countRows(googleSheetsDataWithGrid, sheetsToDownload.index("Transactions - Robinhood")), googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, sheetsToDownload.index("Transactions - Robinhood")), googleSheetsDataWithGrid, sheetsToDownload.index("Transactions - Robinhood"))
# tranDataList.extend(tranRobinhoodDataList[1:len(tranRobinhoodDataList)])

tranRowTotal = len(tranDataList)
tranColTotal = len(tranDataList[0])

brokerageMap = {"Mt": "Motif",
                "Rh": "Robinhood"}


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

    tranDataList[indexOfRow][2] = tranDataList[indexOfRow][2] * multiplyFactor

    if tranDataList[indexOfRow][7] == "":
        tranDataList[indexOfRow][7] = 0


#create map

chartOfAccountsDict = googleSheetsFunctions.createDictMapFromSheet(googleSheetsDataWithGrid, sheetsToDownload.index("Chart of Accounts"))


#use map

for indexOfRow in range(0, tranRowTotal):

    accountName = tranDataList[indexOfRow][tranDataListAccountIndex]

    for i in range(0, len(chartOfAccountsDict[accountName])):
        tranDataList[indexOfRow].insert(tranDataListAccountIndex + 1, list(chartOfAccountsDict[accountName].values())[i]) #chartOfAccountsDict[accountName][columnHeading])


googleSheetsFunctions.populateSheet(1, 1, "Transactions - Scrubbed", googleSheetsObj, spreadsheetID, tranDataList)

# valuesToWrite = {"values": tranDataList}
# googleSheetsObj.values().update(spreadsheetId=spreadsheetID, range=, valueInputOption="USER_ENTERED", body=valuesToWrite).execute()











# for columnToMap in range(googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, sheetsToDownload.index("Chart of Accounts")) - 1, 0, -1):

    # columnHeading = googleSheetsFunctions.getCellValue(googleSheetsDataWithGrid, sheetsToDownload.index("Chart of Accounts"), 0, columnToMap)


# pp(chartOfAccountsDict[accountName])


# if indexOfRow == 0:
#     tranDataList[indexOfRow].insert(tranDataListAccountIndex + 1, columnHeading)
# else:
#     pp(chartOfAccountsDict[accountName][columnHeading])
# tranDataList[indexOfRow].insert(tranDataListAccountIndex + 1, chartOfAccountsDict[accountName][columnHeading])


# chartAccRowTotal = googleSheetsFunctions.countRows(googleSheetsDataWithGrid, sheetsToDownload.index("Chart of Accounts"))
# chartAccColTotal = googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, sheetsToDownload.index("Chart of Accounts"))
# chartOfAccountsDict = {}



# for indexOfRow in range(1, chartAccRowTotal):
#
#     mapDict = {}
#
#     for indexOfColumn in range(1, chartAccColTotal):
#
#         colNameFromChartAcc = googleSheetsFunctions.getCellValue(googleSheetsDataWithGrid, sheetsToDownload.index("Chart of Accounts"), 0, indexOfColumn)
#         mapDict[colNameFromChartAcc] = googleSheetsFunctions.getCellValue(googleSheetsDataWithGrid, sheetsToDownload.index("Chart of Accounts"), indexOfRow, indexOfColumn)
#
#     chartOfAccountsDict[googleSheetsFunctions.getCellValue(googleSheetsDataWithGrid, sheetsToDownload.index("Chart of Accounts"), indexOfRow, 0)] = mapDict


# pp(chartOfAccountsDict)
