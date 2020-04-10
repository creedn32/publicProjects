import pathlib
pathToThisPythonFile = pathlib.Path(__file__).resolve()
import sys
sys.path.append(str(pathlib.Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
import _myPyFunc


splitTime = _myPyFunc.printElapsedTime(False, "Starting code")
from pprint import pprint as pp

import win32com.client


excelApp = win32com.client.gencache.EnsureDispatch('Excel.Application')
excelApp.Visible = False
excelApp.DisplayAlerts = False
filePath = str(_myPyFunc.replacePartOfPath(pathToThisPythonFile.parents[0], 'publicProjects', 'privateData'))
fileName = "Bank Rec"
fileExtension = ".xlsx"

rowAfterHeader = 2
bankDateOrigCol = 14

excelApp.Workbooks.Open(filePath + "\\" + fileName + fileExtension)
excelApp.Calculation = win32com.client.constants.xlCalculationManual
excelBackupWb = excelApp.Workbooks(fileName + fileExtension)
excelBackupWb.SaveAs(Filename=filePath + "\\" + fileName + " Before Running 2" + fileExtension, FileFormat=51)
excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelBackupWb.Close()

excelApp.Workbooks.Open(filePath + "\\" + fileName + fileExtension)
excelApp.Calculation = win32com.client.constants.xlCalculationManual
excelWb = excelApp.Workbooks(fileName + fileExtension)

excelBankTableSheet = excelWb.Worksheets("Bank Table")
excelBankTableSearchSheet = excelWb.Worksheets("Bank Table Search")
excelBankTableSearchSheet.UsedRange.Clear()


splitTime = _myPyFunc.printElapsedTime(splitTime, "Finished importing modules and intializing variables")

firstCell = excelBankTableSheet.Cells(1, 1)

excelBankTableSheet.Range(firstCell, excelBankTableSheet.Cells(firstCell.CurrentRegion.Rows.Count, firstCell.CurrentRegion.Columns.Count - 1)).Copy(excelBankTableSearchSheet.Cells(1, 1))
excelBankTableSheet.Range(excelBankTableSheet.Cells(rowAfterHeader, bankDateOrigCol), excelBankTableSheet.Cells(rowAfterHeader, bankDateOrigCol).End(win32com.client.constants.xlDown)).Copy(excelBankTableSearchSheet.Cells(rowAfterHeader, 2))

excelBankTableSearchSheet.Cells.EntireColumn.AutoFit()

excelApp.DisplayAlerts = True
excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelWb.Save()
excelApp.Visible = True
splitTime = _myPyFunc.printElapsedTime(splitTime, "Finished bank_rec_2")
