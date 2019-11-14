from myPythonLibrary import myPythonFunctions
from pprint import pprint as pp
# import pathlib



# def hasFormattedValue(cell):
#
#     for item in cell:
#         if "formattedValue" in item:
#             return True
#
#     return False



def isWhite(cell):

    try:
        if cell["userEnteredFormat"]["backgroundColor"]["red"] + cell["userEnteredFormat"]["backgroundColor"]["green"] + cell["userEnteredFormat"]["backgroundColor"]["blue"] == 3:
            return True
    except KeyError:
        return True

    return False





def getDataWithGrid(spreadsheetIDStr, googleSheetsObj, rangesArgument):
    return googleSheetsObj.get(spreadsheetId=spreadsheetIDStr, includeGridData=True, ranges=rangesArgument).execute()





def getCellValue(dataObj, sheetPos, rowPos, colPos):
    sheetsData = myPythonFunctions.getFromDict(dataObj, "sheets")
    currentSheetData = myPythonFunctions.getFromList(sheetsData, sheetPos)
    dataOnSheet = myPythonFunctions.getFromList(myPythonFunctions.getFromDict(currentSheetData, "data"), 0)
    currentRowsData = myPythonFunctions.getFromDict(dataOnSheet, "rowData")
    currentRowData = myPythonFunctions.getFromDict(myPythonFunctions.getFromList(currentRowsData, rowPos), "values")
    try:
        return myPythonFunctions.getFromList(currentRowData, colPos)["formattedValue"]
    except:
        return ""





#
# def getCellValueNumber(dataObj, sheetPos, rowPos, colPos):
#     sheetsData = myPythonFunctions.getFromDict(dataObj, "sheets")
#     currentSheetData = myPythonFunctions.getFromList(sheetsData, sheetPos)
#     dataOnSheet = myPythonFunctions.getFromList(myPythonFunctions.getFromDict(currentSheetData, "data"), 0)
#     currentRowsData = myPythonFunctions.getFromDict(dataOnSheet, "rowData")
#     currentRowData = myPythonFunctions.getFromDict(myPythonFunctions.getFromList(currentRowsData, rowPos), "values")
#     try:
#         return myPythonFunctions.getFromList(currentRowData, colPos)["effectiveValue"]["numberValue"]
#     except:
#         return getCellValue(dataObj, sheetPos, rowPos, colPos)





def getCellValueEffective(dataObj, sheetPos, rowPos, colPos):
    sheetsData = myPythonFunctions.getFromDict(dataObj, "sheets")
    currentSheetData = myPythonFunctions.getFromList(sheetsData, sheetPos)
    dataOnSheet = myPythonFunctions.getFromList(myPythonFunctions.getFromDict(currentSheetData, "data"), 0)
    currentRowsData = myPythonFunctions.getFromDict(dataOnSheet, "rowData")
    currentRowData = myPythonFunctions.getFromDict(myPythonFunctions.getFromList(currentRowsData, rowPos), "values")
    try:
        return myPythonFunctions.getFromList(currentRowData, colPos)["effectiveValue"]
    except:
        return getCellValue(dataObj, sheetPos, rowPos, colPos)




#
# def createValuesData(numRows, numCols, dataObj):
#
#     listObj = []
#
#     for indexOfRow in range(0, numRows):
#         currentRowData = []
#
#         for indexOfColumn in range(0, numCols):
#             currentRowData.append(getCellValue(dataObj, 0, indexOfRow, indexOfColumn))
#
#         listObj.append(currentRowData)
#
#     return listObj








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






def extractValues(numRows, numCols, dataObj, sheetPos):

    listToReturn = []

    for indexOfRow in range(0, numRows):
        currentRowData = []

        for indexOfColumn in range(0, numCols):
            dictionary = getCellValueEffective(dataObj, sheetPos, indexOfRow, indexOfColumn)

            if not isinstance(dictionary, str):
                dictKey = list(dictionary.keys())[0]
                currentRowData.append(dictionary[dictKey])  # {"value": dictionary[dictKey], "type": dictKey})
            else:
                currentRowData.append("")  # {"value": "", "type": ""})

        listToReturn.append(currentRowData)


    return listToReturn




def extractValuesAndTypes(numRows, numCols, dataObj, sheetPos):

    listToReturn = []

    for indexOfRow in range(0, numRows):
        currentRowData = []

        for indexOfColumn in range(0, numCols):
            dictionary = getCellValueEffective(dataObj, sheetPos, indexOfRow, indexOfColumn)

            if not isinstance(dictionary, str):
                dictKey = list(dictionary.keys())[0]
                currentRowData.append({"value": dictionary[dictKey], "type": dictKey})
            else:
                currentRowData.append({"value": "", "type": ""})

        listToReturn.append(currentRowData)


    return listToReturn



