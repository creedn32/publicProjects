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
excelBackupWb.SaveAs(Filename=filePath + "\\" + fileName + " Before Running 2" + fileExtension, FileFormat=51)
excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelBackupWb.Close()


excelApp.Workbooks.Open(filePath + "\\" + fileName + fileExtension)
excelApp.Calculation = win32com.client.constants.xlCalculationManual
excelWb = excelApp.Workbooks(fileName + fileExtension)


excelBankSheet = excelWb.Worksheets("Bank Data")
excelGPSheet = excelWb.Worksheets("GP Data")
excelBankTableSheet = excelWb.Worksheets("Bank Table")
excelGPTableSheet = excelWb.Worksheets("GP Table")
maxRows = 7000
excelBankTableSheet.UsedRange.Clear()
excelGPTableSheet.UsedRange.Clear()


print("Cmt: Open and connect to file...Done.")

excelBankTableSheet.Cells(1, 14).Value = "B Date C"

for col in range(1, 14):
    excelBankTableSheet.Cells(1, col).Value = "B " + excelBankSheet.Cells(1, col).Value 


firstCell = excelBankSheet.Cells(1, 1)
excelBankSheet.Range(firstCell, excelBankSheet.Cells(firstCell.CurrentRegion.Rows.Count, firstCell.CurrentRegion.Columns.Count)).Copy(excelBankTableSheet.Cells(1, 1))


bankTableSheetRow = 2

while excelBankTableSheet.Cells(bankTableSheetRow, 1).Value:

    if excelBankTableSheet.Cells(bankTableSheetRow, 8).Value in ["Data", "Ledger Balance", "Collected + 1 Day", "Opening Collected", "One Day Float", "2 Day Float", "3 Day + Float", "MTD Avg Collected", "MTD Avg Neg Collected", "Total Credits", "Number of Credits", "Total Debits", "Number of Debits", "Float Adjustment(s)"] or excelBankTableSheet.Cells(bankTableSheetRow, 1).Value in ["H", "B", "T"]:
       excelBankTableSheet.Rows(bankTableSheetRow).EntireRow.Delete()
       bankTableSheetRow = bankTableSheetRow - 1
    else:
        excelBankTableSheet.Cells(bankTableSheetRow, 14).Value = emptyStr(excelBankTableSheet.Cells(bankTableSheetRow, 2).Value)[:-8] + "/" + emptyStr(excelBankTableSheet.Cells(bankTableSheetRow, 2).Value)[:-6][-2:] + "/" + emptyStr(excelBankTableSheet.Cells(bankTableSheetRow, 2).Value)[:-2][-4:]

        myStr = emptyStr(excelBankTableSheet.Cells(bankTableSheetRow, 13).Value).replace("\n", " ")
        myStr = " ".join(myStr.split())[0:200]
        excelBankTableSheet.Cells(bankTableSheetRow, 13).Value = myStr
        
        if excelBankTableSheet.Cells(bankTableSheetRow, 9).Value == "Debit":
            excelBankTableSheet.Cells(bankTableSheetRow, 10).Value = -float(excelBankTableSheet.Cells(bankTableSheetRow, 10).Value)

    

    bankTableSheetRow = bankTableSheetRow + 1

        

    if bankTableSheetRow == maxRows:
        break
    


excelGPTableSheet.Cells(1, 17).Value = "G Transfer"
for col in range(1, 17):
    excelGPTableSheet.Cells(1, col).Value = "G " + excelGPSheet.Cells(1, col).Value



firstCell = excelGPSheet.Cells(1, 1)
excelGPSheet.Range(firstCell, excelGPSheet.Cells(firstCell.CurrentRegion.Rows.Count, firstCell.CurrentRegion.Columns.Count)).Copy(excelGPTableSheet.Cells(1, 1))



gpTableSheetRow = 2

while excelGPTableSheet.Cells(gpTableSheetRow, 1).Value:
    
    if excelGPTableSheet.Cells(gpTableSheetRow, 15).Value:
        if excelGPTableSheet.Cells(gpTableSheetRow, 15).Value[0:11] == "Transfer To":
            excelGPTableSheet.Cells(gpTableSheetRow, 17).Value = "Out"
        elif excelGPTableSheet.Cells(gpTableSheetRow, 15).Value[0:13] == "Transfer From":
           excelGPTableSheet.Cells(gpTableSheetRow, 17).Value = "In"

    if excelGPTableSheet.Cells(gpTableSheetRow, 12).Value:
        if not excelGPTableSheet.Cells(gpTableSheetRow, 17).Value:
            if excelGPTableSheet.Cells(gpTableSheetRow, 12).Value in ["Increase Adjustment", "Deposit"]:
                excelGPTableSheet.Cells(gpTableSheetRow, 17).Value = "In"
            if excelGPTableSheet.Cells(gpTableSheetRow, 12).Value in ["Decrease Adjustment", "Withdrawl", "Check"]:
                excelGPTableSheet.Cells(gpTableSheetRow, 17).Value = "Out"

    if excelGPTableSheet.Cells(gpTableSheetRow, 17).Value == "Out" and excelGPTableSheet.Cells(gpTableSheetRow, 6).Value:
        excelGPTableSheet.Cells(gpTableSheetRow, 6).Value = -float(excelGPTableSheet.Cells(gpTableSheetRow, 6).Value)

    if gpTableSheetRow == maxRows:
        break

    gpTableSheetRow = gpTableSheetRow + 1



excelBankSheet.Cells.EntireColumn.AutoFit()

excelGPSheet.Cells.EntireColumn.AutoFit()

excelBankTableSheet.Cells.EntireColumn.AutoFit()
excelBankTableSheet.Cells.EntireRow.AutoFit()

excelGPTableSheet.Cells.EntireColumn.AutoFit()

excelApp.DisplayAlerts = True
excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelWb.Save()
excelApp.Visible = True
print("Elapsed time is " + str(time.time() - startTime))









