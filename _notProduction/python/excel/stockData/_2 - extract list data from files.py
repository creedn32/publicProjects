
cutOffDate = 20181227
cutOffDate = cutOffDate * 1000000

import bs4, os, win32com.client

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

# find the last sheet

folderName = "table html files"
filePath = os.path.abspath("..") + "\\private_data\\stock_data\\" + folderName + "\\"



listSheet.Range(listSheet.Cells(3, 1), listSheet.Cells(listSheet.Rows.Count, listSheet.Columns.Count)).Clear()

for fileName in os.listdir(filePath):

    #print(fileName.split("-")[1][:-5])
    #print(cutOffDate)

    if int(fileName.split("-")[1][:-5]) > cutOffDate:
        print(fileName.split("-")[0])
        currentHTMLFile = open(filePath + fileName)
        beautifulSoupObject = bs4.BeautifulSoup(currentHTMLFile, "html.parser")
        tables = beautifulSoupObject.find(id="tableform").find_all("table")

        tableMatrix = []
        for table in tables:
            # Here you can do whatever you want with the data! You can findAll table row headers, etc...

            list_of_rows = []
            rowNum = listSheet.Cells(1, 1).End(win32com.client.constants.xlDown).Row + 1

            for row in table.findAll('tr')[1:]:
                list_of_cells = []
                colNum = 2

                listSheet.Cells(rowNum, 1).Value = fileName.split("-")[0][:-1]

                for cell in row.findAll('td'):
                    text = cell.text.replace('&nbsp;', '')
                    listSheet.Cells(rowNum, colNum).Value = text
                    #print("rowNum = " + str(rowNum))
                    #print("colNum = " + str(colNum))
                    #print("value = " + text)
                    list_of_cells.append(text)
                    colNum = colNum + 1
                list_of_rows.append(list_of_cells)
                rowNum = rowNum + 1
            tableMatrix.append((list_of_rows, list_of_cells))


listSheet.Range(listSheet.Cells(3, 1), listSheet.Cells(listSheet.Cells(3, 1).End(win32com.client.constants.xlDown).Row, 1)).NumberFormat = "_(* #,##0_);_(* (#,##0);_(* ""-""??_);_(@_)"
listSheet.Range(listSheet.Cells(3, 4), listSheet.Cells(listSheet.Cells(3, 4).End(win32com.client.constants.xlDown).Row, 4)).NumberFormat = "_(* #,##0_);_(* (#,##0);_(* ""-""??_);_(@_)"
listSheet.Range(listSheet.Cells(3, 5), listSheet.Cells(listSheet.Cells(3, 5).End(win32com.client.constants.xlDown).Row, 5)).NumberFormat = "m/d/yyyy"
listSheet.Range(listSheet.Cells(3, 6), listSheet.Cells(listSheet.Cells(3, 6).End(win32com.client.constants.xlDown).Row, 6)).NumberFormat = "m/d/yyyy"


excelApp.DisplayAlerts = True
excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
stockWb.Save()