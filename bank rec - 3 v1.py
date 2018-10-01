#on comparison sheet, could write only the necessary columns
#use find function instead of looping so much


print("Cmt: Importing modules...")

import time, win32com.client, os 

startTime = time.time()
print("Cmt: Importing modules...Done.")
print("Cmt: Open and connect to file...")

def emptyStr(s):
    if s:
        return str(s)
    else:
        return ""

excelApp = win32com.client.gencache.EnsureDispatch('Excel.Application')
excelApp.Visible = False
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

print("Cmt: Open and connect to file...Done.")


excelBankTableSearchSheet.Range(excelBankTableSearchSheet.Cells(1, 1), excelBankTableSearchSheet.Cells(1, 13)).Copy(excelCompSheet.Cells(1, 1))
excelGPTableSheet.Range(excelGPTableSheet.Cells(1, 1), excelGPTableSheet.Cells(1, 17)).Copy(excelCompSheet.Cells(1, 14))

gpRow = 2


while excelGPTableSheet.Cells(gpRow, 1).Value:
    lapStartTime = time.time()

    #put in GP data
    
    excelGPTableSheet.Range(excelGPTableSheet.Cells(gpRow, 1), excelGPTableSheet.Cells(gpRow, 17)).Copy(excelCompSheet.Cells(gpRow, 14))

    #check bank data


    if excelGPTableSheet.Cells(gpRow, 14).Value:

        rowsToCheck = []
        startingSearchRow = 2
        searchText = excelGPTableSheet.Cells(gpRow, 6).Value

        while startingSearchRow <= excelBankTableSearchSheet.Cells(2, 10).End(win32com.client.constants.xlDown).Row:
        
            foundRange = excelBankTableSearchSheet.Range(excelBankTableSearchSheet.Cells(startingSearchRow, 10), excelBankTableSearchSheet.Cells(startingSearchRow, 10).End(win32com.client.constants.xlDown)).Find(What=searchText, LookAt=win32com.client.constants.xlPart) 

            if foundRange:
                rowsToCheck.append(foundRange.Row)
                startingSearchRow = foundRange.Row + 1
                #print(str(searchText) + " was found on row " + str(rowsToCheck) + ".")
            else:
                #print(str(searchText) + " was not found.")
                break



        foundRows = []
        
        
        if len(rowsToCheck) > 0:

            #print(rowsToCheck)
            
            for rowToCheck in rowsToCheck:

                #print("row to check is " + str(rowToCheck))

                if excelBankTableSearchSheet.Cells(rowToCheck, 12).Value:
                    if str(excelGPTableSheet.Cells(gpRow, 13).Value)[:-2][-5:] == str(excelBankTableSearchSheet.Cells(rowToCheck, 12).Value)[:-2][-5:]:
                        foundRows.append(bankRow)
                  
            if len(foundRows) != 1:

                if excelGPTableSheet.Cells(gpRow, 12).Value != "Check" or (excelGPTableSheet.Cells(gpRow, 12).Value == "Check" and "ACH" in str(excelGPTableSheet.Cells(gpRow, 13).Value)) or (excelGPTableSheet.Cells(gpRow, 12).Value == "Check" and len(str(excelGPTableSheet.Cells(gpRow, 13).Value)[:-2]) != 5):

                    foundRows = []

                
                    for rowtoCheck in rowsToCheck:
                   
                        if excelBankTableSearchSheet.Cells(rowToCheck, 8).Value != "Check(s) Paid":
                            foundRows.append(rowToCheck)


            if len(foundRows) == 1:

                excelBankTableSearchSheet.Range(excelBankTableSearchSheet.Cells(foundRows[0], 1), excelBankTableSearchSheet.Cells(foundRows[0], 13)).Copy(excelCompSheet.Cells(gpRow, 1))
                excelBankTableSearchSheet.Cells(foundRows[0], 1).EntireRow.Delete()


    print(str(time.time() - lapStartTime)[0:5])
    gpRow = gpRow + 1



excelCompSheet.Cells.EntireColumn.AutoFit()
excelApp.DisplayAlerts = True
excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelWb.Save()
excelApp.Visible = True
print("Elapsed time is " + str(time.time() - startTime))




