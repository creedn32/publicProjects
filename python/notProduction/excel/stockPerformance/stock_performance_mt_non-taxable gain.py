print("Cmt: Importing modules...")

import time, win32com.client, os, re

print("Cmt: Importing modules...Done.")
print("Cmt: Open and connect to file...")

excelApp = win32com.client.gencache.EnsureDispatch('Excel.Application')
excelApp.Visible = True
excelApp.DisplayAlerts = True
filePath = os.path.abspath(os.curdir)
fileName = "Stock_Performance"
fileExtension = ".xlsx"

excelApp.Workbooks.Open(filePath + "\\" + fileName + fileExtension)
excelApp.Calculation = win32com.client.constants.xlCalculationManual
excelWb = excelApp.Workbooks(fileName + fileExtension)
excelTransactionsSheet = excelWb.Worksheets("Transactions")

transRow = 1
sumRow = 1
currentStockBrokerLotDate = ""

while excelTransactionsSheet.Cells(transRow, 1).Value:

    if excelTransactionsSheet.Cells(transRow, 1).Value == "Sell Stock" and excelTransactionsSheet.Cells(transRow, 3).Value == "Mt":
        if str(excelTransactionsSheet.Cells(transRow, 2).Value) + str(excelTransactionsSheet.Cells(transRow, 3).Value) + str(excelTransactionsSheet.Cells(transRow, 4).Value) + str(excelTransactionsSheet.Cells(transRow, 6).Value) != currentStockBrokerLotDate:
            currentStockBrokerLotDate = str(excelTransactionsSheet.Cells(transRow, 2).Value) + str(excelTransactionsSheet.Cells(transRow, 3).Value) + str(excelTransactionsSheet.Cells(transRow, 4).Value) + str(excelTransactionsSheet.Cells(transRow, 6).Value)

            sumRow = transRow
            currentSum = 0
            
            while str(excelTransactionsSheet.Cells(sumRow, 2).Value) + str(excelTransactionsSheet.Cells(sumRow, 3).Value) + str(excelTransactionsSheet.Cells(sumRow, 4).Value) + str(excelTransactionsSheet.Cells(sumRow, 6).Value) == currentStockBrokerLotDate and excelTransactionsSheet.Cells(transRow, 1).Value == "Sell Stock":

                if excelTransactionsSheet.Cells(sumRow, 7).Value == "Sale Fee Expense" or excelTransactionsSheet.Cells(sumRow, 7).Value == "Regulatory Fee Expense" :
                    currentSum = currentSum + excelTransactionsSheet.Cells(sumRow, 8).Value
                
                sumRow = sumRow + 1

            currentSum = round(currentSum, 2)
            
            if currentSum > 0:
                
                print("Gain On Sale (Excluded From Tax): " + str(currentSum))

                checkRow = transRow
            
                while str(excelTransactionsSheet.Cells(checkRow, 2).Value) + str(excelTransactionsSheet.Cells(checkRow, 3).Value) + str(excelTransactionsSheet.Cells(checkRow, 4).Value) + str(excelTransactionsSheet.Cells(checkRow, 6).Value) == currentStockBrokerLotDate and excelTransactionsSheet.Cells(checkRow, 1).Value == "Sell Stock":

                    if "Gain On Sale" in excelTransactionsSheet.Cells(checkRow, 7).Value or "Loss On Sale" in excelTransactionsSheet.Cells(checkRow, 7).Value: 
                        excelTransactionsSheet.Cells(checkRow, 8).Value = round(excelTransactionsSheet.Cells(checkRow, 8).Value, 2) + currentSum #+ (-currentSum)

                        excelTransactionsSheet.Cells(checkRow, 1).EntireRow.Insert()
                        
                        for i in range(1, 7):
                            excelTransactionsSheet.Cells(checkRow, i).Value = excelTransactionsSheet.Cells(checkRow - 1, i).Value

                        excelTransactionsSheet.Cells(checkRow, 7).Value = "Gain On Sale (Excluded From Tax)" #excelTransactionsSheet.Cells(checkRow, 7).Value # 
                        excelTransactionsSheet.Cells(checkRow, 8).Value = -currentSum #excelTransactionsSheet.Cells(checkRow, 8).Value # 
                        
                        break
                
                    checkRow = checkRow + 1
 
    transRow = transRow + 1


excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelWb.Save()
