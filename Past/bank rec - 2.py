
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

excelBankTableSheet = excelWb.Worksheets("Bank Table")
excelBankTableSearchSheet = excelWb.Worksheets("Bank Table Search")
excelApp.Visible = True

print("Cmt: Open and connect to file...Done.")


row = 1

while excelBankTableSheet.Cells(row, 1).Value:
    for bankCol in range(1, 7):
        excelBankTableSearchSheet.Cells(row, bankCol).Value = excelBankTableSheet.Cells(row, bankCol).Value

    excelBankTableSearchSheet.Cells(row, 7).Value = excelBankTableSheet.Cells(row, 9).Value

    row = row + 1


excelBankTableSearchSheet.Cells.EntireColumn.AutoFit()


print("Elapsed time is " + str(time.time() - start_time))




