from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
import _myPyFunc
sys.path.append(str(Path(_myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'googleSheets'), 'myGoogleSheetsLibrary')))
import _myGoogleSheetsFunc

from pprint import pprint as p

pathToThisPythonFileDirectory = pathToThisPythonFile.parents[0]
arrayOfPathParts = ['privateData', 'python', 'googleCredentials']
googleSheetsAPIObj = _myGoogleSheetsFunc.getGoogleSheetsAPIObj(arrayOfPathParts)
fieldMasksArray = [['sheets', 'properties', 'title'], ['sheets', 'data', 'rowData', 'values', 'formattedValue']]
fieldMasksArray = None

spreadsheetIDStr = '1z7cfqKzg4C8jbySJvE7dV-WWUDyQnoVOmNf2GtDH4B8'

spreadsheetDataInJSONFormat = _myGoogleSheetsFunc.getDataInJSONFormat(spreadsheetIDStr, googleSheetsAPIObj, fieldMask=_myGoogleSheetsFunc.getFieldMasksStr(fieldMasksArray=fieldMasksArray))
# _myPyFunc.saveToFile(spreadsheetDataInJSONFormat, 'spreadsheetDataInJSONFormat', 'json', _myPyFunc.replacePartOfPath(pathToThisPythonFileDirectory, 'publicProjects', 'privateData'))
sheetDataInJSONFormat = _myGoogleSheetsFunc.getJSONForSheet(spreadsheetDataInJSONFormat, 'Sheet1')
# _myPyFunc.saveToFile(sheetDataInJSONFormat, 'sheetDataInJSONFormat', 'json', _myPyFunc.replacePartOfPath(pathToThisPythonFileDirectory, 'publicProjects', 'privateData'))
sheetDataInArray = _myGoogleSheetsFunc.getArrayFromJSONData(sheetDataInJSONFormat)
p(sheetDataInArray)


