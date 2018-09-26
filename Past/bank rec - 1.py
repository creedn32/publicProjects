print("Cmt: Importing modules...")

import time, win32com.client #inspect, xlwings, pywinauto, pyautogui, win32api, os

start_time = time.time()
print("Cmt: Importing modules...Done.")
print("Cmt: Open and connect to file...")

def emptyStr(s):
    if s:
        return str(s)
    else:
        return ""

excelApp = win32com.client.gencache.EnsureDispatch('Excel.Application')
filePath = ""
#filePath = ""
fileName = "Bank_Rec.xlsx"
dataFileName = "Bank_Rec_Data.xlsx"

excelApp.Workbooks.Open(filePath + fileName)
excelApp.Workbooks.Open(filePath + dataFileName)
excelWb = excelApp.Workbooks(fileName)
excelDataWb = excelApp.Workbooks(dataFileName)

excelBankSheet = excelDataWb.Worksheets("")
excelGPSheet = excelDataWb.Worksheets("")
excelBankTableSheet = excelWb.Worksheets("Bank Table")
excelGPTableSheet = excelWb.Worksheets("GP Table")
maxRows = 7000
excelApp.Visible = True

print("Cmt: Open and connect to file...Done.")


excelBankTableSheet.Cells(1, 1).Value = "B Key"
excelBankTableSheet.Cells(1, 15).Value = "B Date C"

for col in range(2, 15):
    excelBankTableSheet.Cells(1, col).Value = "B " + emptyStr(excelBankSheet.Cells(1, col - 1).Value)[0:200]    


excelGPTableSheet.Cells(1, 1).Value = "G Key"
excelGPTableSheet.Cells(1, 18).Value = "G Transfer"
for col in range(2, 18):
    excelGPTableSheet.Cells(1, col).Value = "G " + emptyStr(excelGPSheet.Cells(1, col - 1).Value)[0:200]

    


bankTableSheetRow = 2
bankSheetRow = 2

while excelBankSheet.Cells(bankSheetRow, 1).Value:

    if excelBankSheet.Cells(bankSheetRow, 8).Value not in ["Data", "Ledger Balance", "Collected + 1 Day", "Opening Collected", "One Day Float", "2 Day Float", "3 Day + Float", "MTD Avg Collected", "MTD Avg Neg Collected", "Total Credits", "Number of Credits", "Total Debits", "Number of Debits", "Float Adjustment(s)"] and excelBankSheet.Cells(bankSheetRow, 1).Value not in ["H", "B", "T"]:
        excelBankTableSheet.Cells(bankTableSheetRow, 1).Value = bankTableSheetRow - 1
        excelBankTableSheet.Cells(bankTableSheetRow, 15).Value = emptyStr(excelBankSheet.Cells(bankSheetRow, 2).Value)[:-8] + "/" + emptyStr(excelBankSheet.Cells(bankSheetRow, 2).Value)[:-6][-2:] + "/" + emptyStr(excelBankSheet.Cells(bankSheetRow, 2).Value)[:-2][-4:]

        
        
        for col in range(2, 15):
                               
            if col == 11 and excelBankSheet.Cells(bankSheetRow, 9).Value == "Debit":
                excelBankTableSheet.Cells(bankTableSheetRow, 11).Value = -float(excelBankSheet.Cells(bankSheetRow, 10).Value)
            else:
                excelBankTableSheet.Cells(bankTableSheetRow, col).Value = emptyStr(excelBankSheet.Cells(bankSheetRow, col - 1).Value)[0:200]     

        bankTableSheetRow = bankTableSheetRow + 1

        

    if bankSheetRow == maxRows:
        break
    
    
    bankSheetRow = bankSheetRow + 1




row = 2

while excelGPSheet.Cells(row, 1).Value:

    excelGPTableSheet.Cells(row, 1).Value = row - 1
    
    for col in range(2, 18):
            excelGPTableSheet.Cells(row, col).Value = emptyStr(excelGPSheet.Cells(row, col - 1).Value)[0:200]

    
    if excelGPTableSheet.Cells(row, 16).Value:
        if excelGPTableSheet.Cells(row, 16).Value[0:11] == "Transfer To":
            excelGPTableSheet.Cells(row, 18).Value = "Out"
        elif excelGPTableSheet.Cells(row, 16).Value[0:13] == "Transfer From":
           excelGPTableSheet.Cells(row, 18).Value = "In"

    if excelGPTableSheet.Cells(row, 13).Value:
        if not excelGPTableSheet.Cells(row, 18).Value:
            if excelGPTableSheet.Cells(row, 13).Value in ["Increase Adjustment", "Deposit"]:
                excelGPTableSheet.Cells(row, 18).Value = "In"
            if excelGPTableSheet.Cells(row, 13).Value in ["Decrease Adjustment", "Withdrawl", "Check"]:
                excelGPTableSheet.Cells(row, 18).Value = "Out"
    if excelGPTableSheet.Cells(row, 18).Value == "Out" and excelGPTableSheet.Cells(row, 7).Value:
        excelGPTableSheet.Cells(row, 7).Value = -float(excelGPTableSheet.Cells(row, 7).Value)

    if row == maxRows:
        break

    row = row + 1



excelDataWb.Close()



excelBankTableSheet.Cells.EntireColumn.AutoFit()
excelGPTableSheet.Cells.EntireColumn.AutoFit()



print("Elapsed time is " + str(time.time() - start_time))



##row = 2
##rng = None
##
##
##while excelBankTableSheet.Cells(row, 1).Value:
##
##    if excelBankTableSheet.Cells(row, 9).Value in ["Data", "Ledger Balance", "Collected + 1 Day", "Opening Collected", "One Day Float", "2 Day Float", "3 Day + Float", "MTD Avg Collected", "MTD Avg Neg Collected", "Total Credits", "Number of Credits", "Total Debits", "Number of Debits", "Float Adjustment(s)"] or excelBankTableSheet.Cells(row, 2).Value in ["H", "B"]:
##        if rng:
##            rng = excelApp.Union(rng, excelBankTableSheet.Cells(row, 1).EntireRow)
##        else:
##            rng = excelBankTableSheet.Cells(row, 1).EntireRow
##            
##    
##    row = row + 1
##
##
##rng.Delete()









