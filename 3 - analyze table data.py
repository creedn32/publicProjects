import bs4, os, win32com.client

# get Excel going

stockListFilePath = os.path.abspath("..") + "\\Stock_Data_Data"
fileName = "Monthly Purchase Process"
fileExtension = ".xlsx"
excelApp = win32com.client.gencache.EnsureDispatch('Excel.Application')
excelApp.Workbooks.Open(stockListFilePath + "\\" + fileName + fileExtension)
excelApp.Visible = True

stockWb = excelApp.Workbooks(fileName + fileExtension)
listSheet = stockWb.Worksheets["Step 1A - Temp Data"]

# find the last sheet

folderName = "Table HTML Files"
filePath = os.path.abspath("..") + "\\Stock_Data_Data\\" + folderName + "\\"

for fileName in os.listdir(filePath):
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


