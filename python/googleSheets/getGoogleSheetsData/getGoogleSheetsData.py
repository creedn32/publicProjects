from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
import _myPyFunc
sys.path.append(str(Path(pathToThisPythonFile.parents[1], 'myGoogleSheetsLibrary')))
import _myGoogleSheetsFunc

from pprint import pprint as p


googleSheetsAPIObj = _myGoogleSheetsFunc.getGoogleSheetsAPIObj(['privateData', 'python', 'googleCredentials'])
fieldMask = 'sheets/properties/title,sheets/data/rowData/values/formattedValue'
spreadsheetIDStr = "1nR8wJISZjeJh6DCBf1OTpiG6rdY5DyyUtDI763axGhg"

spreadsheetDataInJSONFormat = _myGoogleSheetsFunc.getDataInJSONFormat(spreadsheetIDStr, googleSheetsAPIObj, fieldMask)
# _myPyFunc.saveToFile(googleSpreadsheetDataInJSONFormat, 'googleSpreadsheetDataInJSONFormat', 'json', _myPyFunc.replacePartOfPath(pathToThisPythonFileDirectory, 'publicProjects', 'privateData'))
sheetDataInJSONFormat = _myGoogleSheetsFunc.getJSONForSheet(spreadsheetDataInJSONFormat, 'Bank Transfers')
sheetDataInArray = _myGoogleSheetsFunc.getArrayFromJSONData(sheetDataInJSONFormat)


p(sheetDataInArray)