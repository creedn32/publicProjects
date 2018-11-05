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



pageLoadTime = 15
chromeDriverCapabilities = webdriver.common.desired_capabilities.DesiredCapabilities.CHROME
chromeDriverCapabilities["pageLoadStrategy"] = "none"
chromeDriver = webdriver.Chrome(desired_capabilities=chromeDriverCapabilities)
chromeDriver.set_window_position(1000, 0)
chromeDriver.maximize_window()
   
    
randomOrderList = list(range(6, stockListSheet.Cells(6, 1).End(win32com.client.constants.xlDown).Row + 1))
random.shuffle(randomOrderList)

    

for stockListSheetRow in randomOrderList:

    chromeDriver.get("https://finance.yahoo.com/")
    time.sleep(pageLoadTime)

    chromeDriver.find_element_by_name("p").clear()

    for eachChar in stockListSheet.Cells(stockListSheetRow, 1).Value:
        chromeDriver.find_element_by_name("p").send_keys(eachChar)
        time.sleep(1)
    
    #chromeDriver.find_element_by_name("p").send_keys(stockListSheet.Cells(row, 1).Value)
    time.sleep(pageLoadTime/6)
    chromeDriver.find_element_by_name("input").submit()
    time.sleep(pageLoadTime)
        
    currentPage = "Statistics"
    bsObj = bs4.BeautifulSoup(chromeDriver.page_source, "html.parser")

    for bsElem in bsObj(text=currentPage):
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

    print(xPathStr)

    for chromeDriverElem in chromeDriver.find_elements_by_xpath(xPathStr):
        print("selenium " + str(chromeDriverElem.get_attribute("outerHTML")))

        
    try:
        chromeDriver.execute_script("arguments[0].click();", chromeDriverElem)
        time.sleep(pageLoadTime + 5)

        
        downloadFilePath = filePath + "\\Downloaded HTML Files\\" + currentPage + "\\"
        downloadFileName = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "-" + stockListSheet.Cells(stockListSheetRow, 1).Value + "-from yahoo.html"            

        print(downloadFilePath + downloadFileName)
    
        with open(downloadFilePath + downloadFileName, "w") as fileWriteContainer:
            fileWriteContainer.write(chromeDriver.page_source)        
    
        print(stockListSheet.Cells(stockListSheetRow, 1).Value + " - Found " + currentPage + " link, clicked it, loaded page, and saved it to the hard drive.")


    except:
        print(stockListSheet.Cells(stockListSheetRow, 1).Value + " - Error in traversing the DOM looking for " + currentPage + ".")



    currentPage = "Income Statement"
    xPathStr = "//*[text()='" + currentPage + "']"
    chromeDriver.get("https://finance.yahoo.com/quote/" + stockListSheet.Cells(stockListSheetRow, 1).Value + "/financials?q=" + stockListSheet.Cells(stockListSheetRow, 1).Value)
    time.sleep(pageLoadTime)

    
    for element in chromeDriver.find_elements_by_xpath(xPathStr):
        try:
            element.click()
            time.sleep(pageLoadTime)

            downloadFilePath = filePath + "\\Downloaded HTML Files\\" + currentPage + "s" + "\\"
            downloadFileName = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + "-" + stockListSheet.Cells(stockListSheetRow, 1).Value + "-from yahoo.html"

            with open(downloadFilePath + downloadFileName, "w") as fileWriteContainer:
                fileWriteContainer.write(chromeDriver.page_source)

            print(stockListSheet.Cells(stockListSheetRow, 1).Value + " - Found " + currentPage + " link, clicked it, loaded page, and saved it to the hard drive.")

            break
                   
                    
        except:
            print(stockListSheet.Cells(stockListSheetRow, 1).Value + " - Error in traversing the DOM looking for " + currentPage + ".")



    currentPage = "Balance Sheet"
    xPathStr = "//*[text()='" + currentPage + "']"
    chromeDriver.get("https://finance.yahoo.com/quote/" + stockListSheet.Cells(stockListSheetRow, 1).Value + "/financials?q=" + stockListSheet.Cells(stockListSheetRow, 1).Value)
    time.sleep(pageLoadTime)




    for element in chromeDriver.find_elements_by_xpath(xPathStr):
        try:
            element.click()
            time.sleep(pageLoadTime)

            downloadFilePath = filePath + "\\Downloaded HTML Files\\" + currentPage + "s" + "\\"
            downloadFileName = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "-" + stockListSheet.Cells(stockListSheetRow, 1).Value + "-from yahoo.html"

            with open(downloadFilePath + downloadFileName, "w") as fileWriteContainer:
                fileWriteContainer.write(chromeDriver.page_source)

            print(stockListSheet.Cells(stockListSheetRow, 1).Value + " - Found " + currentPage + " link, clicked it, loaded page, and saved it to the hard drive.")

            break
                   
                    
        except:
            print(stockListSheet.Cells(stockListSheetRow, 1).Value + " - Error in traversing the DOM looking for " + currentPage + ".")


