print("Cmt: Importing modules...")

import time, win32com.client #inspect, xlwings, pywinauto, pyautogui, win32api, os, inspect

#print("execfile(\"" + inspect.getfile(inspect.currentframe()).encode('string-escape') + "\")")
print("Cmt: Importing modules...Done.")
print("Cmt: Open and connect to file...")

def emptyStr(s):
    if s:
        return str(s)
    else:
        return ""

#pyautogui.PAUSE = .005
#pyautogui.FAILSAFE = True
excelApp = win32com.client.gencache.EnsureDispatch('Excel.Application')
filePath = ""
#filePath = ""
fileName = "Bank_Rec.xlsx"
excelApp.Workbooks.Open(filePath + fileName)
excelApp.Visible = True
excelWb = excelApp.Workbooks(fileName)

excelBankSheet = excelWb.Worksheets("")
excelGPSheet = excelWb.Worksheets("")
excelBankTableSheet = excelWb.Worksheets("Bank Table")
excelGPTableSheet = excelWb.Worksheets("GP Table")
excelCompSheet = excelWb.Worksheets("Comparison")


print("Cmt: Open and connect to file...Done.")

row = 1


if excelBankSheet.Cells(row, 1).Value != None:
    print("first")
if excelBankSheet.Cells(row, 1).Value:
    print("second")



while excelBankSheet.Cells(row, 1).Value:

    for col in range(2, 16):
        if row == 1:
            #idea to increase efficiency, could check which col it is on and only write B Key for col 1
            #idea to increase efficiency, could only write rows that won't be deleted later
            #change excelBankTableSheet.Cells(row, 1).Value != None: to excelBankTableSheet.Cells(row, 1).Value
            
            
            excelBankTableSheet.Cells(row, col).Value = "B " + emptyStr(excelBankSheet.Cells(row, col - 1).Value)[0:200]
            excelBankTableSheet.Cells(row, 1).Value = "B Key"
            excelBankTableSheet.Cells(row, 15).Value = "B Date C"
        else:
            excelBankTableSheet.Cells(row, 1).Value = row - 1
            
            
            if excelBankTableSheet.Cells(row, 10).Value == "Debit" and col == 11:
                excelBankTableSheet.Cells(row, col).Value = -float(excelBankSheet.Cells(row, col - 1).Value)
            else:
                excelBankTableSheet.Cells(row, col).Value = emptyStr(excelBankSheet.Cells(row, col - 1).Value)[0:200]

            excelBankTableSheet.Cells(row, 15).Value = emptyStr(excelBankSheet.Cells(row, 2).Value)[:-8] + "/" + emptyStr(excelBankSheet.Cells(row, 2).Value)[:-6][-2:] + "/" + emptyStr(excelBankSheet.Cells(row, 2).Value)[:-2][-4:]
           
        

    if row == 5:
        break
    
    row = row + 1




row = 1
rng = None

while excelBankTableSheet.Cells(row, 1).Value != None:

    if excelBankTableSheet.Cells(row, 9).Value in ["Data", "Ledger Balance", "Collected + 1 Day", "Opening Collected", "One Day Float", "2 Day Float", "3 Day + Float", "MTD Avg Collected", "MTD Avg Neg Collected", "Total Credits", "Number of Credits", "Total Debits", "Number of Debits", "Float Adjustment(s)"] or excelBankTableSheet.Cells(row, 2).Value in ["H", "B"]:
        if rng:
            rng = excelApp.Union(rng, excelBankTableSheet.Cells(row, 1).EntireRow)
        else:
            rng = excelBankTableSheet.Cells(row, 1).EntireRow
            
    
    row = row + 1


rng.Delete()
excelBankTableSheet.Cells.EntireColumn.AutoFit()

row = 1

while excelGPSheet.Cells(row, 1).Value != None:
    
    for col in range(2, 18):
        if row == 1:
            excelGPTableSheet.Cells(row, col).Value = "G " + emptyStr(excelGPSheet.Cells(row, col - 1).Value)[0:200]
            excelGPTableSheet.Cells(row, 1).Value = "G Key"
            excelGPTableSheet.Cells(row, 18).Value = "G Transfer"
        else:
            excelGPTableSheet.Cells(row, 1).Value = row - 1
            excelGPTableSheet.Cells(row, col).Value = emptyStr(excelGPSheet.Cells(row, col - 1).Value)[0:200]
    
    if excelGPTableSheet.Cells(row, 16).Cells.Value:
        if excelGPTableSheet.Cells(row, 16).Cells.Value[0:11] == "Transfer To":
            excelGPTableSheet.Cells(row, 18).Cells.Value = "Out"
        elif excelGPTableSheet.Cells(row, 16).Cells.Value[0:13] == "Transfer From":
           excelGPTableSheet.Cells(row, 18).Cells.Value = "In"

    if excelGPTableSheet.Cells(row, 13).Value:
        if not excelGPTableSheet.Cells(row, 18).Value:
            if excelGPTableSheet.Cells(row, 13).Value in ["Increase Adjustment", "Deposit"]:
                excelGPTableSheet.Cells(row, 18).Value = "In"
            if excelGPTableSheet.Cells(row, 13).Value in ["Decrease Adjustment", "Withdrawl", "Check"]:
                excelGPTableSheet.Cells(row, 18).Value = "Out"
    if excelGPTableSheet.Cells(row, 18).Value == "Out":
        excelGPTableSheet.Cells(row, 7).Value = -float(excelGPTableSheet.Cells(row, 7).Value)

    if row == 4:
        break


    row = row + 1
    
excelGPTableSheet.Cells.EntireColumn.AutoFit()


for col in range(1, 15):
    excelCompSheet.Cells(1, col).Value = excelBankTableSheet.Cells(1, col).Value
for col in range(1, 19):
    excelCompSheet.Cells(1, col + 14).Value = excelGPTableSheet.Cells(1, col).Value




row = 2

while excelGPTableSheet.Cells(row, 1).Value != None:

    #put in GP data
    
    for col in range(1, 19):
        excelCompSheet.Cells(row, col + 14).Value = excelGPTableSheet.Cells(row, col).Value

    #check bank data

    if excelGPTableSheet.Cells(row, 14).Value != None:


        bankRow = 2
        foundRows = []
        
        while excelBankTableSheet.Cells(bankRow, 1).Value != None:
            if excelBankTableSheet.Cells(bankRow, 13).Value != None:
                if excelGPTableSheet.Cells(row, 7).Value == excelBankTableSheet.Cells(bankRow, 11).Value and str(excelGPTableSheet.Cells(row, 14).Value)[:-2][-5:] == str(excelBankTableSheet.Cells(bankRow, 13).Value)[:-2][-5:]:
                    foundRows.append(bankRow)      
                       

                    
            bankRow = bankRow + 1


        if len(foundRows) != 1:
            if excelGPTableSheet.Cells(row, 13).Value != "Check" or (excelGPTableSheet.Cells(row, 13).Value == "Check" and "ACH" in str(excelGPTableSheet.Cells(row, 14).Value)) or (excelGPTableSheet.Cells(row, 13).Value == "Check" and len(str(excelGPTableSheet.Cells(row, 14).Value)[:-2]) == 5):
                secondBankRow = 2
                foundRows = []
        
                while excelBankTableSheet.Cells(secondBankRow, 1).Value != None:
                    if excelGPTableSheet.Cells(row, 7).Value == excelBankTableSheet.Cells(secondBankRow, 11).Value and excelBankTableSheet.Cells(secondBankRow, 9).Value == "Check(s) Paid":
                        foundRows.append(secondBankRow)

                    secondBankRow = secondBankRow + 1


        #for foundRow in foundRows:
        #    print(foundRow)
        

        if len(foundRows) == 1:
            for bankCol in range(1, 15):
                if bankCol == 3:
                    excelCompSheet.Cells(row, bankCol).Value = excelBankTableSheet.Cells(foundRows[0], 15).Value
                else:
                    excelCompSheet.Cells(row, bankCol).Value = excelBankTableSheet.Cells(foundRows[0], bankCol).Value

            excelBankTableSheet.Cells(foundRows[0], 1).EntireRow.Delete()
                    
    row = row + 1

excelCompSheet.Cells.EntireColumn.AutoFit()










