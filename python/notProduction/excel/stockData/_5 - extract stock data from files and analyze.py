#if data is repeated, make it a variable
#create dictionary or class for columns
#reduce repeated code, like code for each webpage
#make functions out of repeated code

import bs4, re, os, win32com.client, sys

# get Excel going

stockListFilePath = os.path.abspath("..") + "\\private_data\\stock_data"
fileName = "Monthly Purchase Process"
fileExtension = ".xlsx"
excelApp = win32com.client.gencache.EnsureDispatch('Excel.Application')
excelApp.Workbooks.Open(stockListFilePath + "\\" + fileName + fileExtension)
excelApp.Visible = True

stockWb = excelApp.Workbooks(fileName + fileExtension)
listSheet = stockWb.Worksheets[1]

# find the last sheet

for sheet in stockWb.Worksheets:
    if sheet.Name > listSheet.Name and sheet.Visible == -1:
        listSheet = sheet


col = {
        "topRow": 6,
        "tickerCol": 3,
        "peLimit": "$B$1",
        "deLimit": "$B$2",
	    "finStats": {
		"Statistics": {
            "folderName": "Statistics",
			"dateCol": 7,
			"lastCol": 16,
			"tickerMatchCol": 8,
			"dataPts": {
                                "Trailing P/E": 9,
                                "Forward P/E": 11,
                                "Total Debt/Equity": 13,
                                "Market Cap (intraday)": 15
                                }
		},
		"Balance Sheet": {
            "folderName": "Balance Sheets",
			"dateCol": 17,
			"lastCol": 24,
			"tickerMatchCol": 18,
                        "dataPts": {
                                "Total Assets": 19,
                                "Total Stockholder Equity": 21,
                                "Total Liabilities": 23
                                }
		},
		"Income Statement": {
            "folderName": "Income Statements",
			"dateCol": 25,
			"lastCol": 30,
			"tickerMatchCol": 26,
                        "dataPts": {
                                "Total Revenue": 27,
                                "Net Income": 29
                                }
		}
        }
}



for currPage in col["finStats"]:

    folderName = col["finStats"][currPage]["folderName"]
    filePath = os.path.abspath("..") + "\\private_data\\stock_data\\downloaded html files\\" + folderName + "\\"
    filesToRename = []

    for fileNameOld in os.listdir(filePath):

            fullPathOld = filePath + fileNameOld

            if os.path.getsize(fullPathOld) == 0:
                print("file to delete: " + fullPathOld)

            else:
                beautifulSoupObject = bs4.BeautifulSoup(open(fullPathOld), "html.parser")

                if fileNameOld.split("-")[1] != beautifulSoupObject.find("title").contents[0].split(" ")[0]:
                        fileNameNew = fileNameOld.replace("-" + fileNameOld.split("-")[1] + "-", "-" + beautifulSoupObject.find("title").contents[0].split(" ")[0] + "-")
                        filesToRename.append([fullPathOld, filePath + fileNameNew])

            break

    for f in filesToRename:
            print("file to rename in the " + folderName + " folder: " + str(f))
            #shutil.move(f[0], f[1])


print("Done renaming and deleting files.")

# go through each stock on the list


listSheet.Range(listSheet.Cells(col["topRow"], col["finStats"]["Statistics"]["dateCol"]), listSheet.Cells(listSheet.Rows.Count, listSheet.Columns.Count)).ClearContents()

row = col["topRow"]

while listSheet.Cells(row, col["tickerCol"]).Value:


    # for each stock, find the newest file in the folder of the downloaded files

    stockTicker = listSheet.Cells(row, col["tickerCol"]).Value
    print(stockTicker)

    for currPage in col["finStats"]:

        folderName = col["finStats"][currPage]["folderName"]
        downloadFolder = os.path.abspath("..") + "\\private_data\\stock_data\\downloaded html files\\" + folderName + "\\"
        currDateCol = col["finStats"][currPage]["dateCol"]
        dateCellVal = listSheet.Cells(row, currDateCol).Value
        newestFileDate = 0 if not isinstance(dateCellVal, int) else int(dateCellVal)


        for fileName in os.listdir(downloadFolder):

            fileTicker = fileName.split("-")[1]

            if fileTicker == stockTicker:

                 fileDate = int(fileName.split("-")[0])

                 if fileDate > newestFileDate:
                    newestFileDate = fileDate

        print(newestFileDate)
        
        if newestFileDate == 0:

            # if you didn't find a file, put that information in the cells
        
             for i in range(currDateCol, col["finStats"][currPage]["lastCol"] + 1):
                    listSheet.Cells(row, i).Value = "No " + currPage + " file found."
        else:

            # if you did find a file, go to it and load it

            listSheet.Cells(row, currDateCol).Value = newestFileDate

            currentHTMLFile = open(downloadFolder + str(newestFileDate) + "-" + stockTicker + "-" + "from yahoo.html")
            beautifulSoupObject = bs4.BeautifulSoup(currentHTMLFile, "html.parser")

            for script in beautifulSoupObject(["script", "style"]):
                    script.decompose()

            try:
                    if stockTicker == beautifulSoupObject.find("title").contents[0].split(" ")[0]:
                            tickerMatch = "Yes"
                    else:
                            tickerMatch = "No"

                    listSheet.Cells(row, col["finStats"][currPage]["tickerMatchCol"]).Value = tickerMatch
            except:
                    print("File is empty")



            for dataPoint in col["finStats"][currPage]["dataPts"]:

                    dataPtCol = col["finStats"][currPage]["dataPts"][dataPoint]
                    print(dataPoint)

                    # go through each data point that you are looking for and put it into the spreadsheet

                    elements = beautifulSoupObject(text=dataPoint)

                    for element in elements:
                        if dataPoint == "Net Income" and "Fz(15px)" in str(element.parent.parent):
                            elements.remove(element)


                    listSheet.Cells(row, dataPtCol).Value = len(elements)

                    for element in elements:
                        if len(element.parent.parent.parent.contents) > 1:

                            dataToWrite = element.parent.parent.parent.contents[1].string

                            if dataPoint == "Market Cap (intraday)":
                                if str(dataToWrite[-1:]) == "B":
                                    listSheet.Cells(row, dataPtCol + 1).Value = float(dataToWrite[:-1]) * 1000000#000
                                elif str(dataToWrite[-1:]) == "M":
                                    listSheet.Cells(row, dataPtCol + 1).Value = float(dataToWrite[:-1]) * 1000#000

                            else:

                                listSheet.Cells(row, dataPtCol + 1).Value = dataToWrite

                        else:
                            listSheet.Cells(row, dataPtCol + 1).Value = "Element does not exist in HTML"


    peRatioCol = col["finStats"]["Income Statement"]["lastCol"] + 1
    liabToEquityCol = col["finStats"]["Income Statement"]["lastCol"] + 2
    finalPECol = col["finStats"]["Income Statement"]["lastCol"] + 3
    trailPECol = col["finStats"]["Statistics"]["dataPts"]["Trailing P/E"] + 1
    totalStockEqCol = col["finStats"]["Balance Sheet"]["dataPts"]["Total Stockholder Equity"] + 1


    #listSheet.Cells(row, peRatioCol).Formula = "=IFERROR(P" + str(row) + "/AD" + str(row) + ",0)"
    listSheet.Cells(row, peRatioCol).Formula = "=IFERROR(INDIRECT(ADDRESS(" + str(row) + "," + str(col["finStats"]["Statistics"]["dataPts"]["Market Cap (intraday)"] + 1) + "))/" + "INDIRECT(ADDRESS(" + str(row) + "," + str(col["finStats"]["Income Statement"]["dataPts"]["Net Income"] + 1) + ")),0)"

    #listSheet.Cells(row, liabToEquityCol).Formula = "=IFERROR(X" + str(row) + "/V" + str(row) + ", \"N/A\")"
    listSheet.Cells(row, liabToEquityCol).Formula = "=IFERROR(INDIRECT(ADDRESS(" + str(row) + "," + str(col["finStats"]["Balance Sheet"]["dataPts"]["Total Liabilities"] + 1) + "))/INDIRECT(ADDRESS(" + str(row) + "," + str(totalStockEqCol) + ")), \"N/A\")"

    #listSheet.Cells(row, finalPECol).Formula = "=IF(AE" + str(row) + "=0,IF(J" + str(row) + "=\"N/A\",L" + str(row) + ",J" + str(row) + "),AE" + str(row) + ")"
    listSheet.Cells(row, finalPECol).Formula = "=IF(INDIRECT(ADDRESS(" + str(row) + "," + str(peRatioCol) + "))=0,IF(INDIRECT(ADDRESS(" + str(row) + "," + str(trailPECol) + "))=\"N/A\",INDIRECT(ADDRESS(" + str(row) + "," + str(col["finStats"]["Statistics"]["dataPts"]["Forward P/E"] + 1) + ")),INDIRECT(ADDRESS(" + str(row) + "," + str(trailPECol) + "))),INDIRECT(ADDRESS(" + str(row) + "," + str(peRatioCol) + ")))"

    #listSheet.Cells(row, col["finStats"]["Income Statement"]["lastCol"] + 4).Formula = "=IF(AND(AG" + str(row) + "<$B$1,AG" + str(row) + "<>0,AF" + str(row) + "<$B$2,V" + str(row) + ">0),\"Passed Test\","")"
    listSheet.Cells(row, col["finStats"]["Income Statement"]["lastCol"] + 4).Formula = "=IF(AND(INDIRECT(ADDRESS(" + str(row) + "," + str(finalPECol) + "))<" + col["peLimit"] + ",INDIRECT(ADDRESS(" + str(row) + "," + str(finalPECol) + "))<>0,INDIRECT(ADDRESS(" + str(row) + "," + str(liabToEquityCol) + "))<" + col["deLimit"] + ",INDIRECT(ADDRESS(" + str(row) + "," + str(totalStockEqCol) + "))>0),\"Passed Test\","")"

    row = row + 1

