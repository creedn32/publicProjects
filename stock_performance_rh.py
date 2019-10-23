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
startingRow = 2

excelApp.Workbooks.Open(filePath + "\\" + fileName + fileExtension)
excelApp.Calculation = win32com.client.constants.xlCalculationManual
excelWb = excelApp.Workbooks(fileName + fileExtension)
excelFromRobinhoodSheet = excelWb.Worksheets("From Robinhood")

copyRow = startingRow
pasteRow = startingRow
pasteCol = 3

while excelFromRobinhoodSheet.Cells(copyRow, 1).Value:
    
    if pasteCol > 5 and re.search(" shares at \$", excelFromRobinhoodSheet.Cells(copyRow, 1).Value) == None:
        pasteCol = 3
        pasteRow = pasteRow + 1

    if excelFromRobinhoodSheet.Cells(copyRow, 1).Value != "Older":
        excelFromRobinhoodSheet.Cells(copyRow, 1).Copy(excelFromRobinhoodSheet.Cells(pasteRow, pasteCol))
        pasteCol = pasteCol + 1

    copyRow = copyRow + 1


excelFromRobinhoodSheet.Range("C2:F2").CurrentRegion.Sort(Key1=excelFromRobinhoodSheet.Range("D2"), Order1=win32com.client.constants.xlAscending, Orientation=win32com.client.constants.xlSortColumns)


transRow = startingRow
doubleEntryRow = startingRow

while excelFromRobinhoodSheet.Cells(transRow, 3).Value:

    if excelFromRobinhoodSheet.Cells(transRow, 5).Value != "Failed":

        acctName = ""
        companyName = ""
        transType = ""
        shares = ""
        currentLot = ""
        excelFromRobinhoodSheet.Cells(doubleEntryRow, 13).Value = excelFromRobinhoodSheet.Cells(transRow, 4).Value.strftime("%m/%d/%y")

        if re.search("Interest Payment", excelFromRobinhoodSheet.Cells(transRow, 3).Value):
            acctName = "Cash - Rh"
            transType = "Receive Interest"
        elif re.search("Dividend from", excelFromRobinhoodSheet.Cells(transRow, 3).Value):
            acctName = "Cash - Rh"
            companyNameRegex = re.compile(r"^(Dividend from )(.+)$")
            mo = companyNameRegex.search(excelFromRobinhoodSheet.Cells(transRow, 3).Value)
            companyName = mo.group(2)

            if companyName == "Tessera Technologies, Inc. - Common Stock":
                companyName = "Xperi"
            
            transType = "Receive Dividend"
            purchaseCount = 0
            
            for i in range(startingRow, doubleEntryRow):
                if excelFromRobinhoodSheet.Cells(i, 9).Value == companyName and excelFromRobinhoodSheet.Cells(i, 8).Value == "Purchase Stock" and excelFromRobinhoodSheet.Cells(i, 14).Value == "Cash - Rh":
                    currentLot = excelFromRobinhoodSheet.Cells(i, 11).Value
                    purchaseCount = purchaseCount + 1

            shares = purchaseCount
            if purchaseCount == 1:
                excelFromRobinhoodSheet.Cells(doubleEntryRow, 11).Value = currentLot
        
            
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
            
            if companyName == "Tessera Technologies, Inc. - Common Stock":
                companyName = "Xperi"

            excelFromRobinhoodSheet.Cells(doubleEntryRow, 11).Value = str(excelFromRobinhoodSheet.Cells(doubleEntryRow, 13).Value.month) + str(excelFromRobinhoodSheet.Cells(doubleEntryRow, 13).Value.strftime('%d')) + str(excelFromRobinhoodSheet.Cells(doubleEntryRow, 13).Value.strftime('%y'))
            transType = "Purchase Stock"

            sharesRegex = re.compile(r"^(.+)( shares at .+)$")
            mo = sharesRegex.search(excelFromRobinhoodSheet.Cells(transRow, 6).Value)
            shares = mo.group(1)


        excelFromRobinhoodSheet.Cells(doubleEntryRow, 8).Value = transType
        excelFromRobinhoodSheet.Cells(doubleEntryRow, 9).Value = companyName
        excelFromRobinhoodSheet.Cells(doubleEntryRow, 10).Value = "Rh"
        excelFromRobinhoodSheet.Cells(doubleEntryRow, 12).Value = shares
        excelFromRobinhoodSheet.Cells(doubleEntryRow, 14).Formula = acctName
        excelFromRobinhoodSheet.Cells(doubleEntryRow, 15).Value = abs(excelFromRobinhoodSheet.Cells(transRow, 5).Value)
       
        
        
        
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
        excelFromRobinhoodSheet.Cells(doubleEntryRow, 9).Value = excelFromRobinhoodSheet.Cells(doubleEntryRow - 1, 9).Value
        excelFromRobinhoodSheet.Cells(doubleEntryRow, 10).Value = excelFromRobinhoodSheet.Cells(doubleEntryRow - 1, 10).Value
        excelFromRobinhoodSheet.Cells(doubleEntryRow, 11).Value = excelFromRobinhoodSheet.Cells(doubleEntryRow - 1, 11).Value
        excelFromRobinhoodSheet.Cells(doubleEntryRow, 12).Value = excelFromRobinhoodSheet.Cells(doubleEntryRow - 1, 12).Value
        excelFromRobinhoodSheet.Cells(doubleEntryRow, 13).Value = excelFromRobinhoodSheet.Cells(doubleEntryRow - 1, 13).Value
        excelFromRobinhoodSheet.Cells(doubleEntryRow, 14).Value = acctName
        excelFromRobinhoodSheet.Cells(doubleEntryRow, 15).Value = excelFromRobinhoodSheet.Cells(doubleEntryRow - 1, 15).Value * -1
        #excelFromRobinhoodSheet.Cells(doubleEntryRow, 16).Value = excelFromRobinhoodSheet.Cells(doubleEntryRow - 1, 16).Value
                                                                                                                                                                                                                          
                                                                                                                                                                                                                           
     
        
        doubleEntryRow = doubleEntryRow + 1
    transRow = transRow + 1



excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelWb.Save()
