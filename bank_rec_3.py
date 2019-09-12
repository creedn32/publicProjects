#on comparison sheet, could write only the necessary columns
#add feature counting if number of duplicate amounts matches duplicate amounts on bank statement
#Copy the comparison sheet into it's own workbook


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
bankColumns = 13
bankTrxTypeCol = 8
bankTrxNumCol = 12
bankTableSearchCol = 10
gpColumns = 17
gpSearchValueCol = 6
gpTrxTypeCol = 12
gpTrxNumCol = 13


print("Cmt: Open and connect to file...Done.")

#copy column names to Comparison

excelBankTableSearchSheet.Range(excelBankTableSearchSheet.Cells(1, 1), excelBankTableSearchSheet.Cells(1, bankColumns)).Copy(excelCompSheet.Cells(1, 1))
excelGPTableSheet.Range(excelGPTableSheet.Cells(1, 1), excelGPTableSheet.Cells(1, gpColumns)).Copy(excelCompSheet.Cells(1, bankColumns + 1))

gpRow = rowAfterHeader


while excelGPTableSheet.Cells(gpRow, 1).Value:
    #lapStartTime = time.time()

    #copy GP row to Comparison
    
    excelGPTableSheet.Range(excelGPTableSheet.Cells(gpRow, 1), excelGPTableSheet.Cells(gpRow, gpColumns)).Copy(excelCompSheet.Cells(gpRow, bankColumns + 1))

    #check bank data

    rowsToCheck = []

    startingSearchRow = rowAfterHeader
    endingSearchRow = excelBankTableSearchSheet.Cells(2, bankTableSearchCol).End(win32com.client.constants.xlDown).Row
    searchText = excelGPTableSheet.Cells(gpRow, gpSearchValueCol).Value



    while startingSearchRow <= excelBankTableSearchSheet.Cells(rowAfterHeader, bankTableSearchCol).End(win32com.client.constants.xlDown).Row:
        
        foundRange = excelBankTableSearchSheet.Range(excelBankTableSearchSheet.Cells(startingSearchRow, bankTableSearchCol), excelBankTableSearchSheet.Cells(startingSearchRow, bankTableSearchCol).End(win32com.client.constants.xlDown)).Find(What=searchText, LookAt=win32com.client.constants.xlWhole) 

            
        if foundRange:

            #if searchText == -19281.77:
            #    print("starting cell for search is " + str(excelBankTableSearchSheet.Cells(startingSearchRow, bankTableSearchCol).Address))
            #    print("ending cell for search is " + str(excelBankTableSearchSheet.Cells(startingSearchRow, bankTableSearchCol).End(win32com.client.constants.xlDown).Address))      
            #    print("foundRange.Row is " + str(foundRange.Row))
                

            if excelGPTableSheet.Cells(gpRow, gpTrxTypeCol).Value == "Check" and excelBankTableSearchSheet.Cells(foundRange.Row, bankTrxTypeCol).Value == "Check(s) Paid":

                if int(excelGPTableSheet.Cells(gpRow, gpTrxNumCol).Value[-5:]) == excelBankTableSearchSheet.Cells(foundRange.Row, bankTrxNumCol).Value and len(excelGPTableSheet.Cells(gpRow, gpTrxNumCol).Value) in (5, 6, 7):

                    startingSearchRow = foundRange.Row
                    endingSearchRow = excelBankTableSearchSheet.Cells(rowAfterHeader, bankTableSearchCol).End(win32com.client.constants.xlDown).Row
                    excelBankTableSearchSheet.Range(excelBankTableSearchSheet.Cells(foundRange.Row, 1), excelBankTableSearchSheet.Cells(foundRange.Row, bankColumns)).Copy(excelCompSheet.Cells(gpRow, 1))
                    excelBankTableSearchSheet.Cells(foundRange.Row, 1).EntireRow.Delete()
                    break
                
           
                
            rowsToCheck.append(foundRange.Row)
            startingSearchRow = foundRange.Row + 1
        else:
            break

            
    if len(rowsToCheck) == 1:

        if excelGPTableSheet.Cells(gpRow, gpTrxTypeCol).Value != "Check" or (excelGPTableSheet.Cells(gpRow, gpTrxTypeCol).Value == "Check" and (len(excelGPTableSheet.Cells(gpRow, gpTrxNumCol).Value) not in (5, 6, 7) or excelGPTableSheet.Cells(gpRow, 13).Value[:3] == "ACH")):

            # if searchText == 283.02:
            #     print("Value on row to check is " + str(excelBankTableSearchSheet.Cells(rowsToCheck[0], bankTableSearchCol).Value))

            excelBankTableSearchSheet.Range(excelBankTableSearchSheet.Cells(rowsToCheck[0], 1), excelBankTableSearchSheet.Cells(rowsToCheck[0], bankColumns)).Copy(excelCompSheet.Cells(gpRow, 1))
            excelBankTableSearchSheet.Cells(rowsToCheck[0], 1).EntireRow.Delete()
    elif len(rowsToCheck) > 1:
        if excelGPTableSheet.Cells(gpRow, gpTrxTypeCol).Value == "Check" and len(excelGPTableSheet.Cells(gpRow, gpTrxNumCol).Value) in (5, 6, 7):
            for rowToCheck in rowsToCheck:
               if excelBankTableSearchSheet.Cells(rowToCheck, bankTrxTypeCol).Value == "Check(s) Paid":

                    #review this logic

                    if int(excelGPTableSheet.Cells(gpRow, gpTrxNumCol).Value[-5:]) == excelBankTableSearchSheet.Cells(rowToCheck, bankTrxNumCol).Value:
                        excelBankTableSearchSheet.Range(excelBankTableSearchSheet.Cells(rowToCheck, 1), excelBankTableSearchSheet.Cells(rowToCheck, bankColumns)).Copy(excelCompSheet.Cells(gpRow, 1))
                        excelBankTableSearchSheet.Cells(rowToCheck, 1).EntireRow.Delete()

    #print(str(time.time() - lapStartTime)[0:5])
    gpRow = gpRow + 1



excelCompSheet.Cells.EntireColumn.AutoFit()
excelApp.DisplayAlerts = True
excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelWb.Save()
excelApp.Visible = True
print("Elapsed time is " + str(time.time() - startTime))
