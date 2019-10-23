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
excelFromMotifSheet = excelWb.Worksheets("From Motif")

transRow = 1769
doubleEntryRow = 1769

while excelFromMotifSheet.Cells(transRow, 1).Value:

    excelFromMotifSheet.Cells(doubleEntryRow, 11).Value = "Sell Stock"
    excelFromMotifSheet.Cells(doubleEntryRow, 12).Value = excelFromMotifSheet.Cells(transRow, 1).Value
    excelFromMotifSheet.Cells(doubleEntryRow, 13).Value = "Mt"
    excelFromMotifSheet.Cells(doubleEntryRow, 14).Value = "52815"
    excelFromMotifSheet.Cells(doubleEntryRow, 15).Value = ""
    excelFromMotifSheet.Cells(doubleEntryRow, 16).Value = "3/16/2018"
    excelFromMotifSheet.Cells(doubleEntryRow, 17).Value = "Cash - Mt"
    excelFromMotifSheet.Cells(doubleEntryRow, 18).Value = excelFromMotifSheet.Cells(transRow, 2).Value

    doubleEntryRow = doubleEntryRow + 1

    excelFromMotifSheet.Cells(doubleEntryRow, 11).Value = "Sell Stock"
    excelFromMotifSheet.Cells(doubleEntryRow, 12).Value = excelFromMotifSheet.Cells(transRow, 1).Value
    excelFromMotifSheet.Cells(doubleEntryRow, 13).Value = "Mt"
    excelFromMotifSheet.Cells(doubleEntryRow, 14).Value = "52815"
    excelFromMotifSheet.Cells(doubleEntryRow, 15).Value = ""
    excelFromMotifSheet.Cells(doubleEntryRow, 16).Value = "3/16/2018"
    excelFromMotifSheet.Cells(doubleEntryRow, 17).Value = "Sale Fee Expense"
    excelFromMotifSheet.Cells(doubleEntryRow, 18).Value = excelFromMotifSheet.Cells(transRow, 3).Value

    doubleEntryRow = doubleEntryRow + 1


    excelFromMotifSheet.Cells(doubleEntryRow, 11).Value = "Sell Stock"
    excelFromMotifSheet.Cells(doubleEntryRow, 12).Value = excelFromMotifSheet.Cells(transRow, 1).Value
    excelFromMotifSheet.Cells(doubleEntryRow, 13).Value = "Mt"
    excelFromMotifSheet.Cells(doubleEntryRow, 14).Value = "52815"
    excelFromMotifSheet.Cells(doubleEntryRow, 15).Value = ""
    excelFromMotifSheet.Cells(doubleEntryRow, 16).Value = "3/16/2018"
    excelFromMotifSheet.Cells(doubleEntryRow, 17).Value = "Regulatory Fee Expense"
    excelFromMotifSheet.Cells(doubleEntryRow, 18).Value = excelFromMotifSheet.Cells(transRow, 4).Value

    doubleEntryRow = doubleEntryRow + 1


    excelFromMotifSheet.Cells(doubleEntryRow, 11).Value = "Sell Stock"
    excelFromMotifSheet.Cells(doubleEntryRow, 12).Value = excelFromMotifSheet.Cells(transRow, 1).Value
    excelFromMotifSheet.Cells(doubleEntryRow, 13).Value = "Mt"
    excelFromMotifSheet.Cells(doubleEntryRow, 14).Value = "52815"
    excelFromMotifSheet.Cells(doubleEntryRow, 15).Value = ""
    excelFromMotifSheet.Cells(doubleEntryRow, 16).Value = "3/16/2018"
    excelFromMotifSheet.Cells(doubleEntryRow, 17).Value = excelFromMotifSheet.Cells(transRow, 1).Value + " - Investment Asset - Mt - 52815"
    excelFromMotifSheet.Cells(doubleEntryRow, 18).Value = excelFromMotifSheet.Cells(transRow, 5).Value

    doubleEntryRow = doubleEntryRow + 1


    excelFromMotifSheet.Cells(doubleEntryRow, 11).Value = "Sell Stock"
    excelFromMotifSheet.Cells(doubleEntryRow, 12).Value = excelFromMotifSheet.Cells(transRow, 1).Value
    excelFromMotifSheet.Cells(doubleEntryRow, 13).Value = "Mt"
    excelFromMotifSheet.Cells(doubleEntryRow, 14).Value = "52815"
    excelFromMotifSheet.Cells(doubleEntryRow, 15).Value = ""
    excelFromMotifSheet.Cells(doubleEntryRow, 16).Value = "3/16/2018"
    excelFromMotifSheet.Cells(doubleEntryRow, 17).Value = excelFromMotifSheet.Cells(transRow, 1).Value + " - Purchase Fee Asset - Mt - 52815"
    excelFromMotifSheet.Cells(doubleEntryRow, 18).Value = excelFromMotifSheet.Cells(transRow, 6).Value

    doubleEntryRow = doubleEntryRow + 1


    excelFromMotifSheet.Cells(doubleEntryRow, 11).Value = "Sell Stock"
    excelFromMotifSheet.Cells(doubleEntryRow, 12).Value = excelFromMotifSheet.Cells(transRow, 1).Value
    excelFromMotifSheet.Cells(doubleEntryRow, 13).Value = "Mt"
    excelFromMotifSheet.Cells(doubleEntryRow, 14).Value = "52815"
    excelFromMotifSheet.Cells(doubleEntryRow, 15).Value = ""
    excelFromMotifSheet.Cells(doubleEntryRow, 16).Value = "3/16/2018"
    
    sumTotal = 0
    
    for i in range(1, 6):
        if excelFromMotifSheet.Cells(doubleEntryRow - i, 18).Value != None:
            sumTotal = sumTotal + excelFromMotifSheet.Cells(doubleEntryRow - i, 18).Value
        #print(excelFromMotifSheet.Cells(doubleEntryRow - i, 18).Value)
        
    excelFromMotifSheet.Cells(doubleEntryRow, 18).Value = -sumTotal


    if excelFromMotifSheet.Cells(doubleEntryRow, 18).Value < 0:
        excelFromMotifSheet.Cells(doubleEntryRow, 17 ).Value= "Gain On Sale"
    else:
        excelFromMotifSheet.Cells(doubleEntryRow, 17 ).Value= "Loss On Sale"

    doubleEntryRow = doubleEntryRow + 1
    
    transRow = transRow + 1


excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelWb.Save()
