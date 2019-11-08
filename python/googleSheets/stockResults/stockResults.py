import sys, pathlib
sys.path.append(str(pathlib.Path.cwd().parents[0]))
sys.path.append(str(pathlib.Path.cwd().parents[1]))
from myPythonLibrary import myPythonFunctions
startTime = myPythonFunctions.startCode()

multiplyFactor = 1
accountColumn = 1
listOfSheetData = []
destRange = "Scrubbed Transactions"
rangesToDownload = ["Transactions", "Scrubbed Transactions", "Chart of Accounts"]

import importlib
googleSheetsFunctions = importlib.import_module("myGoogleSheetsPythonLibrary.googleSheetsFunctions")
googleSheetsAuthenticate = importlib.import_module("myGoogleSheetsPythonLibrary.googleSheetsAuthenticate")
from pprint import pprint as pp


# spreadsheetID = "1yZfwzel6R3HTUtH5HIv7LEjAaoJDPESG6jCEz-b7jBw" #simple spreadsheet
spreadsheetID = "1pjhFRIoB9mnbiMOj_hsFwsGth91l1oX_4kmeYrsT5mc" #full spreadsheet


googleSheetsObj = googleSheetsAuthenticate.authFunc()
googleSheetsDataWithGrid = googleSheetsFunctions.getDataWithGrid(spreadsheetID, googleSheetsObj, optionalArgumentRanges=rangesToDownload)

# googleSheetsDataWithGrid = {"sheets": []}
# sheetsData = myPythonFunctions.getFromDict(googleSheetsDataWithGridWithPivot, "sheets")
#
# for sheetPos in range(0, 3):
#     googleSheetsDataWithGrid["sheets"].append(myPythonFunctions.getFromList(sheetsData, sheetPos))


# pp(googleSheetsDataWithGrid["sheets"][2])
# pp(myPythonFunctions.getFromList(sheetsData, 2))


finishSetupTime = myPythonFunctions.time.time()
print("Comment: Importing modules and setting up variables...Done. " + str(round(finishSetupTime - startTime, 3)) + " seconds")

# myPythonFunctions.saveFile(googleSheetsDataWithGrid, pathlib.Path(pathlib.Path.cwd().parents[3]/"privateData"/"stockResults"/"googleSheetsDataWithGrid.json"), finishSetupTime)


numberOfRows = googleSheetsFunctions.countRows(googleSheetsDataWithGrid, 0)
numberOfColumns = googleSheetsFunctions.countColumns(googleSheetsDataWithGrid, 0)



for indexOfRow in range(0, numberOfRows):
    currentRowData = []

    for indexOfColumn in range(0, numberOfColumns):
        currentRowData.append(googleSheetsFunctions.getCellValue(googleSheetsDataWithGrid, 0, indexOfRow, indexOfColumn))

    listOfSheetData.append(currentRowData)



# for indexOfRow in range(0, numberOfRows):
#     if listOfSheetData[indexOfRow][1] == "Cash":
#         listOfSheetData[indexOfRow][1] = "Cash (General)"


for indexOfRow in range(1, numberOfRows):
    listOfSheetData[indexOfRow][accountColumn] = listOfSheetData[indexOfRow][accountColumn].replace(" - " + listOfSheetData[indexOfRow][5], " ")

for indexOfRow in range(1, numberOfRows):
    listOfSheetData[indexOfRow][accountColumn] = listOfSheetData[indexOfRow][accountColumn].replace(" - " + listOfSheetData[indexOfRow][6], " ")

for indexOfRow in range(1, numberOfRows):
    listOfSheetData[indexOfRow][accountColumn] = listOfSheetData[indexOfRow][accountColumn].replace(listOfSheetData[indexOfRow][4] + " - ", "")

for indexOfRow in range(1, numberOfRows):
    listOfSheetData[indexOfRow][accountColumn] = listOfSheetData[indexOfRow][accountColumn].rstrip()

brokerageMap = {"Mt": "Motif",
                "Rh": "Robinhood"}

for indexOfRow in range(1, numberOfRows):
    listOfSheetData[indexOfRow][5] = brokerageMap[listOfSheetData[indexOfRow][5]]


for indexOfRow in range(1, numberOfRows):
    listOfSheetData[indexOfRow][2] = listOfSheetData[indexOfRow][2] #float(listOfSheetData[indexOfRow][2]) * multiplyFactor



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

        if indexOfRow == 0:
            listOfSheetData[indexOfRow].insert(accountColumn + 1, columnHeading)
        else:
            listOfSheetData[indexOfRow].insert(accountColumn + 1, chartOfAccountsDict[accountName][columnHeading])




valuesToWrite = {"values": listOfSheetData}
googleSheetsObj.values().update(spreadsheetId=spreadsheetID, range=destRange, valueInputOption="USER_ENTERED", body=valuesToWrite).execute()
