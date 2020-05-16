import os, win32com.client, sys

# get Excel going

stockListFilePath = os.path.abspath("..") + "\\private_data\\stock_data"
fileName = "Monthly Purchase Process"
fileExtension = ".xlsx"
excelApp = win32com.client.gencache.EnsureDispatch('Excel.Application')
excelApp.DisplayAlerts = False
excelApp.Workbooks.Open(stockListFilePath + "\\" + fileName + fileExtension)
excelApp.Calculation = win32com.client.constants.xlCalculationManual
excelApp.Visible = True


stockWb = excelApp.Workbooks(fileName + fileExtension)
listSheet = stockWb.Worksheets["Step 2 - From Website"]

firstCell = listSheet.Cells(2, 1)
lastCell = listSheet.Cells(listSheet.Cells(2, 1).End(win32com.client.constants.xlDown).Row, listSheet.Cells(2, 1).End(win32com.client.constants.xlToRight).Column)

print(firstCell)
print(lastCell)

# listSheet.Range(firstCell, lastCell).Sort(Key1=listSheet.Cells(2, 1), Order1=win32com.client.constants.xlAscending, Key2=listSheet.Cells(2, 2), Order2=win32com.client.constants.xlAscending, Header=win32com.client.constants.xlYes, Orientation=win32com.client.constants.xlSortColumns)
listSheet.Range(firstCell, lastCell).Sort(Key1=listSheet.Cells(2, 5), Order1=win32com.client.constants.xlDescending, Key2=listSheet.Cells(2, 1), Order2=win32com.client.constants.xlAscending, Key3=listSheet.Cells(2, 2), Order3=win32com.client.constants.xlAscending, Header=win32com.client.constants.xlYes, Orientation=win32com.client.constants.xlSortColumns)

try:
    stockWb.Worksheets("Step 2 - From Website2").Delete()
except:
    print("Error")

newSheet = stockWb.Worksheets.Add(After=listSheet)
#newSheet = stockWb.ActiveSheet
newSheet.Name = "Step 2 - From Website2"
listSheet.Cells.Copy(Destination=newSheet.Range("A1"))

row = 3

while listSheet.Cells(row, 1).Value:
    print("row is " + str(row))
    dupCheckRow = row + 1
    while listSheet.Cells(dupCheckRow, 1).Value:
        #print(dupCheckRow)
        if listSheet.Cells(dupCheckRow, 2).Value == listSheet.Cells(row, 2).Value:
            #print("current company is " + listSheet.Cells(row, 2).Value + " and row " + str(dupCheckRow) + " has company " + listSheet.Cells(dupCheckRow, 2).Value + " so it was deleted")
            listSheet.Rows(dupCheckRow).Delete()
            dupCheckRow = dupCheckRow - 1
        dupCheckRow = dupCheckRow + 1
    row = row + 1



excelApp.DisplayAlerts = True
excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
stockWb.Save()