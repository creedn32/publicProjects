#if data is repeated, make it a variable
#create dictionary or class for columns
#reduce repeated code, like code for each webpage
#make functions out of repeated code

import bs4, re, os, win32com.client, sys

# get Excel going

stockListFilePath = os.path.abspath(os.curdir)
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
        "tickerCol": 1,
	    "finStats": {
		"Statistics": {
            "folderName": "Statistics",
			"dateCol": 4,
			"lastCol": 11,
			"tickerMatchCol": 5,
			"dataPts": {
                                "Trailing P/E": 6,
                                "Forward P/E": 8,
                                "Total Debt/Equity": 10,
                                "Market Cap (intraday)": 12
                                }
		},
		"Balance Sheet": {
            "folderName": "Balance Sheets",
			"dateCol": 14,
			"lastCol": 21,
			"tickerMatchCol": 15,
                        "dataPts": {
                                "Total Assets": 16,
                                "Total Stockholder Equity": 18,
                                "Total Liabilities": 20
                                }
		},
		"Income Statement": {
            "folderName": "Income Statements",
			"dateCol": 22,
			"lastCol": 27,
			"tickerMatchCol": 23,
                        "dataPts": {
                                "Total Revenue": 24,
                                "Net Income": 26
                                }
		}
        }
}



for currPage in col["finStats"]:

    folderName = col["finStats"][currPage]["folderName"]
    filePath = os.path.abspath("..") + "\\Stock_Data_Data\\Downloaded HTML Files\\" + folderName + "\\"
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

row = 6

while listSheet.Cells(row, col["tickerCol"]).Value:


    # for each stock, find the newest file in the folder of the downloaded files

    stockTicker = listSheet.Cells(row, col["tickerCol"]).Value
    print(stockTicker)

    for currPage in col["finStats"]:

        folderName = col["finStats"][currPage]["folderName"]
        downloadFolder = os.path.abspath("..") + "\\Stock_Data_Data\\Downloaded HTML Files\\" + folderName + "\\"
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
                    listSheet.Cells(row, i).Value = "No " + currPage + " file found for this stock."
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
                                    listSheet.Cells(row, dataPtCol + 1).Value = float(dataToWrite[:-1]) * 1000000000
                                elif str(dataToWrite[-1:]) == "M":
                                    listSheet.Cells(row, dataPtCol + 1).Value = float(dataToWrite[:-1]) * 1000000

                            else:

                                listSheet.Cells(row, dataPtCol + 1).Value = dataToWrite

                        else:
                            listSheet.Cells(row, dataPtCol + 1).Value = "Element does not exist in HTML"

    row = row + 1


         # # for each stock, find the newest file in the folder of the downloaded files
        #
        # currPage = "Balance Sheet"
        # downloadFolder = os.path.abspath(os.curdir) + "\\Downloaded HTML Files\\" + currPage + "s" + "\\"
        #
        # newestFileDate = 0 if not isinstance(dateCellVal, int) else int(dateCellVal)
        #
        # for fileName in os.listdir(downloadFolder):
        #
        #     fileTicker = fileName.split("-")[1]
        #
        #     if fileTicker == stockTicker:
        #
        #          fileDate = int(fileName.split("-")[0])
        #
        #          if fileDate > newestFileDate:
        #             newestFileDate = fileDate
        #
        #
        # if newestFileDate == 0:
        #
        #     # if you didn't find a file, put that information in the cells
        #
        #      for i in [currDateCol, col["finStats"][currPage]["lastCol"] + 1]:
        #             listSheet.Cells(row, i).Value = "No " + currPage + " file found for this stock."
        # else:
        #
        #     # if you did find a file, go to it and load it
        #
        #     dateCellVal = newestFileDate
        #     currentHTMLFile = open(downloadFolder + str(newestFileDate) + "-" + stockTicker + "-" + "from yahoo.html")
        #     beautifulSoupObject = bs4.BeautifulSoup(currentHTMLFile, "html.parser")
        #     for script in beautifulSoupObject(["script", "style"]):
        #             script.decompose()
        #
        #
        #     try:
        #             if stockTicker == beautifulSoupObject.find("title").contents[0].split(" ")[0]:
        #                     tickerMatch = "Yes"
        #             else:
        #                     tickerMatch = "No"
        #
        #             listSheet.Cells(row, col["finStats"][currPage]["tickerMatchCol"]).Value = tickerMatch
        #     except:
        #             print("File is empty")
        #
        #
        #     for dataPoint in col["finStats"][currPage]["dataPts"]:
        #
        #             print(dataPoint)
        #
        #             # go through each data point that you are looking for and put it into the spreadsheet
        #
        #             elements = beautifulSoupObject(text=dataPoint)
        #
        #
        #             listSheet.Cells(row, dataPtCol).Value = len(elements)
        #
        #             for element in elements:
        #                     if len(element.parent.parent.parent.contents) > 1:
        #                             listSheet.Cells(row, dataPtCol + 1).Value = element.parent.parent.parent.contents[1].string
        #                     else:
        #                             listSheet.Cells(row, dataPtCol + 1).Value = "Element does not exist in HTML"
        #
        #
        #         # for each stock, find the newest file in the folder of the downloaded files
        #
        # currPage = "Income Statement"
        # downloadFolder = os.path.abspath(os.curdir) + "\\Downloaded HTML Files\\" + currPage + "s" + "\\"
        #
        # newestFileDate = 0 if not isinstance(dateCellVal, int) else int(dateCellVal)
        #
        # for fileName in os.listdir(downloadFolder):
        #
        #     fileTicker = fileName.split("-")[1]
        #
        #     if fileTicker == stockTicker:
        #
        #          fileDate = int(fileName.split("-")[0])
        #
        #          if fileDate > newestFileDate:
        #             newestFileDate = fileDate
        #
        #
        # if newestFileDate == 0:
        #
        #     # if you didn't find a file, put that information in the cells
        #
        #      for i in [currDateCol, col["finStats"][currPage]["lastCol"] + 1]:
        #             listSheet.Cells(row, i).Value = "No " + currPage + " file found for this stock."
        # else:
        #
        #     # if you did find a file, go to it and load it
        #
        #     dateCellVal = newestFileDate
        #     currentHTMLFile = open(downloadFolder + str(newestFileDate) + "-" + stockTicker + "-" + "from yahoo.html")
        #     beautifulSoupObject = bs4.BeautifulSoup(currentHTMLFile, "html.parser")
        #     for script in beautifulSoupObject(["script", "style"]):
        #             script.decompose()
        #
        #
        #     try:
        #             if stockTicker == beautifulSoupObject.find("title").contents[0].split(" ")[0]:
        #                     tickerMatch = "Yes"
        #             else:
        #                     tickerMatch = "No"
        #
        #             listSheet.Cells(row, col["finStats"][currPage]["tickerMatchCol"]).Value = tickerMatch
        #     except:
        #             print("File is empty")
        #
        #
        #     for dataPoint in col["finStats"][currPage]["dataPts"]:
        #
        #             print(dataPoint)
        #
        #             # go through each data point that you are looking for and put it into the spreadsheet
        #
        #             elements = beautifulSoupObject(text=dataPoint)
        #
        #             for element in elements:
        #                     if dataPoint == "Net Income" and "Fz(15px)" in str(element.parent.parent):
        #                             elements.remove(element)
        #
        #
        #             listSheet.Cells(row, dataPtCol).Value = len(elements)
        #
        #             for element in elements:
        #
        #                     #if (dataPoint == "Net Income" and "Fz(15px)" not in str(element.parent.parent)) or dataPoint != "Net Income":
        #                      #       print(element.parent.parent)
        #
        #                     if len(element.parent.parent.parent.contents) > 1:
        #                              listSheet.Cells(row, dataPtCol + 1).Value = element.parent.parent.parent.contents[1].string
        #                     else:
        #                             listSheet.Cells(row, dataPtCol + 1).Value = "Element does not exist in HTML"
        #
        #






#create functions

# def soup_prettify2(soup, desired_indent): #where desired_indent is number of spaces as an int()
# 	pretty_soup = str()
# 	previous_indent = 0
# 	for line in soup.prettify().split("\n"): # iterate over each line of a prettified soup
# 		current_indent = str(line).find("<") # returns the index for the opening html tag '<'
# 		# which is also represents the number of spaces in the lines indentation
# 		if current_indent == -1 or current_indent > previous_indent + 2:
# 			current_indent = previous_indent + 1
# 			# str.find() will equal -1 when no '<' is found. This means the line is some kind
# 			# of text or script instead of an HTML element and should be treated as a child
# 			# of the previous line. also, current_indent should never be more than previous + 1.
# 		previous_indent = current_indent
# 		pretty_soup += write_new_line(line, current_indent, desired_indent)
# 	return pretty_soup
#
#
# def write_new_line(line, current_indent, desired_indent):
# 	new_line = ""
# 	spaces_to_add = (current_indent * desired_indent) - current_indent
# 	if spaces_to_add > 0:
# 		for i in range(spaces_to_add):
# 			new_line += " "
# 	new_line += str(line) + "\n"
# 	return new_line
#
