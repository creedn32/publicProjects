#if data is repeated, make it a variable
#create dictionary or class for columns
#reduce repeated code, like code for each webpage
#make functions out of repeated code


import bs4, re, os, win32com.client, sys


#create functions

def soup_prettify2(soup, desired_indent): #where desired_indent is number of spaces as an int() 
	pretty_soup = str()
	previous_indent = 0
	for line in soup.prettify().split("\n"): # iterate over each line of a prettified soup
		current_indent = str(line).find("<") # returns the index for the opening html tag '<' 
		# which is also represents the number of spaces in the lines indentation
		if current_indent == -1 or current_indent > previous_indent + 2:
			current_indent = previous_indent + 1
			# str.find() will equal -1 when no '<' is found. This means the line is some kind 
			# of text or script instead of an HTML element and should be treated as a child 
			# of the previous line. also, current_indent should never be more than previous + 1.	
		previous_indent = current_indent
		pretty_soup += write_new_line(line, current_indent, desired_indent)
	return pretty_soup
		
		
def write_new_line(line, current_indent, desired_indent):
	new_line = ""
	spaces_to_add = (current_indent * desired_indent) - current_indent
	if spaces_to_add > 0:
		for i in range(spaces_to_add):
			new_line += " "		
	new_line += str(line) + "\n"
	return new_line




# get Excel going

excelApp = win32com.client.DispatchEx('Excel.Application')
stockListFileFolder = os.path.abspath(os.curdir)
stockListFileName = "Monthly Purchase Process.xlsx"
excelApp.Visible = True
excelApp.Workbooks.Open(stockListFileFolder + "\\" + stockListFileName)
stockListWb = excelApp.Workbooks(stockListFileName)


col = {
        "Ticker Col": 1,
	"Data": {
		"Statistics": {
			"Date": 4,
			"Last Col": 11,
			"Ticker Match": 5,
			"Data": {
                                "Trailing P/E": 6,
                                "Forward P/E": 8,
                                "Total Debt/Equity": 10,
                                "Market Cap (intraday)": 12
                                }
		},
		"Balance Sheet": {
			"Date": 14,
			"Last Col": 21,
			"Ticker Match": 15,
                        "Data": {
                                "Total Assets": 16,
                                "Total Stockholder Equity": 18,
                                "Total Liabilities": 20
                                }
		},
		"Income Statement": {
			"Date": 22,
			"Last Col": 27,
			"Ticker Match": 23,
                        "Data": {
                                "Total Revenue": 24,
                                "Net Income": 26
                                }
		}
        }
}



# find the last sheet

listSheet = stockListWb.Worksheets[1]

for sheet in stockListWb.Worksheets:
    if sheet.Name > listSheet.Name and sheet.Visible == -1:
        listSheet = sheet




currentPage = "Balance Sheets"
filePath = os.path.abspath(os.curdir) + "\\Downloaded HTML Files\\" + currentPage + "\\"
filesToRename = []



for fileNameOld in os.listdir(filePath):
        currentHTMLFile = open(filePath + fileNameOld)
        beautifulSoupObject = bs4.BeautifulSoup(currentHTMLFile, "html.parser")

        #print(fileNameOld.split("-")[1] + " = " + beautifulSoupObject.find("title").contents[0].split(" ")[0])

        if fileNameOld.split("-")[1] != beautifulSoupObject.find("title").contents[0].split(" ")[0]:
                fileNameNew = fileNameOld.replace("-" + fileNameOld.split("-")[1] + "-", "-" + beautifulSoupObject.find("title").contents[0].split(" ")[0] + "-")
                #print(fileNameOld)
                #print(fileNameNew)
                filesToRename.append([filePath + fileNameOld, filePath + fileNameNew])
                

for f in filesToRename:
        print(f)
        #shutil.move(f[0], f[1])



print(1)

# go through each stock on the list

row = 6

while listSheet.Cells(row, col["Ticker Col"]).Value:

 
    # for each stock, find the newest file in the folder of the downloaded files

    currentPage = "Statistics"
    downloadedFolder = os.path.abspath(os.curdir) + "\\Downloaded HTML Files\\" + currentPage + "\\"

    stockTicker = listSheet.Cells(row, col["Ticker Col"]).Value
    print(stockTicker)
    newestFileDate = 0 if not isinstance(listSheet.Cells(row, col["Data"][currentPage]["Date"]).Value, int) else int(listSheet.Cells(row, col["Data"][currentPage]["Date"]).Value)

    for fileName in os.listdir(downloadedFolder):
            
        fileTicker = fileName.split("-")[1]

        if fileTicker == stockTicker:
                
             fileDate = int(fileName.split("-")[0])
             
             if fileDate > newestFileDate:
                newestFileDate = fileDate


    if newestFileDate == 0:

        # if you didn't find a file, put that information in the cells

         for i in range(col["Data"][currentPage]["Date"], col["Data"][currentPage]["Last Col"] + 1):
                listSheet.Cells(row, i).Value = "No " + currentPage + " file found for this stock."
    else:

        # if you did find a file, go to it and load it

        listSheet.Cells(row, col["Data"][currentPage]["Date"]).Value = newestFileDate
        currentHTMLFile = open(downloadedFolder + str(newestFileDate) + "-" + stockTicker + "-" + "from yahoo.html")
        beautifulSoupObject = bs4.BeautifulSoup(currentHTMLFile, "html.parser")
        for script in beautifulSoupObject(["script", "style"]):
                script.decompose()

        try:
                if stockTicker == beautifulSoupObject.find("title").contents[0].split(" ")[0]:
                        tickerMatch = "Yes"
                else:
                        tickerMatch = "No"
                
                listSheet.Cells(row, col["Data"][currentPage]["Ticker Match"]).Value = tickerMatch
        except:
                print("File is empty")


                
        for dataPoint in col["Data"][currentPage]["Data"]:

                print(dataPoint)
                        
                # go through each data point that you are looking for and put it into the spreadsheet

                elements = beautifulSoupObject(text=dataPoint)
                #print(elements)

                listSheet.Cells(row, col["Data"][currentPage]["Data"][dataPoint]).Value = len(elements)

                for element in elements:                          
                        listSheet.Cells(row, col["Data"][currentPage]["Data"][dataPoint] + 1).Value = element.parent.parent.parent.contents[1].string

        if str(listSheet.Cells(row, 13).Value)[-1:] == "B":
                listSheet.Cells(row, 13).Value = float(listSheet.Cells(row, 13).Value[:-1])*1000000
        if str(listSheet.Cells(row, 13).Value)[-1:] == "M":
                listSheet.Cells(row, 13).Value = float(listSheet.Cells(row, 13).Value[:-1])*1000



    # for each stock, find the newest file in the folder of the downloaded files

    currentPage = "Balance Sheet"
    downloadedFolder = os.path.abspath(os.curdir) + "\\Downloaded HTML Files\\" + currentPage + "s" + "\\"

    newestFileDate = 0 if not isinstance(listSheet.Cells(row, col["Data"][currentPage]["Date"]).Value, int) else int(listSheet.Cells(row, col["Data"][currentPage]["Date"]).Value)

    for fileName in os.listdir(downloadedFolder):
            
        fileTicker = fileName.split("-")[1]

        if fileTicker == stockTicker:
                
             fileDate = int(fileName.split("-")[0])
             
             if fileDate > newestFileDate:
                newestFileDate = fileDate


    if newestFileDate == 0:

        # if you didn't find a file, put that information in the cells

         for i in [col["Data"][currentPage]["Date"], col["Data"][currentPage]["Last Col"] + 1]:
                listSheet.Cells(row, i).Value = "No " + currentPage + " file found for this stock."
    else:

        # if you did find a file, go to it and load it

        listSheet.Cells(row, col["Data"][currentPage]["Date"]).Value = newestFileDate
        currentHTMLFile = open(downloadedFolder + str(newestFileDate) + "-" + stockTicker + "-" + "from yahoo.html")
        beautifulSoupObject = bs4.BeautifulSoup(currentHTMLFile, "html.parser")
        for script in beautifulSoupObject(["script", "style"]):
                script.decompose()


        try:
                if stockTicker == beautifulSoupObject.find("title").contents[0].split(" ")[0]:
                        tickerMatch = "Yes"
                else:
                        tickerMatch = "No"
                
                listSheet.Cells(row, col["Data"][currentPage]["Ticker Match"]).Value = tickerMatch
        except:
                print("File is empty")


        for dataPoint in col["Data"][currentPage]["Data"]:

                print(dataPoint)
                        
                # go through each data point that you are looking for and put it into the spreadsheet

                elements = beautifulSoupObject(text=dataPoint)

              
                listSheet.Cells(row, col["Data"][currentPage]["Data"][dataPoint]).Value = len(elements)

                for element in elements:                          
                        if len(element.parent.parent.parent.contents) > 1:    
                                listSheet.Cells(row, col["Data"][currentPage]["Data"][dataPoint] + 1).Value = element.parent.parent.parent.contents[1].string
                        else:
                                listSheet.Cells(row, col["Data"][currentPage]["Data"][dataPoint] + 1).Value = "Element does not exist in HTML"


            # for each stock, find the newest file in the folder of the downloaded files

    currentPage = "Income Statement"
    downloadedFolder = os.path.abspath(os.curdir) + "\\Downloaded HTML Files\\" + currentPage + "s" + "\\"

    newestFileDate = 0 if not isinstance(listSheet.Cells(row, col["Data"][currentPage]["Date"]).Value, int) else int(listSheet.Cells(row, col["Data"][currentPage]["Date"]).Value)

    for fileName in os.listdir(downloadedFolder):
            
        fileTicker = fileName.split("-")[1]

        if fileTicker == stockTicker:
                
             fileDate = int(fileName.split("-")[0])
             
             if fileDate > newestFileDate:
                newestFileDate = fileDate


    if newestFileDate == 0:

        # if you didn't find a file, put that information in the cells

         for i in [col["Data"][currentPage]["Date"], col["Data"][currentPage]["Last Col"] + 1]:
                listSheet.Cells(row, i).Value = "No " + currentPage + " file found for this stock."
    else:

        # if you did find a file, go to it and load it

        listSheet.Cells(row, col["Data"][currentPage]["Date"]).Value = newestFileDate
        currentHTMLFile = open(downloadedFolder + str(newestFileDate) + "-" + stockTicker + "-" + "from yahoo.html")
        beautifulSoupObject = bs4.BeautifulSoup(currentHTMLFile, "html.parser")
        for script in beautifulSoupObject(["script", "style"]):
                script.decompose()


        try:
                if stockTicker == beautifulSoupObject.find("title").contents[0].split(" ")[0]:
                        tickerMatch = "Yes"
                else:
                        tickerMatch = "No"
                
                listSheet.Cells(row, col["Data"][currentPage]["Ticker Match"]).Value = tickerMatch
        except:
                print("File is empty")


        for dataPoint in col["Data"][currentPage]["Data"]:

                print(dataPoint)
                        
                # go through each data point that you are looking for and put it into the spreadsheet

                elements = beautifulSoupObject(text=dataPoint)

                for element in elements:
                        if dataPoint == "Net Income" and "Fz(15px)" in str(element.parent.parent):
                                elements.remove(element)
                                
                        
                listSheet.Cells(row, col["Data"][currentPage]["Data"][dataPoint]).Value = len(elements)

                for element in elements:
                                
                        #if (dataPoint == "Net Income" and "Fz(15px)" not in str(element.parent.parent)) or dataPoint != "Net Income":
                         #       print(element.parent.parent)
                                
                        if len(element.parent.parent.parent.contents) > 1:
                                 listSheet.Cells(row, col["Data"][currentPage]["Data"][dataPoint] + 1).Value = element.parent.parent.parent.contents[1].string
                        else:
                                listSheet.Cells(row, col["Data"][currentPage]["Data"][dataPoint] + 1).Value = "Element does not exist in HTML"



    row = row + 1







##    # for each stock, find the newest file in the Balance Sheets folder of the downloaded files

##    stockRatios = ["Total Assets", "Total Stockholder Equity"]
##    downloadedFolder = ""
##    fileNameRegEx = re.compile(r"(.*)-(.*)-(.*)-(.*)")
##    newestFileDate = ""
##
##    for fileName in os.listdir(downloadedFolder):
##
##        fileNameRegExResult = fileNameRegEx.findall(fileName)
##
##        if fileNameRegExResult[0][1] == listSheet.Cells(row, 1).Value:
##
##            if int(fileNameRegExResult[0][0]) >= int(
##                    0 if not isinstance(listSheet.Cells(row, 4).Value, int) else listSheet.Cells(row, 4).Value):
##                newestFileDate = fileNameRegExResult[0][0]
##
##    if newestFileDate == "":
##
##        # if you didn't find a Balance Sheet file, put that information in the cells
##
##        for i in range(4, 12):
##
##            if i != 5:
##                listSheet.Cells(row, i).Value = "No Balance Sheet downloaded file found for this stock"
##    else:
##
##        # if you did find a Balance Sheet file, go to it and load it
##
##        for fileName in os.listdir(downloadedFolder):
##
##            fileNameRegExResult = fileNameRegEx.findall(fileName)
##
##            if fileNameRegExResult[0][1] == listSheet.Cells(row, 1).Value:
##
##                if fileNameRegExResult[0][0] == newestFileDate:
##
##                    currentHTMLFile = open(downloadedFolder + fileName)
##                    beautifulSoupObject = bs4.BeautifulSoup(currentHTMLFile, "html.parser")
##                    for script in beautifulSoupObject(["script", "style"]):
##                        script.decompose()
##
##                    listSheet.Cells(row, 5).Value = newestFileDate
##
##
##                    for stockRatio in stockRatios:
##
##                        # go through each stock ratio that you are looking for from the Balance Sheet file and put it into the spreadsheet
##
##                        print(stockRatio)
##
##                        elements = beautifulSoupObject(text=re.compile(stockRatio))
##
##                        if stockRatio == "Total Assets":
##                            column = 12
##                        elif stockRatio == "Total Stockholder Equity":
##                            column = 14
##
##                        listSheet.Cells(row, column).Value = len(elements)
##
##                        for element in elements:
##                            
####                            parentCount = 0
####                            
####                            for parent in element.parents:
####                                print("stock: " + listSheet.Cells(row, 1).Value + "; ratio: " + stockRatio + "; element: " + str(element)[:1500] + "; parent " + str(parentCount) + ":")
####                                print(soup_prettify2(parent, desired_indent=2))
####
####                                if parentCount == 2:
####                                    break
####                                                       
####                                parentCount = parentCount + 1
####
####                            print(element.parent.parent.parent.contents[1].string)
##
##                            
####                            for cont in element.parent.parent.parent.contents:
####                                print("contents: " + str(cont))
####                            print(len(element.parent.parent.parent.contents))
##
##                            if len(element.parent.parent.parent.contents) > 1:    
##                                listSheet.Cells(row, column + 1).Value = element.parent.parent.parent.contents[1].string
##                            else:
##                                listSheet.Cells(row, column + 1).Value = "Element does not exist in HTML"
##
####    if row == 2:
####        break
##

    

        
##        for fileName in os.listdir(downloadedFolder):
##
##            fileNameRegExResult = fileNameRegEx.findall(fileName)
##
##            if fileNameRegExResult[0][1] == listSheet.Cells(row, 1).Value:
##
##                if fileNameRegExResult[0][0] == newestFileDate:
##                  
##                    currentHTMLFile = open(downloadedFolder + fileName)
##                    beautifulSoupObject = bs4.BeautifulSoup(currentHTMLFile, "html.parser")
##
##                    listSheet.Cells(row, 4).Value = newestFileDate
##
##                    for stockRatio in stockRatios:
##
##                        print(stockRatio)
##                        
##                        # go through each stock ratio that you are looking for from the Stats file and put it into the spreadsheet
##
##                        elements = beautifulSoupObject(text=re.compile(stockRatio))
##
##                        if stockRatio == "Trailing P/E":
##                            column = 6
##                        elif stockRatio == "Forward P/E":
##                            column = 8
##                        elif stockRatio == "Debt/Equity":
##                            column = 10
##
##                        listSheet.Cells(row, column).Value = len(elements)
##
##                        for element in elements:
##                            
##                            #print("stock: " + listSheet.Cells(row, 1).Value + "; ratio: " + stockRatio + ";")
##                            parentCount = 0
##                            
####                            for parent in element.parents:
####                                print("stock: " + listSheet.Cells(row, 1).Value + "; ratio: " + stockRatio + "; parent " + str(parentCount) + ":")
####                                print(soup_prettify2(parent, desired_indent=2))
####
####                                if parentCount == 2:
####                                    break
####                                
####                                parentCount = parentCount + 1
##
##
##                            
##                            listSheet.Cells(row, column + 1).Value = element.parent.parent.parent.contents[1].string
##
##
##
##
##
                        #print("stock: " + listSheet.Cells(row, 1).Value + "; ratio: " + stockRatio + ";")
##                        parentCount = 0
                            
##                            for parent in element.parents:
##                                print("stock: " + listSheet.Cells(row, 1).Value + "; ratio: " + stockRatio + "; parent " + str(parentCount) + ":")
##                                print(soup_prettify2(parent, desired_indent=2))
##
##                                if parentCount == 2:
##                                    break
##                                
##                                parentCount = parentCount + 1



##
##    #htmlDataSheet = stockListWb.Worksheets("Step 1 - HTML Data")
##    #a = (["'1:1", "'1:2"], ["'2:1", "'2:2", ["'2:3:1", "'2:3:2"]])
##    #list_flatten(beautifulSoupObject)
##
##
##
## #htmlDataSheetRow = 1
##
##                        # for i in beautifulSoupObject:
##                        #     htmlDataSheet.Cells(htmlDataSheetRow, 1).Value = str(i)
##                        #
##                        #     for j in i:
##                        #         htmlDataSheet.Cells(htmlDataSheetRow, 2).Value = str(j)
##                        #
##                        #     htmlDataSheetRow = htmlDataSheetRow + 1
##
##
##                        #list_flatten(beautifulSoupObject)
##
##                        #for element in elements:
## 
##                         #   parentHierarchyList = [element.string] + recursiveParent(element)
##
##                            #for i in range(len(parentHierarchyList) - 1, -1, -1):
##                            #    print("i is " + str(i) + " " + "-----" * (len(parentHierarchyList) - i - 1) + parentHierarchyList[i][0:40])
##
##                                #htmlDataSheet.Cells(htmlDataSheetRow, htmlDataSheetColumn).Value = element #element.parent.parent.parent.contents[1].string
##                                #htmlDataSheetRow = htmlDataSheetRow + 1
##
##
### currentHTMLFile = open(downloadedFolder + fileName)
### beautifulSoupObject = bs4.BeautifulSoup(currentHTMLFile, "html.parser")
###
### listSheet.Cells(row, 4).Value = newestFileDate
###
### elements = beautifulSoupObject(text=re.compile(stockRatios[0]))
### listSheet.Cells(row, 5).Value = len(elements)
###
### for element in elements:
###     listSheet.Cells(row, 6).Value = element.parent.parent.parent.contents[1].string
###
### elements = beautifulSoupObject(text=re.compile(stockRatios[1]))
### listSheet.Cells(row, 7).Value = len(elements)
###
### for element in elements:
###     listSheet.Cells(row, 8).Value = element.parent.parent.parent.contents[1].string
###
### elements = beautifulSoupObject(text=re.compile(stockRatios[2]))
### listSheet.Cells(row, 9).Value = len(elements)
###
### for element in elements:
###     listSheet.Cells(row, 10).Value = element.parent.parent.parent.contents[1].string
##
##
##
###
###
###
###
###
### obj = {'id':'nodeA','children':[
###            {'id':'nodeB','children':[
###                  {'id':'nodeD','children':[]},
###                  {'id':'nodeE','children':[]}
###            ]},
###            {'id':'nodeC','children':[]}
###       ]}
###
###
### obj1 = [['zxc', 'hfd'], ['gsdf', 'hggg']]
###
###
###
### def iterativeChildren(nodes):
### 	results = []
### 	while 1:
### 		newNodes = []
### 		if len(nodes) == 0:
### 			break
### 		for node in nodes:
### 			results.append(node['id'])
### 			if len(node['children']) > 0:
### 				for child in node['children']:
### 					newNodes.append(child)
### 		nodes = newNodes
### 	return results
###
###
### def iterativeChildren1(nodes):
###
###     results = []
###
###     while 1:
###
###         newNodes = []
###
###         if len(nodes) == 0:
###
###             break
###
### #        firstLevelNodeCounter = 0
###
###         for node in nodes:
###
###             results.append(node[0:2])
###  #           firstLevelNodeCounter = firstLevelNodeCounter + 1
###
###   #          secondLevelNodeCounter = 0
###
###             if isinstance(node, list) and len(node) > 0:
###
###                 for child in node:
###
###                     #results.append(node[0:2])
###                     newNodes.append(child[0:2])
###    #                 secondLevelNodeCounter = secondLevelNodeCounter + 1
###
###         break
###
###     return results
##
##
##
##
####
####
####
####def list_flatten(my_list):
####    for item in my_list:
####        if not isinstance(item, str):
####            try:
####                for i in item:
####                    myvar = i
####
####                row = 1
####
####                for i in range(1, 1000):
####                    if htmlDataSheet.Cells(i, 1).Value == None:
####                        row = i
####                        break
####
####                htmlDataSheet.Cells(row, 1).Value = str(item)
####
####                list_flatten(item)
####
####            except:
####
####                row = 1
####
####                for i in range(1, 1000):
####                    if htmlDataSheet.Cells(i, 1).Value == None:
####                        row = i
####                        break
####
####                htmlDataSheet.Cells(row, 1).Value = str(item)
####        else:
####
####            row = 1
####
####            for i in range(1, 1000):
####                if htmlDataSheet.Cells(i, 1).Value == None:
####                    row = i
####                    break
####
####            htmlDataSheet.Cells(row, 1).Value = str(item)
####
####
##
