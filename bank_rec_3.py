#on comparison sheet, could write only the necessary columns

print("Cmt: Importing modules...")

import time, win32com.client, os, sys

startTime = time.time()
print("Cmt: Importing modules...Done.")
print("Cmt: Open and connect to file...")


excelApp = win32com.client.gencache.EnsureDispatch('Excel.Application')
excelApp.Visible = True
excelApp.DisplayAlerts = False
filePath = os.path.abspath(os.curdir)
fileName = "Bank Rec"
fileExtension = ".xlsx"


excelApp.Workbooks.Open(filePath + "\\" + fileName + fileExtension)
excelApp.Calculation = win32com.client.constants.xlCalculationManual
excelBackupWb = excelApp.Workbooks(fileName + fileExtension)
excelBackupWb.SaveAs(Filename=filePath + "\\" + fileName + " Before Running 3" + fileExtension, FileFormat=51)
excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelBackupWb.Close()


excelApp.Workbooks.Open(filePath + "\\" + fileName + fileExtension)
excelApp.Calculation = win32com.client.constants.xlCalculationManual
excelWb = excelApp.Workbooks(fileName  + fileExtension)

excelGPTableSheet = excelWb.Worksheets("GP Table")
excelBankTableSearchSheet = excelWb.Worksheets("Bank Table Search")
excelCompSheet = excelWb.Worksheets("Comparison")
excelCompSheet.UsedRange.Clear()


rowAfterHeader = 2
bankColumns = 8
bankTableSearchCol = 8
gpColumns = 17
gpSearchValueCol = 6



print("Cmt: Open and connect to file...Done.")


excelBankTableSearchSheet.Range(excelBankTableSearchSheet.Cells(1, 1), excelBankTableSearchSheet.Cells(1, bankColumns)).Copy(excelCompSheet.Cells(1, 1))
excelGPTableSheet.Range(excelGPTableSheet.Cells(1, 1), excelGPTableSheet.Cells(1, gpColumns)).Copy(excelCompSheet.Cells(1, bankColumns + 1))

gpRow = rowAfterHeader


while excelGPTableSheet.Cells(gpRow, 1).Value:

    #put in GP data
    
    excelGPTableSheet.Range(excelGPTableSheet.Cells(gpRow, 1), excelGPTableSheet.Cells(gpRow, gpColumns)).Copy(excelCompSheet.Cells(gpRow, bankColumns + 1))

    #check bank data

    rowsToCheck = []

    startingSearchRow = 2
    endingSearchRow = excelBankTableSearchSheet.Cells(2, bankTableSearchCol).End(win32com.client.constants.xlDown).Row
    searchText = excelGPTableSheet.Cells(gpRow, gpSearchValueCol).Value

    while startingSearchRow <= excelBankTableSearchSheet.Cells(rowAfterHeader, bankTableSearchCol).End(win32com.client.constants.xlDown).Row:
        
        foundRange = excelBankTableSearchSheet.Range(excelBankTableSearchSheet.Cells(startingSearchRow, bankTableSearchCol), excelBankTableSearchSheet.Cells(startingSearchRow, bankTableSearchCol).End(win32com.client.constants.xlDown)).Find(What=searchText, LookAt=win32com.client.constants.xlWhole) 

        if foundRange:         
            rowsToCheck.append(foundRange.Row)
            startingSearchRow = foundRange.Row + 1
        else:
            break

            
    if len(rowsToCheck) == 1:
            excelBankTableSearchSheet.Range(excelBankTableSearchSheet.Cells(rowsToCheck[0], 1), excelBankTableSearchSheet.Cells(rowsToCheck[0], bankColumns)).Copy(excelCompSheet.Cells(gpRow, 1))
            excelBankTableSearchSheet.Cells(rowsToCheck[0], 1).EntireRow.Delete()
 
    gpRow = gpRow + 1



excelCompSheet.Cells.EntireColumn.AutoFit()
excelApp.DisplayAlerts = True
excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelWb.Save()
excelApp.Visible = True
print("Elapsed time is " + str(time.time() - startTime))
