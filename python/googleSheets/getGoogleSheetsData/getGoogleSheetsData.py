from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
import _myPyFunc
sys.path.append(_myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'myGoogleSheetsLibrary'))
import _myGoogleSheetsFunc

from pprint import pprint as p


googleSheetsAPIObj = _myGoogleSheetsFunc.getGoogleSheetsAPIObj(['privateData', 'python', 'googleCredentials'])
fieldMasksArray = [['sheets', 'properties', 'title'], ['sheets', 'data', 'rowData', 'values', 'formattedValue']]

spreadsheetIDStr = '1z7cfqKzg4C8jbySJvE7dV-WWUDyQnoVOmNf2GtDH4B8'

spreadsheetDataInJSONFormat = _myGoogleSheetsFunc.getDataInJSONFormat(spreadsheetIDStr, googleSheetsAPIObj, _myGoogleSheetsFunc.getFieldMasksStr(fieldMasksArray))
sheetDataInJSONFormat = _myGoogleSheetsFunc.getJSONForSheet(spreadsheetDataInJSONFormat, 'Sheet1')
sheetDataInArray = _myGoogleSheetsFunc.getArrayFromJSONData(sheetDataInJSONFormat)


p(sheetDataInArray)