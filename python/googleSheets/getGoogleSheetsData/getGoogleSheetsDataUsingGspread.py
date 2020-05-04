from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
import _myPyFunc
sys.path.append(str(Path(_myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'googleSheets'), 'myGoogleSheetsLibrary')))
import _myGoogleSheetsFunc

from pprint import pprint as p
import gspread

pathToRepos = _myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')
arrayOfPartsToAddToPath = ['privateData', 'python', 'googleCredentials']


pathToCredentialsRetrievalFileServiceAccount = _myPyFunc.addToPath(pathToRepos, arrayOfPartsToAddToPath + ['usingServiceAccount', 'jsonWithAPIKey.json'])
useServiceAccount = True


if useServiceAccount:

    gc = gspread.service_account(filename=pathToCredentialsRetrievalFileServiceAccount)
    sh = gc.open("Test")

    print(sh.sheet1.get_all_values())
    sh.sheet1.format('D4', {'textFormat': {'bold': True}})


else:

    gc = gspread.oauth()
    sh = gc.open("Test")

    print(sh.sheet1.get_all_values())
    sh.sheet1.format('D4', {'textFormat': {'bold': True}})





pathToCredentialsDirectoryOAuth = _myPyFunc.addToPath(pathToRepos, arrayOfPartsToAddToPath + ['usingOAuth'])
googleSheetsAPIObj = _myGoogleSheetsFunc.getGoogleSheetsAPIObj(pathToCredentialsFileServiceAccount=pathToCredentialsRetrievalFileServiceAccount)
strOfAllFieldMasks = _myGoogleSheetsFunc.getStrOfAllFieldMasks(arrayOfAllFieldMasks=None)

jsonOfAllSheets = _myGoogleSheetsFunc.getJSONOfAllSheets('1z7cfqKzg4C8jbySJvE7dV-WWUDyQnoVOmNf2GtDH4B8', googleSheetsAPIObj, fieldMask=strOfAllFieldMasks)
_myPyFunc.saveToFile(jsonOfAllSheets, 'jsonOfAllSheets', 'json', _myPyFunc.replacePartOfPath(pathToThisPythonFile.parents[0], 'publicProjects', 'privateData'))
















# googleSheetsAPIObj = _myGoogleSheetsFunc.getGoogleSheetsAPIObj(pathToCredentialsDirectory=pathToCredentialsDirectory)
# spreadsheetIDStr = '1z7cfqKzg4C8jbySJvE7dV-WWUDyQnoVOmNf2GtDH4B8'
# sheetNameStr = 'Sheet1'

# arrayOfAllFieldMasks = [['sheets', 'properties', 'title'], ['sheets', 'data', 'rowData', 'values', 'formattedValue']]
# arrayOfAllFieldMasks = None
# strOfAllFieldMasks = _myGoogleSheetsFunc.getStrOfAllFieldMasks(arrayOfAllFieldMasks=arrayOfAllFieldMasks)

# p(_myGoogleSheetsFunc.getArrayOfOneSheet(googleSheetsAPIObj, spreadsheetIDStr, sheetNameStr, strOfAllFieldMasks)) #, pathToSaveFile=_myPyFunc.replacePartOfPath(pathToThisPythonFile.parents[0], 'publicProjects', 'privateData')))

# _myGoogleSheetsFunc.addColumnToOneSheet(googleSheetsAPIObj, spreadsheetIDStr, sheetNameStr, strOfAllFieldMasks)