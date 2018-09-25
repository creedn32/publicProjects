#on comparison sheet, could write only the necessary columns

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



print("Cmt: Open and connect to file...Done.")


excelBankTableSearchSheet.Range(excelBankTableSearchSheet.Cells(1, 1), excelBankTableSearchSheet.Cells(1, 13)).Copy(excelCompSheet.Cells(1, 1))
excelGPTableSheet.Range(excelGPTableSheet.Cells(1, 1), excelGPTableSheet.Cells(1, 17)).Copy(excelCompSheet.Cells(1, 14))

gpRow = 2


while excelGPTableSheet.Cells(gpRow, 1).Value:
    lapStartTime = time.time()

    #put in GP data
    
    excelGPTableSheet.Range(excelGPTableSheet.Cells(gpRow, 1), excelGPTableSheet.Cells(gpRow, 17)).Copy(excelCompSheet.Cells(gpRow, 14))

    #check bank data

    rowsToCheck = []

    startingSearchRow = 2
    endingSearchRow = excelBankTableSearchSheet.Cells(2, 10).End(win32com.client.constants.xlDown).Row
    searchText = excelGPTableSheet.Cells(gpRow, 6).Value

    while startingSearchRow <= excelBankTableSearchSheet.Cells(2, 10).End(win32com.client.constants.xlDown).Row:
        
        foundRange = excelBankTableSearchSheet.Range(excelBankTableSearchSheet.Cells(startingSearchRow, 10), excelBankTableSearchSheet.Cells(startingSearchRow, 10).End(win32com.client.constants.xlDown)).Find(What=searchText, LookAt=win32com.client.constants.xlWhole) 

        if foundRange:

            if excelGPTableSheet.Cells(gpRow, 12).Value == "Check" and excelBankTableSearchSheet.Cells(foundRange.Row, 8).Value == "Check(s) Paid":
                
                if int(excelGPTableSheet.Cells(gpRow, 13).Value[-5:]) == excelBankTableSearchSheet.Cells(foundRange.Row, 12).Value and len(excelGPTableSheet.Cells(gpRow, 13).Value) in (5, 6, 7):

                    startingSearchRow = foundRange.Row
                    endingSearchRow = excelBankTableSearchSheet.Cells(2, 10).End(win32com.client.constants.xlDown).Row
                    excelBankTableSearchSheet.Range(excelBankTableSearchSheet.Cells(foundRange.Row, 1), excelBankTableSearchSheet.Cells(foundRange.Row, 13)).Copy(excelCompSheet.Cells(gpRow, 1))
                    excelBankTableSearchSheet.Cells(foundRange.Row, 1).EntireRow.Delete()
                    break
                
    
            rowsToCheck.append(foundRange.Row)
            startingSearchRow = foundRange.Row + 1
        else:
            break

            
    if len(rowsToCheck) == 1:
        if excelGPTableSheet.Cells(gpRow, 12).Value != "Check" or (excelGPTableSheet.Cells(gpRow, 12).Value == "Check" and (len(excelGPTableSheet.Cells(gpRow, 13).Value) not in (5, 6, 7) or excelGPTableSheet.Cells(gpRow, 13).Value[:3] == "ACH")):
            excelBankTableSearchSheet.Range(excelBankTableSearchSheet.Cells(rowsToCheck[0], 1), excelBankTableSearchSheet.Cells(rowsToCheck[0], 13)).Copy(excelCompSheet.Cells(gpRow, 1))
            excelBankTableSearchSheet.Cells(rowsToCheck[0], 1).EntireRow.Delete()
    elif len(rowsToCheck) > 1:
        if excelGPTableSheet.Cells(gpRow, 12).Value == "Check" and len(excelGPTableSheet.Cells(gpRow, 13).Value) in (5, 6, 7):
            for rowToCheck in rowsToCheck:
               if excelBankTableSearchSheet.Cells(rowToCheck, 8).Value == "Check(s) Paid":
                    if int(excelGPTableSheet.Cells(gpRow, 13).Value[-5:]) == excelBankTableSearchSheet.Cells(rowToCheck, 12).Value:
                        excelBankTableSearchSheet.Range(excelBankTableSearchSheet.Cells(rowToCheck, 1), excelBankTableSearchSheet.Cells(rowToCheck, 13)).Copy(excelCompSheet.Cells(gpRow, 1))
                        excelBankTableSearchSheet.Cells(rowToCheck, 1).EntireRow.Delete()

    #print(str(time.time() - lapStartTime)[0:5])
    gpRow = gpRow + 1



excelCompSheet.Cells.EntireColumn.AutoFit()
excelApp.DisplayAlerts = True
excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelWb.Save()
excelApp.Visible = True
print("Elapsed time is " + str(time.time() - startTime))
