
def clearArray(startingRow, endingRow, startingColumn, endingColumn, arrayOfSheet):

    if endingRow == -1:
        endingRow = len(arrayOfSheet) - 1
    if endingColumn == -1:
        endingColumn = len(arrayOfSheet[len(arrayOfSheet) - 1]) - 1

    for row in range(startingRow, endingRow + 1):
        for column in range(startingColumn, endingColumn + 1):
            arrayOfSheet[row][column] = ''

    return arrayOfSheet


def clearSheet(startingRow, endingRow, startingColumn, endingColumn, gspSheetOfArray):

    import gspread

    arrayOfSheet = gspSheetOfArray.get_all_values()

    if len(arrayOfSheet) > 0:
        
        arrayOfSheet = clearArray(startingRow, endingRow, startingColumn, endingColumn, gspSheetOfArray.get_all_values())
        numberOfRowsInArrayOfSheet = len(arrayOfSheet)
        numberOfColumnsInArrayOfSheet = len(arrayOfSheet[numberOfRowsInArrayOfSheet - 1])

        startingCell = 'R1C1'
        endingCell = 'R' + str(numberOfRowsInArrayOfSheet) + 'C' + str(numberOfColumnsInArrayOfSheet)
        addressOfSheet = startingCell + ':' + endingCell

        gspSheetOfArray.update(addressOfSheet, arrayOfSheet)
