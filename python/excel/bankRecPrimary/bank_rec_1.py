print("Cmt: Importing modules...")

import sys, pathlib
from pprint import pprint as pp

# pp(sys.path)
# pp(str(pathlib.Path.cwd().parents[0]))
sys.path.append(str(pathlib.Path.cwd().parents[1]))
from myPythonLibrary import myPythonFunctions

import time, win32com.client

startTime = time.time()
print("Cmt: Importing modules...Done.")
print("Cmt: Open and connect to file...")

excelApp = win32com.client.gencache.EnsureDispatch('Excel.Application')
excelApp.Visible = False
excelApp.DisplayAlerts = False
filePath = str(pathlib.Path.cwd().parents[3]) + "\\privateData\\bankRecPrimary"
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
#maxRows = 7000
excelBankTableSheet.UsedRange.Clear()
excelGPTableSheet.UsedRange.Clear()

rowAfterHeader = 2
bankTypeCol = 8
bankDateCol = 14
bankOrigDateCol = 2
bankDescCol = 13
bankAmountCol = 10
bankColumns = 13
gpNameCol = 15
gpTransferCol = 17
gpAmountCol = 6
gpTrxTypeCol = 12

print("Cmt: Open and connect to file...Done.")

excelBankTableSheet.Cells(1, bankColumns + 1).Value = "B Date C"

for col in range(1, bankColumns + 1):
    excelBankTableSheet.Cells(1, col).Value = "B " + excelBankSheet.Cells(1, col).Value


firstCell = excelBankSheet.Cells(rowAfterHeader, 1)
excelBankSheet.Range(firstCell, excelBankSheet.Cells(firstCell.CurrentRegion.Rows.Count, firstCell.CurrentRegion.Columns.Count)).Copy(excelBankTableSheet.Cells(rowAfterHeader, 1))


bankTableSheetRow = rowAfterHeader

while excelBankTableSheet.Cells(bankTableSheetRow, 1).Value:

    if excelBankTableSheet.Cells(bankTableSheetRow, bankTypeCol).Value in ["Data", "Ledger Balance", "Collected + 1 Day", "Opening Collected", "One Day Float", "2 Day Float", "3 Day + Float", "MTD Avg Collected", "MTD Avg Neg Collected", "Total Credits", "Number of Credits", "Total Debits", "Number of Debits", "Float Adjustment(s)"] or excelBankTableSheet.Cells(bankTableSheetRow, 1).Value in ["H", "B", "T"]:
       excelBankTableSheet.Rows(bankTableSheetRow).EntireRow.Delete()
       bankTableSheetRow = bankTableSheetRow - 1
    else:
        excelBankTableSheet.Cells(bankTableSheetRow, bankDateCol).Value = myPythonFunctions.convertNothingToEmptyStr(excelBankTableSheet.Cells(bankTableSheetRow, bankOrigDateCol).Value)[:-8] + "/" + myPythonFunctions.convertNothingToEmptyStr(excelBankTableSheet.Cells(bankTableSheetRow, bankOrigDateCol).Value)[:-6][-2:] + "/" + myPythonFunctions.convertNothingToEmptyStr(excelBankTableSheet.Cells(bankTableSheetRow, bankOrigDateCol).Value)[:-2][-4:]

        myStr = myPythonFunctions.convertNothingToEmptyStr(excelBankTableSheet.Cells(bankTableSheetRow, bankDescCol).Value).replace("\n", " ")
        myStr = " ".join(myStr.split())[0:200]
        excelBankTableSheet.Cells(bankTableSheetRow, bankDescCol).Value = myStr

        if excelBankTableSheet.Cells(bankTableSheetRow, 9).Value == "Debit":
            excelBankTableSheet.Cells(bankTableSheetRow, bankAmountCol).Value = -float(excelBankTableSheet.Cells(bankTableSheetRow, bankAmountCol).Value)



    bankTableSheetRow = bankTableSheetRow + 1



    #if bankTableSheetRow == maxRows:
    #    break



excelGPTableSheet.Cells(1, gpTransferCol).Value = "G Transfer"
for col in range(1, gpTransferCol):
    excelGPTableSheet.Cells(1, col).Value = "G " + excelGPSheet.Cells(1, col).Value



firstCell = excelGPSheet.Cells(rowAfterHeader, 1)
excelGPSheet.Range(firstCell, excelGPSheet.Cells(firstCell.CurrentRegion.Rows.Count, firstCell.CurrentRegion.Columns.Count)).Copy(excelGPTableSheet.Cells(rowAfterHeader, 1))



gpTableSheetRow = rowAfterHeader

while excelGPTableSheet.Cells(gpTableSheetRow, 1).Value:

    if excelGPTableSheet.Cells(gpTableSheetRow, gpNameCol).Value:
        if excelGPTableSheet.Cells(gpTableSheetRow, gpNameCol).Value[0:11] == "Transfer To":
            excelGPTableSheet.Cells(gpTableSheetRow, gpTransferCol).Value = "Out"
        elif excelGPTableSheet.Cells(gpTableSheetRow, gpNameCol).Value[0:13] == "Transfer From":
           excelGPTableSheet.Cells(gpTableSheetRow, gpTransferCol).Value = "In"

    if excelGPTableSheet.Cells(gpTableSheetRow, gpTrxTypeCol).Value:
        if not excelGPTableSheet.Cells(gpTableSheetRow, gpTransferCol).Value:
            if excelGPTableSheet.Cells(gpTableSheetRow, gpTrxTypeCol).Value in ["Increase Adjustment", "Deposit"]:
                excelGPTableSheet.Cells(gpTableSheetRow, gpTransferCol).Value = "In"
            if excelGPTableSheet.Cells(gpTableSheetRow, gpTrxTypeCol).Value in ["Decrease Adjustment", "Withdrawl", "Check"]:
                excelGPTableSheet.Cells(gpTableSheetRow, gpTransferCol).Value = "Out"

    if excelGPTableSheet.Cells(gpTableSheetRow, gpTransferCol).Value == "Out" and excelGPTableSheet.Cells(gpTableSheetRow, gpAmountCol).Value:
        excelGPTableSheet.Cells(gpTableSheetRow, gpAmountCol).Value = -float(excelGPTableSheet.Cells(gpTableSheetRow, gpAmountCol).Value)

    #if gpTableSheetRow == maxRows:
    #    break

    #print(gpTableSheetRow)

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
