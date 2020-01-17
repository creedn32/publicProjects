import sys, pathlib
sys.path.append(str(pathlib.Path.cwd().parents[1]))
from myPyLib import myPyFunc, myGoogleSheetsFunc

startTime = myPyFunc.printElapsedTime(False, "Starting code")

import win32com.client

excelApp = win32com.client.gencache.EnsureDispatch('Excel.Application')
excelApp.Visible = False
excelApp.DisplayAlerts = False
filePath = str(pathlib.Path.cwd().parents[3]) + "\\privateData\\bankRecSecondary"
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


splitTime = myPyFunc.printElapsedTime(startTime, "Finished importing modules and intializing variables")


firstCell = excelBankTableSheet.Cells(1, 1)

excelBankTableSheet.Range(firstCell, excelBankTableSheet.Cells(firstCell.CurrentRegion.Rows.Count, firstCell.CurrentRegion.Columns.Count)).Copy(excelBankTableSearchSheet.Cells(1, 1))

excelBankTableSearchSheet.Cells.EntireColumn.AutoFit()

excelApp.DisplayAlerts = True
excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelWb.Save()
excelApp.Visible = True
myPyFunc.printElapsedTime(startTime, "Total time to run code")
