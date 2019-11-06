from myPythonLibrary import myPythonFunctions
from pprint import pprint as pp
# import pathlib



def hasFormattedValue(cell):

    for item in cell:
        if "formattedValue" in item:
            return True

    return False



def isWhite(cell):

    try:
        if cell["userEnteredFormat"]["backgroundColor"]["red"] + cell["userEnteredFormat"]["backgroundColor"]["green"] + cell["userEnteredFormat"]["backgroundColor"]["blue"] == 3:
            return True
    except KeyError:
        return True

    return False





def getDataWithGrid(spreadsheetIDStr, googleSheetsObj):
    return googleSheetsObj.get(spreadsheetId=spreadsheetIDStr, includeGridData=True).execute()





def getCellValue(dataObj, sheetPos, rowPos, colPos):
    sheetsData = myPythonFunctions.getFromDict(dataObj, "sheets")
    currentSheetData = myPythonFunctions.getFromList(sheetsData, sheetPos)
    dataOnSheet = myPythonFunctions.getFromList(myPythonFunctions.getFromDict(currentSheetData, "data"), 0)
    currentRowsData = myPythonFunctions.getFromDict(dataOnSheet, "rowData")
    currentRowData = myPythonFunctions.getFromDict(myPythonFunctions.getFromList(currentRowsData, rowPos), "values")
    try:
        currentCellData = myPythonFunctions.getFromList(currentRowData, colPos)
    except IndexError:
        currentCellData = {}

    return currentCellData.get("formattedValue", "")





def countRows(dataObj, sheetPos):
    sheetsData = myPythonFunctions.getFromDict(dataObj, "sheets")

    # saveFile(sheetsData, pathlib.Path(pathlib.Path.cwd().parents[3]/"privateData"/"stockResults"/"sheetsData.json"))
    # for i in sheetsData:
    #     pp(str(i)[:50])

    currentSheetData = myPythonFunctions.getFromList(sheetsData, sheetPos)
    dataOnSheet = myPythonFunctions.getFromList(myPythonFunctions.getFromDict(currentSheetData, "data"), 0)
    return len(myPythonFunctions.getFromDict(dataOnSheet, "rowData"))






def countColumns(dataObj, sheetPos):
    sheetsData = myPythonFunctions.getFromDict(dataObj, "sheets")
    currentSheetData = myPythonFunctions.getFromList(sheetsData, sheetPos)
    dataOnSheet = myPythonFunctions.getFromList(myPythonFunctions.getFromDict(currentSheetData, "data"), 0)
    currentRowsData = myPythonFunctions.getFromDict(dataOnSheet, "rowData")
    currentRowData = myPythonFunctions.getFromDict(myPythonFunctions.getFromList(currentRowsData, 0), "values")
    return len(currentRowData)





def saveFile(dataObj, path):

    from pprint import pprint as pp

    with open(path, "wt") as out:
        pp(dataObj, stream=out)
