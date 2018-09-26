#on comparison sheet, could write only the necessary columns
#use find function instead of looping so much
#create a module to import with the emptyStr(s) function
#use faster method to copy data


print("Cmt: Importing modules...")

import time, win32com.client 

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

excelApp.Workbooks.Open(filePath + fileName)
excelWb = excelApp.Workbooks(fileName)

excelGPTableSheet = excelWb.Worksheets("GP Table")
excelBankTableSearchSheet = excelWb.Worksheets("Bank Table Search")
excelCompSheet = excelWb.Worksheets("Comparison")
excelApp.Visible = True

print("Cmt: Open and connect to file...Done.")


excelBankTableSearchSheet.Range(excelBankTableSearchSheet.Cells(1, 1), excelBankTableSearchSheet.Cells(1, 14)).Copy()
excelCompSheet.Range(excelCompSheet.Cells(1, 1), excelCompSheet.Cells(1, 14)).PasteSpecial(Paste=win32com.client.constants.xlPasteValues)

excelGPTableSheet.Range(excelGPTableSheet.Cells(1, 1), excelGPTableSheet.Cells(1, 18)).Copy()
excelCompSheet.Range(excelCompSheet.Cells(1, 15), excelCompSheet.Cells(1, 32)).PasteSpecial(Paste=win32com.client.constants.xlPasteValues)



row = 2

while excelGPTableSheet.Cells(row, 1).Value:

    #put in GP data
    
    excelGPTableSheet.Range(excelGPTableSheet.Cells(row, 1), excelGPTableSheet.Cells(row, 18)).Copy()
    excelCompSheet.Range(excelCompSheet.Cells(row, 15), excelCompSheet.Cells(row, 32)).PasteSpecial(Paste=win32com.client.constants.xlPasteValues)


    #check bank data


  

    if excelGPTableSheet.Cells(row, 14).Value:


        bankRow = 2
        foundRows = []


        #myCell = excelBankTableSearchSheet.Range("K:K").Find(excelGPTableSheet.Cells(row, 7).Value)
        #if myCell:
        #    print(myCell.Row)
        
        while excelBankTableSearchSheet.Cells(bankRow, 1).Value:

            if excelBankTableSearchSheet.Cells(bankRow, 13).Value:
                if excelGPTableSheet.Cells(row, 7).Value == excelBankTableSearchSheet.Cells(bankRow, 11).Value and str(excelGPTableSheet.Cells(row, 14).Value)[:-2][-5:] == str(excelBankTableSearchSheet.Cells(bankRow, 13).Value)[:-2][-5:]:
                    foundRows.append(bankRow)

            bankRow = bankRow + 1

           
                  
        if len(foundRows) != 1:

             
            if excelGPTableSheet.Cells(row, 13).Value != "Check" or (excelGPTableSheet.Cells(row, 13).Value == "Check" and "ACH" in str(excelGPTableSheet.Cells(row, 14).Value)) or (excelGPTableSheet.Cells(row, 13).Value == "Check" and len(str(excelGPTableSheet.Cells(row, 14).Value)[:-2]) != 5):
                secondBankRow = 2
                foundRows = []

                
                while excelBankTableSearchSheet.Cells(secondBankRow, 1).Value:

                   
                    if excelGPTableSheet.Cells(row, 7).Value == excelBankTableSearchSheet.Cells(secondBankRow, 11).Value and excelBankTableSearchSheet.Cells(secondBankRow, 9).Value != "Check(s) Paid":
                        foundRows.append(secondBankRow)

                    secondBankRow = secondBankRow + 1


        if len(foundRows) == 1:

            excelBankTableSearchSheet.Range(excelBankTableSearchSheet.Cells(foundRows[0], 1), excelBankTableSearchSheet.Cells(foundRows[0], 14)).Copy()
            excelCompSheet.Range(excelCompSheet.Cells(row, 1), excelCompSheet.Cells(row, 14)).PasteSpecial(Paste=win32com.client.constants.xlPasteValues)
            
            excelBankTableSearchSheet.Cells(foundRows[0], 1).EntireRow.Delete()

        

    excelWb.Save()                
    row = row + 1

excelCompSheet.Cells.EntireColumn.AutoFit()


print("Elapsed time is " + str(time.time() - start_time))




