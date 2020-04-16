from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
import _myPyFunc
sys.path.append(str(Path(_myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'googleSheets'), 'myGoogleSheetsLibrary')))
import _myGoogleSheetsFunc

from pprint import pprint as p


googleSheetsAPIObj = _myGoogleSheetsFunc.getGoogleSheetsAPIObj(['privateData', 'python', 'googleCredentials'])
fieldMasksArray = [['sheets', 'properties', 'title'], ['sheets', 'data', 'rowData', 'values', 'formattedValue']]
fieldMasksArray = [['sheets', 'properties', 'title'], ['sheets', 'data', 'rowData', 'values']]

spreadsheetIDStr = '1z7cfqKzg4C8jbySJvE7dV-WWUDyQnoVOmNf2GtDH4B8'

spreadsheetDataInJSONFormat = _myGoogleSheetsFunc.getDataInJSONFormat(spreadsheetIDStr, googleSheetsAPIObj, _myGoogleSheetsFunc.getFieldMasksStr(fieldMasksArray))
# p(spreadsheetDataInJSONFormat)
# p('done')
# spreadsheetDataInJSONFormat = _myGoogleSheetsFunc.getDataInJSONFormat(spreadsheetIDStr, googleSheetsAPIObj)
# p(spreadsheetDataInJSONFormat)
sheetDataInJSONFormat = _myGoogleSheetsFunc.getJSONForSheet(spreadsheetDataInJSONFormat, 'Sheet1')
# p(sheetDataInJSONFormat)
sheetDataInArray = _myGoogleSheetsFunc.getArrayFromJSONData(sheetDataInJSONFormat)


p(sheetDataInArray)