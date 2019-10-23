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

tickerLookup = {'': '', 'ARGAN INC COM': 'AGX', 'BLOCK H & R INC': 'HRB', 'CAPELLA ED CO COM': 'CPLA', 'CISCO SYSTEMS INC': 'CSCO', 'COACH INC COM': 'COH', 'COLLECTORS UNIVERSE INC COM NEW': 'CLCT', 'DELUXE CORP': 'DLX', 'EBIX INC COM NEW': 'EBIX', 'ENZON PHARMACEUTICALS INC COM': 'ENZN', 'FLUOR CORP NEW COM': 'FLR', 'GAMESTOP CORP NEW CLASS A': 'GME', 'GILEAD SCIENCES INC': 'GILD', 'INTELIQUENT INC COM': 'IQNT', 'INTERDIGITAL INC PA FOR FUTURE ISSUES SEE 458660 COM': 'IDCC', 'KING DIGITAL ENTMT PLC ORD SHS ISIN#IE00BKJ9QQ58': 'KING', 'MANNATECH INC COM NEW': 'MTEX', 'MESABI TR CO CTF BEN INT': 'MSB', 'MIND C T I LTD SHS ISIN#IL0010851827': 'MNDO', 'NATHANS FAMOUS INC NEW COM': 'NATH', 'PDL BIOPHARMA INC COM': 'PDLI', 'PETMED EXPRESS INC COMMON STK': 'PETS', 'RPX CORP COM': 'RPXC', 'SPOK HLDGS INC COM': 'SPOK', 'STRAYER ED INC COM': 'STRA', 'TESSERA TECHNOLOGIES INC COM': 'XPER', 'VIACOM INC NEW CL B': 'VIAB', 'WAYSIDE TECHNOLOGY GROUP INC COM': 'WSTG'}

transRow = 225
doubleEntryRow = 1695

while excelFromMotifSheet.Cells(transRow, 1).Value:
    
    acctName = ""
    companyName = ""
    transType = ""
    shares = ""
    currentLot = ""

    
    excelFromMotifSheet.Cells(doubleEntryRow, 16).Value = excelFromMotifSheet.Cells(transRow, 1).Value.strftime("%m/%d/%y")

    if excelFromMotifSheet.Cells(transRow, 3).Value == "ACH" and excelFromMotifSheet.Cells(transRow, 9).Value > 0:
        acctName = "Cash - Mt"
        transType = "Cash From Owners"
    elif excelFromMotifSheet.Cells(transRow, 3).Value == "Dividend Paid":
        acctName = "Cash - Mt"
        companyNameRegex = re.compile(r"(.+)( SHRS )(.+)( RD )(.+)") 
        mo = companyNameRegex.search(excelFromMotifSheet.Cells(transRow, 2).Value)
        companyName = mo.group(3)
        transType = "Receive Dividend"

        purchaseCount = 0
            
        for i in range(2, doubleEntryRow):
            if excelFromMotifSheet.Cells(i, 12).Value == tickerLookup[companyName] and excelFromMotifSheet.Cells(i, 11).Value == "Purchase Stock" and excelFromMotifSheet.Cells(i, 17).Value == "Cash - Mt":
                currentLot = excelFromMotifSheet.Cells(i, 14).Value
                purchaseCount = purchaseCount + 1

        shares = purchaseCount

        if purchaseCount == 1:
                excelFromMotifSheet.Cells(doubleEntryRow, 14).Value = currentLot

    elif excelFromMotifSheet.Cells(transRow, 3).Value == "Distribution":
        acctName = "Cash - Mt"
        companyNameRegex = re.compile(r"(.+)( SHRS )(.+)( RD )(.+)")
        mo = companyNameRegex.search(excelFromMotifSheet.Cells(transRow, 2).Value)
        companyName = mo.group(3)
        transType = "Receive Distribution"
    elif excelFromMotifSheet.Cells(transRow, 3).Value == "ACH" and excelFromMotifSheet.Cells(transRow, 9).Value <= 0:
        acctName = "Capital Contributions"
        transType = "Cash To Owners"
    elif excelFromMotifSheet.Cells(transRow, 3).Value == "Fee":
        acctName = "Platform Fee Expense"
        transType = "Pay Platform Fee"
    elif excelFromMotifSheet.Cells(transRow, 3).Value == "Credit":
        acctName = "Cash - Mt"
        transType = "Receive Platform Fee"

        
##    elif re.search("Market Buy", excelFromMotifSheet.Cells(transRow, 3).Value):
##        acctName = "=I" + str(doubleEntryRow) + "&\" - Investment Asset - Rh - \"&" + "K" + str(doubleEntryRow)
##        companyNameRegex = re.compile(r"^(.+)( Market Buy)$")
##        mo = companyNameRegex.search(excelFromMotifSheet.Cells(transRow, 3).Value)
##        companyName = mo.group(1)
##        excelFromMotifSheet.Cells(doubleEntryRow, 11).Value = str(excelFromMotifSheet.Cells(doubleEntryRow, 13).Value.month) + str(excelFromMotifSheet.Cells(doubleEntryRow, 13).Value.strftime('%d')) + str(excelFromMotifSheet.Cells(doubleEntryRow, 13).Value.strftime('%y'))
##        transType = "Purchase Stock"


        
    excelFromMotifSheet.Cells(doubleEntryRow, 11).Value = transType
    excelFromMotifSheet.Cells(doubleEntryRow, 12).Value = tickerLookup[companyName]
    excelFromMotifSheet.Cells(doubleEntryRow, 13).Value = "Mt"
    excelFromMotifSheet.Cells(doubleEntryRow, 15).Value = shares
    excelFromMotifSheet.Cells(doubleEntryRow, 17).Formula = acctName
    
    if excelFromMotifSheet.Cells(transRow, 9).Value == "--":
        excelFromMotifSheet.Cells(doubleEntryRow, 18).Value = 0
    else:
        excelFromMotifSheet.Cells(doubleEntryRow, 18).Value = abs(excelFromMotifSheet.Cells(transRow, 9).Value)
        
    excelFromMotifSheet.Cells(doubleEntryRow, 19).Value = companyName
 
    doubleEntryRow = doubleEntryRow + 1
    acctName = ""
    
    if transType == "Receive Dividend":
        acctName = "Dividend Revenue"
    elif transType == "Cash To Owners":
        acctName = "Cash - Mt"
    elif transType == "Cash From Owners":
        acctName = "Capital Contributions"
    elif transType == "Purchase Stock":
        acctName = "Cash - Mt"
    elif transType == "Pay Platform Fee":
        acctName = "Cash - Mt"
    elif transType == "Receive Platform Fee":
        acctName = "Platform Fee Expense"

        
        

    excelFromMotifSheet.Cells(doubleEntryRow, 11).Value = excelFromMotifSheet.Cells(doubleEntryRow - 1, 11).Value
    excelFromMotifSheet.Cells(doubleEntryRow, 12).Value = excelFromMotifSheet.Cells(doubleEntryRow - 1, 12).Value
    excelFromMotifSheet.Cells(doubleEntryRow, 13).Value = excelFromMotifSheet.Cells(doubleEntryRow - 1, 13).Value
    excelFromMotifSheet.Cells(doubleEntryRow, 14).Value = excelFromMotifSheet.Cells(doubleEntryRow - 1, 14).Value
    excelFromMotifSheet.Cells(doubleEntryRow, 15).Value = excelFromMotifSheet.Cells(doubleEntryRow - 1, 15).Value
    excelFromMotifSheet.Cells(doubleEntryRow, 16).Value = excelFromMotifSheet.Cells(doubleEntryRow - 1, 16).Value
    excelFromMotifSheet.Cells(doubleEntryRow, 17).Value = acctName
    excelFromMotifSheet.Cells(doubleEntryRow, 18).Value = excelFromMotifSheet.Cells(doubleEntryRow - 1, 18).Value * -1
    excelFromMotifSheet.Cells(doubleEntryRow, 19).Value = excelFromMotifSheet.Cells(doubleEntryRow - 1, 19).Value                                                                                                                                                                                                                  
                                                                                                                                                                                                                       
    print(doubleEntryRow)
    doubleEntryRow = doubleEntryRow + 1
    transRow = transRow + 1


excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelWb.Save()
