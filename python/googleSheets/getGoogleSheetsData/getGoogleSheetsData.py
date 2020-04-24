from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
import _myPyFunc
sys.path.append(str(Path(_myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'googleSheets'), 'myGoogleSheetsLibrary')))
import _myGoogleSheetsFunc

from pprint import pprint as p


pathToRepos = _myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')
arrayOfPartsToAddToPath = ['privateData', 'python', 'googleCredentials']
pathToCredentialsDirectory = _myPyFunc.addToPath(pathToRepos, arrayOfPartsToAddToPath)

googleSheetsAPIObj = _myGoogleSheetsFunc.getGoogleSheetsAPIObj(pathToCredentialsDirectory=pathToCredentialsDirectory)
spreadsheetIDStr = '1z7cfqKzg4C8jbySJvE7dV-WWUDyQnoVOmNf2GtDH4B8'
sheetNameStr = 'Sheet1'

arrayOfAllFieldMasks = [['sheets', 'properties', 'title'], ['sheets', 'data', 'rowData', 'values', 'formattedValue']]
arrayOfAllFieldMasks = None
strOfAllFieldMasks = _myGoogleSheetsFunc.getStrOfAllFieldMasks(arrayOfAllFieldMasks=arrayOfAllFieldMasks)

p(_myGoogleSheetsFunc.getArrayOfOneSheet(googleSheetsAPIObj, spreadsheetIDStr, sheetNameStr, strOfAllFieldMasks)) #, pathToSaveFile=_myPyFunc.replacePartOfPath(pathToThisPythonFile.parents[0], 'publicProjects', 'privateData')))

_myGoogleSheetsFunc.addColumnToOneSheet(googleSheetsAPIObj, spreadsheetIDStr, sheetNameStr, strOfAllFieldMasks)