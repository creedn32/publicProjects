
print("Cmt: Importing modules...")

import time, win32com.client, os, sys

startTime = time.time()
print("Cmt: Importing modules...Done.")
print("Cmt: Open and connect to file...")

def emptyStr(s):
    if s:
        return str(s)
    else:
        return ""

excelApp = win32com.client.gencache.EnsureDispatch('Excel.Application')
#excelApp.Interactive = False
excelApp.Visible = False
excelApp.DisplayAlerts = False
filePath = os.path.abspath(os.curdir)
fileName = "Bank Rec"
fileExtension = ".xlsx"


excelApp.Workbooks.Open(filePath + "\\" + fileName + fileExtension)
excelApp.Calculation = win32com.client.constants.xlCalculationManual
excelBackupWb = excelApp.Workbooks(fileName + fileExtension)
excelBackupWb.SaveAs(Filename=filePath + "\\" + fileName + " Before Running 1" + fileExtension, FileFormat=51)
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
excelBankTableSheet.Range(excelBankTableSheet.Cells(2, 14), excelBankTableSheet.Cells(2, 14).End(win32com.client.constants.xlDown)).Copy(excelBankTableSearchSheet.Cells(2, 2))

excelBankTableSearchSheet.Cells.EntireColumn.AutoFit()

#excelApp.Interactive = True
excelApp.DisplayAlerts = True
excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelWb.Save()
excelApp.Visible = True
print("Elapsed time is " + str(time.time() - startTime))




