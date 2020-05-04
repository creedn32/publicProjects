#also use service account
#get all spreadsheet data and look for if the data has the empty cells


from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
import _myPyFunc
# sys.path.append(str(Path(_myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'googleSheets'), 'myGoogleSheetsLibrary')))
# import _myGoogleSheetsFunc

from pprint import pprint as p
import gspread


useServiceAccount = True
pathToRepos = _myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')
arrayOfPartsToAddToPath = ['privateData', 'python', 'googleCredentials', 'usingServiceAccount', 'jsonForCredentialsRetrieval.json']
pathToCredentialsRetrievalFile = _myPyFunc.addToPath(pathToRepos, arrayOfPartsToAddToPath)



if useServiceAccount:
    
    gc = gspread.service_account(filename=pathToCredentialsRetrievalFile)
    sh = gc.open("Test")

    print(sh.sheet1.get('A1'))

else:

    gc = gspread.oauth()

    sh = gc.open("Test")

    print(sh.sheet1.get('B1'))
    print(sh.sheet1.get_all_values())

    sh.sheet1.format('A1', {'textFormat': {'bold': True}})
    sh.sheet1.update_cell(1, 1, 'bingo')




















# googleSheetsAPIObj = _myGoogleSheetsFunc.getGoogleSheetsAPIObj(pathToCredentialsDirectory=pathToCredentialsDirectory)
# spreadsheetIDStr = '1z7cfqKzg4C8jbySJvE7dV-WWUDyQnoVOmNf2GtDH4B8'
# sheetNameStr = 'Sheet1'

# arrayOfAllFieldMasks = [['sheets', 'properties', 'title'], ['sheets', 'data', 'rowData', 'values', 'formattedValue']]
# arrayOfAllFieldMasks = None
# strOfAllFieldMasks = _myGoogleSheetsFunc.getStrOfAllFieldMasks(arrayOfAllFieldMasks=arrayOfAllFieldMasks)

# p(_myGoogleSheetsFunc.getArrayOfOneSheet(googleSheetsAPIObj, spreadsheetIDStr, sheetNameStr, strOfAllFieldMasks)) #, pathToSaveFile=_myPyFunc.replacePartOfPath(pathToThisPythonFile.parents[0], 'publicProjects', 'privateData')))

# _myGoogleSheetsFunc.addColumnToOneSheet(googleSheetsAPIObj, spreadsheetIDStr, sheetNameStr, strOfAllFieldMasks)