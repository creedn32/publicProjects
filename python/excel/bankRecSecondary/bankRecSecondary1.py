#deal with "In Progress" transactions

#local application imports
from pathlib import Path
import sys
pathToThisPythonFile = Path(__file__).resolve()
sys.path.append(str(pathToThisPythonFile.parents[3]))
import herokuGorilla.backend.python.myPythonLibrary._myPyFunc as _myPyFunc


startTime = _myPyFunc.printElapsedTime(False, "Starting code")
from pprint import pprint as pp
from decimal import *


import win32com.client

excelApp = win32com.client.gencache.EnsureDispatch('Excel.Application')
excelApp.Visible = False
excelApp.DisplayAlerts = False

# pp("Manual printout: " + str(Path.cwd().parents[3]) + "\\privateData\\python\\excel\\bankRecSecondary")
filePath = _myPyFunc.replacePartOfPath(pathToThisPythonFile.parents[0], 'publicProjects', 'privateData')
fileName = "Bank Rec"
fileExtension = ".xlsx"


excelApp.Workbooks.Open(Path(filePath, fileName + fileExtension))
excelApp.Calculation = win32com.client.constants.xlCalculationManual
excelBackupWb = excelApp.Workbooks(fileName + fileExtension)
excelBackupWb.SaveAs(Filename=str(Path(filePath, fileName + " Before Running 1" + fileExtension)), FileFormat=51)
excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelBackupWb.Close()


excelApp.Workbooks.Open(Path(filePath, fileName + fileExtension))
excelApp.Calculation = win32com.client.constants.xlCalculationManual
excelWb = excelApp.Workbooks(fileName + fileExtension)


excelBankSheet = excelWb.Worksheets("Bank Data")
excelGPSheet = excelWb.Worksheets("GP Data")
excelBankTableSheet = excelWb.Worksheets("Bank Table")
excelGPTableSheet = excelWb.Worksheets("GP Table")
maxRows = 7000
excelBankTableSheet.UsedRange.Clear()
excelGPTableSheet.UsedRange.Clear()

rowAfterHeader = 2
bankColumns = 7
gpNameCol = 15
gpTransferCol = 17
gpAmountCol = 6
gpTrxTypeCol = 12


splitTime = _myPyFunc.printElapsedTime(startTime, "Finished importing modules and intializing variables")

excelBankTableSheet.Cells(1, bankColumns + 1).Value = "B Amount"

for col in range(1, bankColumns + 1):
    excelBankTableSheet.Cells(1, col).Value = "B " + excelBankSheet.Cells(1, col).Value


firstCell = excelBankSheet.Cells(rowAfterHeader, 1)
excelBankSheet.Range(firstCell, excelBankSheet.Cells(firstCell.CurrentRegion.Rows.Count, firstCell.CurrentRegion.Columns.Count)).Copy(excelBankTableSheet.Cells(rowAfterHeader, 1))



bankTableSheetRow = rowAfterHeader

while excelBankTableSheet.Cells(bankTableSheetRow, 1).Value:


    paymentAmount = _myPyFunc.convertToZero(excelBankTableSheet.Cells(bankTableSheetRow, 6).Value)
    depositAmount =_myPyFunc.convertToZero(excelBankTableSheet.Cells(bankTableSheetRow, 7).Value)

    excelBankTableSheet.Cells(bankTableSheetRow, bankColumns + 1).Value = float(depositAmount - paymentAmount)
    bankTableSheetRow = bankTableSheetRow + 1



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
_myPyFunc.printElapsedTime(startTime, "Total time to run code")



