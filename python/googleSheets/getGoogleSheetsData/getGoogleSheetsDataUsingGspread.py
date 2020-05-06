from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
import _myPyFunc
sys.path.append(str(Path(_myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'googleSheets'), 'myGoogleSheetsLibrary')))
import _myGoogleSheetsFunc

from pprint import pprint as p
import gspread, random

pathToRepos = _myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')
arrayOfPartsToAddToPath = ['privateData', 'python', 'googleCredentials']


useServiceAccount = True

if useServiceAccount:

    pathToCredentialsFileServiceAccount = _myPyFunc.addToPath(pathToRepos, arrayOfPartsToAddToPath + ['usingServiceAccount', 'jsonWithAPIKey.json'])
    saveToFile = False


    if saveToFile:
        googleSheetsAPIObj = _myGoogleSheetsFunc.getGoogleSheetsAPIObj(pathToCredentialsFileServiceAccount=pathToCredentialsFileServiceAccount)
        strOfAllFieldMasks = _myGoogleSheetsFunc.getStrOfAllFieldMasks(arrayOfAllFieldMasks=None)
        jsonOfAllSheets = _myGoogleSheetsFunc.getJSONOfAllSheets('1z7cfqKzg4C8jbySJvE7dV-WWUDyQnoVOmNf2GtDH4B8', googleSheetsAPIObj, fieldMask=strOfAllFieldMasks)
        _myPyFunc.saveToFile(jsonOfAllSheets, 'jsonOfAllSheets', 'json', _myPyFunc.replacePartOfPath(pathToThisPythonFile.parents[0], 'publicProjects', 'privateData'))


    gspObj = gspread.service_account(filename=pathToCredentialsFileServiceAccount)
    gspSpreadsheet = gspObj.open("Test")
    gspSheet1 = gspSpreadsheet.sheet1
    # gspSheet1.format('D4', {'textFormat': {'bold': True}})


    # randomInt = random.randint(1, 101)

    # for row in range(1, len(gspSheet1.get_all_values()) + 1):
    #     p(gspSheet1.cell(row, 1).value)
        # gspSheet1.update_cell(row, 1, randomInt)


    arrayOfSheet1 = gspSheet1.get_all_values()
    numberOfRows = len(arrayOfSheet1)
    numberOfColumnsInLastRow = len(arrayOfSheet1[numberOfRows - 1])
    addressOfSheet1 = 'R1C1' + ':' + 'R' + str(numberOfRows) + 'C' + str(numberOfColumnsInLastRow)


    for row in range(0, numberOfRows):
        for column in range(0, numberOfColumnsInLastRow):
            arrayOfSheet1[row][column] = ''

    gspSheet1.update(addressOfSheet1, arrayOfSheet1)

   

    randomInt = random.randint(1, 101)

    for rowIndex in range(0, numberOfRows):
        arrayOfSheet1[rowIndex][0] = randomInt

    arrayOfSheet1[numberOfRows - 1][numberOfColumnsInLastRow - 1] = 't'
    gspSheet1.update(addressOfSheet1, arrayOfSheet1)
    


 
    