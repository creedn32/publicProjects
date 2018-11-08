print("Cmt: Importing modules...")

import time, win32com.client, os, re, datetime

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
excelFromRobinhoodSheet = excelWb.Worksheets("From Robinhood")

copyRow = 1
pasteRow = 1
pasteCol = 3

##while excelFromRobinhoodSheet.Cells(copyRow, 1).Value:
##
####    if (copyRow - 0) % 3 == 0:
####        pasteCol = 3
####    elif (copyRow - 1) % 3 == 0:
####        pasteCol = 4
####    elif (copyRow - 2) % 3 == 0:
####        pasteCol = 5
##
##    if pasteCol > 5 and re.search(" shares at \$", excelFromRobinhoodSheet.Cells(copyRow, 1).Value) == None:
##        pasteCol = 3
##        pasteRow = pasteRow + 1
##        
####    if copyRow % 3 == 0 and copyRow != 3:
####        pasteRow = pasteRow + 1
##
##    excelFromRobinhoodSheet.Cells(copyRow, 1).Copy(excelFromRobinhoodSheet.Cells(pasteRow, pasteCol))
##
##    pasteCol = pasteCol + 1
##
##    copyRow = copyRow + 1


transRow = 1
doubleEntryRow = 1

while excelFromRobinhoodSheet.Cells(transRow, 3).Value:

    amountFactor = 1

    if excelFromRobinhoodSheet.Cells(transRow, 5).Value < 0:
        amountFactor = -1
      
    acctName = ""
    companyName = ""
    transType = ""
    excelFromRobinhoodSheet.Cells(doubleEntryRow, 13).Value = excelFromRobinhoodSheet.Cells(transRow, 4).Value.strftime("%m/%d/%y")

    if re.search("Interest Payment", excelFromRobinhoodSheet.Cells(transRow, 3).Value):
        acctName = "Cash - Rh"
        transType = "Receive Interest"
    elif re.search("Dividend from", excelFromRobinhoodSheet.Cells(transRow, 3).Value):
        acctName = "Cash - Rh"
        companyNameRegex = re.compile(r"^(Dividend from )(.+)$")
        mo = companyNameRegex.search(excelFromRobinhoodSheet.Cells(transRow, 3).Value)
        companyName = mo.group(2)
        transType = "Receive Dividend"
    elif re.search("Withdrawal to", excelFromRobinhoodSheet.Cells(transRow, 3).Value):
        acctName = "Capital Contributions"
        transType = "Cash To Owners"
    elif re.search("Deposit from", excelFromRobinhoodSheet.Cells(transRow, 3).Value):
        acctName = "Cash - Rh"
        transType = "Cash From Owners"
    elif re.search("Market Buy", excelFromRobinhoodSheet.Cells(transRow, 3).Value):
        acctName = "=I" + str(doubleEntryRow) + "&\" - Investment Asset - Rh - \"&" + "K" + str(doubleEntryRow)
        companyNameRegex = re.compile(r"^(.+)( Market Buy)$")
        mo = companyNameRegex.search(excelFromRobinhoodSheet.Cells(transRow, 3).Value)
        companyName = mo.group(1)
        excelFromRobinhoodSheet.Cells(doubleEntryRow, 11).Value = str(excelFromRobinhoodSheet.Cells(doubleEntryRow, 13).Value.month) + str(excelFromRobinhoodSheet.Cells(doubleEntryRow, 13).Value.strftime('%d')) + str(excelFromRobinhoodSheet.Cells(doubleEntryRow, 13).Value.strftime('%y'))
        transType = "Purchase Stock"
        
    excelFromRobinhoodSheet.Cells(doubleEntryRow, 8).Value = transType
    excelFromRobinhoodSheet.Cells(doubleEntryRow, 10).Value = "Rh"
    excelFromRobinhoodSheet.Cells(doubleEntryRow, 14).Formula = acctName
    excelFromRobinhoodSheet.Cells(doubleEntryRow, 15).Value = excelFromRobinhoodSheet.Cells(transRow, 5).Value * amountFactor
    excelFromRobinhoodSheet.Cells(doubleEntryRow, 16).Value = companyName
    
    
    
    doubleEntryRow = doubleEntryRow + 1
    acctName = ""
    
    if re.search("Interest Payment", excelFromRobinhoodSheet.Cells(transRow, 3).Value):
        acctName = "Interest Revenue"
    elif re.search("Dividend from", excelFromRobinhoodSheet.Cells(transRow, 3).Value):
        acctName = "Dividend Revenue"
    elif re.search("Withdrawal to", excelFromRobinhoodSheet.Cells(transRow, 3).Value):
        acctName = "Cash - Rh"
    elif re.search("Deposit from", excelFromRobinhoodSheet.Cells(transRow, 3).Value):
        acctName = "Capital Contributions"
    elif re.search("Market Buy", excelFromRobinhoodSheet.Cells(transRow, 3).Value):
        acctName = "Cash - Rh"

    excelFromRobinhoodSheet.Cells(doubleEntryRow, 8).Value = excelFromRobinhoodSheet.Cells(doubleEntryRow - 1, 8).Value
    #excelFromRobinhoodSheet.Cells(doubleEntryRow, 9).Value = excelFromRobinhoodSheet.Cells(doubleEntryRow - 1, 9).Value
    excelFromRobinhoodSheet.Cells(doubleEntryRow, 10).Value = excelFromRobinhoodSheet.Cells(doubleEntryRow - 1, 10).Value
    excelFromRobinhoodSheet.Cells(doubleEntryRow, 11).Value = excelFromRobinhoodSheet.Cells(doubleEntryRow - 1, 11).Value
    excelFromRobinhoodSheet.Cells(doubleEntryRow, 12).Value = excelFromRobinhoodSheet.Cells(doubleEntryRow - 1, 12).Value
    excelFromRobinhoodSheet.Cells(doubleEntryRow, 13).Value = excelFromRobinhoodSheet.Cells(doubleEntryRow - 1, 13).Value
    excelFromRobinhoodSheet.Cells(doubleEntryRow, 14).Value = acctName
    excelFromRobinhoodSheet.Cells(doubleEntryRow, 15).Value = excelFromRobinhoodSheet.Cells(doubleEntryRow - 1, 15).Value * -1
    excelFromRobinhoodSheet.Cells(doubleEntryRow, 16).Value = excelFromRobinhoodSheet.Cells(doubleEntryRow - 1, 16).Value
                                                                                                                                                                                                                      
                                                                                                                                                                                                                       
 
    
    doubleEntryRow = doubleEntryRow + 1
    transRow = transRow + 1


excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelWb.Save()
