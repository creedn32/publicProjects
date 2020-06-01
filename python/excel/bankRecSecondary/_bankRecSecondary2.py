#local application imports
from pathlib import Path
import sys
pathToThisPythonFile = Path(__file__).resolve()
sys.path.append(str(pathToThisPythonFile.parents[3]))
import herokuGorilla.backend.python.myPythonLibrary._myPyFunc as _myPyFunc

startTime = _myPyFunc.printElapsedTime(False, "Starting code")

import win32com.client

excelApp = win32com.client.gencache.EnsureDispatch('Excel.Application')
excelApp.Visible = False
excelApp.DisplayAlerts = False

# pp("Manual printout: " + str(Path.cwd().parents[3]) + "\\privateData\\python\\excel\\bankRecSecondary")
filePath = _myPyFunc.replacePartOfPath(pathToThisPythonFile.parents[0], 'publicProjects', 'privateData')
fileName = "Bank Rec"
fileExtension = ".xlsx"

rowAfterHeader = 2
bankDateOrigCol = 14

excelApp.Workbooks.Open(Path(filePath, fileName + fileExtension))
excelApp.Calculation = win32com.client.constants.xlCalculationManual
excelBackupWb = excelApp.Workbooks(fileName + fileExtension)
excelBackupWb.SaveAs(Filename=str(Path(filePath, fileName + " Before Running 2" + fileExtension)), FileFormat=51)
excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelBackupWb.Close()

excelApp.Workbooks.Open(Path(filePath, fileName + fileExtension))
excelApp.Calculation = win32com.client.constants.xlCalculationManual
excelWb = excelApp.Workbooks(fileName + fileExtension)

excelBankTableSheet = excelWb.Worksheets("Bank Table")
excelBankTableSearchSheet = excelWb.Worksheets("Bank Table Search")
excelBankTableSearchSheet.UsedRange.Clear()


splitTime = _myPyFunc.printElapsedTime(startTime, "Finished importing modules and intializing variables")


firstCell = excelBankTableSheet.Cells(1, 1)

excelBankTableSheet.Range(firstCell, excelBankTableSheet.Cells(firstCell.CurrentRegion.Rows.Count, firstCell.CurrentRegion.Columns.Count)).Copy(excelBankTableSearchSheet.Cells(1, 1))

excelBankTableSearchSheet.Cells.EntireColumn.AutoFit()

excelApp.DisplayAlerts = True
excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelWb.Save()
excelApp.Visible = True
_myPyFunc.printElapsedTime(startTime, "Total time to run code")
