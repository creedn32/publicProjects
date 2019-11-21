from myPythonLibrary import myPythonFunctions
from pprint import pprint as pp


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




def reduceSheet(rowsToKeep, columnsToKeep, sheetName, googleSheetsObj, spreadsheetID):

    googleSheetsDataWithGrid = getDataWithGrid(spreadsheetID, googleSheetsObj, sheetName)
    totalRows =  countRows(googleSheetsDataWithGrid, 0)
    totalColumns = countColumns(googleSheetsDataWithGrid, 0)

    # pp(totalRows)
    # pp(totalColumns)

    if totalRows > rowsToKeep and totalColumns > columnsToKeep:

        requestObj = {
            "requests": [
                {
                    "deleteDimension": {
                        "range": {
                            "sheetId": googleSheetsDataWithGrid["sheets"][0]["properties"]["sheetId"],
                            "dimension": "ROWS",
                            "startIndex": rowsToKeep,
                            "endIndex": totalRows
                        }
                    }
                },
                {
                    "deleteDimension": {
                        "range": {
                            "sheetId": googleSheetsDataWithGrid["sheets"][0]["properties"]["sheetId"],
                            "dimension": "COLUMNS",
                            "startIndex": columnsToKeep,
                            "endIndex": totalColumns
                        }
                    }
                },
            ],
        }

        googleSheetsObj.batchUpdate(spreadsheetId=spreadsheetID, body=requestObj).execute()

    googleSheetsObj.values().clear(spreadsheetId=spreadsheetID, range=sheetName, body={}).execute()




def createDictMapFromSheet(googleSheetsDataWithGrid, sheetIndex):

    from collections import OrderedDict

    rowTotal = countRows(googleSheetsDataWithGrid, sheetIndex)
    colTotal = countColumns(googleSheetsDataWithGrid, sheetIndex)

    mappingDict = {}

    for indexOfRow in range(0, rowTotal):

        colDict = OrderedDict()

        for indexOfColumn in range(1, colTotal):

            colTitle = getCellValue(googleSheetsDataWithGrid, sheetIndex, 0, indexOfColumn)

            colDict[colTitle] = getCellValue(googleSheetsDataWithGrid, sheetIndex, indexOfRow, indexOfColumn)


        mappingDict[getCellValue(googleSheetsDataWithGrid, sheetIndex, indexOfRow, 0)] = colDict

    return mappingDict


def populateSheet(rowsToKeep, colsToKeep, sheetName, googleSheetsObj, spreadsheetID, valuesList):

    reduceSheet(rowsToKeep, colsToKeep, sheetName, googleSheetsObj, spreadsheetID)
    googleSheetsObj.values().update(spreadsheetId=spreadsheetID, range=sheetName, valueInputOption="USER_ENTERED", body={"values": valuesList}).execute()