
def clearArray(arrayOfSheet, startingRow, endingRow, startingColumn, endingColumn):

    if endingRow == -1:
        endingRow = len(arrayOfSheet) - 1
    if endingColumn == -1:
        endingColumn = len(arrayOfSheet[len(arrayOfSheet) - 1]) - 1

    for row in range(startingRow, endingRow + 1):
        for column in range(startingColumn, endingColumn + 1):
            arrayOfSheet[row][column] = ''

    return arrayOfSheet