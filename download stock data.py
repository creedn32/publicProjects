print("Importing, setting up variables and object...")

import win32com.client, time, datetime, bs4, random, os #, sys
from selenium import webdriver
#from selenium.webdriver.common.by import By

filePath = os.path.abspath(os.curdir)
fileName = "Monthly Purchase Process"
fileExtension = ".xlsx"
excelApp = win32com.client.gencache.EnsureDispatch('Excel.Application')
excelApp.Workbooks.Open(filePath + "\\" + fileName + fileExtension)
excelApp.Visible = True

stockWb = excelApp.Workbooks(fileName + fileExtension)
stockListSheet = stockWb.Worksheets[1]

# find the last sheet

for sheet in stockWb.Worksheets:
    if sheet.Name > stockListSheet.Name and sheet.Visible == -1:
        stockListSheet = sheet


pageLoadTime = 10
chromeDriverCapabilities = webdriver.common.desired_capabilities.DesiredCapabilities.CHROME
chromeDriverCapabilities["pageLoadStrategy"] = "none"
chromeDriver = webdriver.Chrome(desired_capabilities=chromeDriverCapabilities)
chromeDriver.set_window_position(-1000, 0)
chromeDriver.maximize_window()
   
    
randomOrderList = list(range(6, stockListSheet.Cells(6, 1).End(win32com.client.constants.xlDown).Row + 1))
random.shuffle(randomOrderList)

currentPage = {0:
                    {"name": "Statistics",
                     "folderName": "Statistics"},
                1:
                    {"name": "Income Statement",
                     "folderName": "Income Statements"},
                2:
                    {"name": "Balance Sheet",
                     "folderName": "Balance Sheets"}
                }

print("Done")

for stockListSheetRow in randomOrderList:

    print("Open Yahoo! Finance...")    

    chromeDriver.get("https://finance.yahoo.com/")
    time.sleep(pageLoadTime)

    print("Loaded")

    print("Open stock page...")

    inputElement = chromeDriver.find_element_by_name("yfin-usr-qry")

    for eachChar in stockListSheet.Cells(stockListSheetRow, 1).Value:
        inputElement.send_keys(eachChar)
        time.sleep(1)
    
    time.sleep(pageLoadTime/6)
    inputElement.submit()
    time.sleep(pageLoadTime)

    print("Loaded")

    print("Create xPath...")
    

    bsObj = bs4.BeautifulSoup(chromeDriver.page_source, "html.parser")


    for bsElem in bsObj(text=currentPage[0]["name"]):
        bsParentElem = bsElem.parent
        print("bs element parent: " + str(bsParentElem.parent))
        print("bs element parent attributes: " + str(bsParentElem.attrs))
        print("bs element parent contents: " + str(bsParentElem.contents))
        print("bs element parent name: " + str(bsParentElem.name))


    xPathStr = "//" + bsParentElem.name + "[" + "text()='" + bsParentElem.contents[0] + "'"

    
    for key, value in bsParentElem.attrs.items():
        if isinstance(value, (list, tuple)):
            for eachValue in value:
                xPathStr = xPathStr + " and " + "@" + key + "=" + eachValue
        else:
            xPathStr = xPathStr + " and " + "@" + key + "=" + value
    

    xPathStr = xPathStr + "]"

    print("xPath is: " + xPathStr)

    print("Done")

    for chromeDriverElem in chromeDriver.find_elements_by_xpath(xPathStr):
        print("selenium " + str(chromeDriverElem.get_attribute("outerHTML")))

        
    try:
        chromeDriver.execute_script("arguments[0].click();", chromeDriverElem)
        time.sleep(pageLoadTime + 5)

        
        downloadFilePath = os.path.abspath("..") + "\\Stock_Data_Data\\Downloaded HTML Files\\" + currentPage[0]["folderName"] + "\\"
        downloadFileName = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "-" + stockListSheet.Cells(stockListSheetRow, 1).Value + "-from yahoo.html"            

        print(downloadFilePath + downloadFileName)
    
        with open(downloadFilePath + downloadFileName, "w") as fileWriteContainer:
            fileWriteContainer.write(chromeDriver.page_source)        
    
        print(stockListSheet.Cells(stockListSheetRow, 1).Value + " - Found " + currentPage[0]["name"] + " link, clicked it, loaded page, and saved it to the hard drive.")


    except:
        print(stockListSheet.Cells(stockListSheetRow, 1).Value + " - Error in traversing the DOM looking for " + currentPage[0]["name"] + ".")


    for i in range(1, 3):
        xPathStr = "//*[text()='" + currentPage[i]["name"] + "']"
        chromeDriver.get("https://finance.yahoo.com/quote/" + stockListSheet.Cells(stockListSheetRow, 1).Value + "/financials?q=" + stockListSheet.Cells(stockListSheetRow, 1).Value)
        time.sleep(pageLoadTime)


        for element in chromeDriver.find_elements_by_xpath(xPathStr):
            try:
                element.click()
                time.sleep(pageLoadTime)

                downloadFilePath = filePath + "\\Downloaded HTML Files\\" + currentPage[i]["folderName"] + "\\"
                downloadFileName = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + "-" + stockListSheet.Cells(stockListSheetRow, 1).Value + "-from yahoo.html"

                with open(downloadFilePath + downloadFileName, "w") as fileWriteContainer:
                    fileWriteContainer.write(chromeDriver.page_source)

                print(stockListSheet.Cells(stockListSheetRow, 1).Value + " - Found " + currentPage[i]["name"] + " link, clicked it, loaded page, and saved it to the hard drive.")

                break


            except:
                print(stockListSheet.Cells(stockListSheetRow, 1).Value + " - Error in traversing the DOM looking for " + currentPage[i]["name"] + ".")



    #currentPage = currentPage[2]
    #xPathStr = "//*[text()='" + currentPage + "']"
    #chromeDriver.get("https://finance.yahoo.com/quote/" + stockListSheet.Cells(stockListSheetRow, 1).Value + "/financials?q=" + stockListSheet.Cells(stockListSheetRow, 1).Value)
    #time.sleep(pageLoadTime)



    #
    # for element in chromeDriver.find_elements_by_xpath(xPathStr):
    #     try:
    #         element.click()
    #         time.sleep(pageLoadTime)
    #
    #         downloadFilePath = filePath + "\\Downloaded HTML Files\\" + currentPage + "s" + "\\"
    #         downloadFileName = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "-" + stockListSheet.Cells(stockListSheetRow, 1).Value + "-from yahoo.html"
    #
    #         with open(downloadFilePath + downloadFileName, "w") as fileWriteContainer:
    #             fileWriteContainer.write(chromeDriver.page_source)
    #
    #         print(stockListSheet.Cells(stockListSheetRow, 1).Value + " - Found " + currentPage + " link, clicked it, loaded page, and saved it to the hard drive.")
    #
    #         break
    #
    #
    #     except:
    #         print(stockListSheet.Cells(stockListSheetRow, 1).Value + " - Error in traversing the DOM looking for " + currentPage + ".")
    #
    #
