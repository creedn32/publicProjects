print("Cmt: Importing modules...")

import time, win32com.client, pathlib

startTime = time.time()
print("Cmt: Importing modules...Done.")
print("Cmt: Open and connect to file...")

excelApp = win32com.client.gencache.EnsureDispatch('Excel.Application')
excelApp.Visible = False
excelApp.DisplayAlerts = False
filePath = str(pathlib.Path.cwd().parents[3]) + "\\privateData\\bankRecPrimary"
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


print("Cmt: Open and connect to file...Done.")

firstCell = excelBankTableSheet.Cells(1, 1)

excelBankTableSheet.Range(firstCell, excelBankTableSheet.Cells(firstCell.CurrentRegion.Rows.Count, firstCell.CurrentRegion.Columns.Count - 1)).Copy(excelBankTableSearchSheet.Cells(1, 1))
excelBankTableSheet.Range(excelBankTableSheet.Cells(rowAfterHeader, bankDateOrigCol), excelBankTableSheet.Cells(rowAfterHeader, bankDateOrigCol).End(win32com.client.constants.xlDown)).Copy(excelBankTableSearchSheet.Cells(rowAfterHeader, 2))

excelBankTableSearchSheet.Cells.EntireColumn.AutoFit()

excelApp.DisplayAlerts = True
excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelWb.Save()
excelApp.Visible = True
print("Elapsed time is " + str(time.time() - startTime))
