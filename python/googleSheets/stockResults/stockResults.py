import sys, pathlib
sys.path.append(str(pathlib.Path.cwd().parents[0]))
sys.path.append(str(pathlib.Path.cwd().parents[1]))
from myPythonLibrary import myPythonFunctions
startTime = myPythonFunctions.startCode()

# import robinhoodTransactions

multiplyFactor = 1
accountColumn = 1
destRange = "Transactions - Scrubbed"
rangesToDownload = ["Transactions", "Transactions - Scrubbed", "Chart of Accounts", "Transactions - Robinhood", "Ticker Map"]
saveJSONFile = False
# spreadsheetID = "1yZfwzel6R3HTUtH5HIv7LEjAaoJDPESG6jCEz-b7jBw" #simple spreadsheet
spreadsheetID = "1pjhFRIoB9mnbiMOj_hsFwsGth91l1oX_4kmeYrsT5mc" #full spreadsheet


import importlib
googleSheetsFunctions = importlib.import_module("myGoogleSheetsPythonLibrary.googleSheetsFunctions")
googleSheetsAuthenticate = importlib.import_module("myGoogleSheetsPythonLibrary.googleSheetsAuthenticate")
from pprint import pprint as pp


googleSheetsObj = googleSheetsAuthenticate.authFunc()
googleSheetsDataWithGrid = googleSheetsFunctions.getDataWithGrid(spreadsheetID, googleSheetsObj, rangesToDownload)


finishSetupTime = myPythonFunctions.time.time()
print("Comment: Importing modules and setting up variables...Done. " + str(round(finishSetupTime - startTime, 3)) + " seconds")

if saveJSONFile:
    myPythonFunctions.saveFile(googleSheetsDataWithGrid, pathlib.Path(pathlib.Path.cwd().parents[3]/"privateData"/"stockResults"/"googleSheetsDataWithGrid.json"))
    print("Comment: Writing data to file...Done. " + str(round(myPythonFunctions.time.time() - finishSetupTime, 3)) + " seconds")




listOfSheetData = googleSheetsFunctions.extractValues(googleSheetsFunctions.countRows(googleSheetsDataWithGrid, 0), googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, 0), googleSheetsDataWithGrid, 0)
listOfSheetDataRobinhood = googleSheetsFunctions.extractValues(googleSheetsFunctions.countRows(googleSheetsDataWithGrid, 3), googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, 3), googleSheetsDataWithGrid, 3)
listOfSheetData.extend(listOfSheetDataRobinhood[1:len(listOfSheetDataRobinhood)])

numberOfRows = len(listOfSheetData)
numberOfColumns = len(listOfSheetData[0])

brokerageMap = {"Mt": "Motif",
                "Rh": "Robinhood"}



for indexOfRow in range(1, numberOfRows):
    listOfSheetData[indexOfRow][accountColumn] = listOfSheetData[indexOfRow][accountColumn].replace(" - " + listOfSheetData[indexOfRow][5], " ")
    listOfSheetData[indexOfRow][accountColumn] = listOfSheetData[indexOfRow][accountColumn].replace(
        " - " + str(listOfSheetData[indexOfRow][6]), " ")
    listOfSheetData[indexOfRow][accountColumn] = listOfSheetData[indexOfRow][accountColumn].replace(
        listOfSheetData[indexOfRow][4] + " - ", "")
    listOfSheetData[indexOfRow][accountColumn] = listOfSheetData[indexOfRow][accountColumn].rstrip()

    if listOfSheetData[indexOfRow][5] in brokerageMap:
        listOfSheetData[indexOfRow][5] = brokerageMap[listOfSheetData[indexOfRow][5]]

    listOfSheetData[indexOfRow][2] = listOfSheetData[indexOfRow][2] * multiplyFactor

    if listOfSheetData[indexOfRow][7] == "":
        listOfSheetData[indexOfRow][7] = 0



numberOfRowsChartOfAccounts = googleSheetsFunctions.countRows(googleSheetsDataWithGrid, 2)
numberOfColumnsChartOfAccounts = googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, 2)
chartOfAccountsDict = {}


for indexOfRow in range(1, numberOfRowsChartOfAccounts):

    mapDict = {}

    for indexOfColumn in range(1, numberOfColumnsChartOfAccounts):
        mapDict[googleSheetsFunctions.getCellValue(googleSheetsDataWithGrid, 2, 0, indexOfColumn)] = googleSheetsFunctions.getCellValue(googleSheetsDataWithGrid, 2, indexOfRow, indexOfColumn)

    chartOfAccountsDict[googleSheetsFunctions.getCellValue(googleSheetsDataWithGrid, 2, indexOfRow, 0)] = mapDict



for columnToMap in range(numberOfColumnsChartOfAccounts - 1, 0, -1):

    columnHeading = googleSheetsFunctions.getCellValue(googleSheetsDataWithGrid, 2, 0, columnToMap)

    for indexOfRow in range(0, numberOfRows):

        accountName = listOfSheetData[indexOfRow][accountColumn]
        # pp(accountName)

        if indexOfRow == 0:
            listOfSheetData[indexOfRow].insert(accountColumn + 1, columnHeading)
        else:
            # pp(chartOfAccountsDict[accountName][columnHeading])
            listOfSheetData[indexOfRow].insert(accountColumn + 1, chartOfAccountsDict[accountName][columnHeading])



valuesToWrite = {"values": listOfSheetData}
googleSheetsObj.values().update(spreadsheetId=spreadsheetID, range=destRange, valueInputOption="USER_ENTERED", body=valuesToWrite).execute()

