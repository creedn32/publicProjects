import win32com.client, time, datetime, bs4
from selenium import webdriver
#from selenium.webdriver.common.by import By
 
#excelApp = win32com.client.gencache.EnsureDispatch('Excel.Application')
#filePath = 
#fileName = "Monthly Purchase Process.xlsx"
#excelApp.Workbooks.Open(filePath + fileName)
##excelApp.Visible = True
##stockWb = excelApp.Workbooks(fileName)
## 
## 
##mainSheet = stockWb.Worksheets[1]
## 
##for sheet in stockWb.Worksheets:
##    if sheet.Name > mainSheet.Name and sheet.Visible == -1:
##        mainSheet = sheet
 
 
pageLoadTime = 15
capabilities = webdriver.common.desired_capabilities.DesiredCapabilities.CHROME
capabilities["pageLoadStrategy"] = "none"
driver = webdriver.Chrome(desired_capabilities=capabilities)
#driver.set_window_position(1000, 0)
driver.maximize_window()
 
 
 
row = 6
 
while mainSheet.Cells(row, 1).Value:
 
    driver.get("https://finance.yahoo.com/")
    time.sleep(pageLoadTime)
 
    driver.find_element_by_name("p").clear()
    driver.find_element_by_name("p").send_keys(mainSheet.Cells(row, 1).Value)
    time.sleep(pageLoadTime/7)
    driver.find_element_by_name("input").submit()
    time.sleep(pageLoadTime)
         
    currentPage = "Statistics"
    bsObj = bs4.BeautifulSoup(driver.page_source, "html.parser")
 
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
 
    for driverElem in driver.find_elements_by_xpath(xPathStr):
        print("selenium " + str(driverElem.get_attribute('outerHTML')))
 
         
    try:
        driver.execute_script("arguments[0].click();", driverElem)
        time.sleep(pageLoadTime)
 
         
        downloadFilePath = "C:\\"
        downloadFileName = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + "-" + mainSheet.Cells(row, 1).Value + "-from yahoo.html"           
 
        print(downloadFilePath + downloadFileName)
     
        with open(downloadFilePath + downloadFileName, "w") as fileWriteContainer:
            fileWriteContainer.write(driver.page_source)        
     
        print(mainSheet.Cells(row, 1).Value + " - Found " + currentPage + " link, clicked it, loaded page, and saved it to the hard drive.")
 
 
    except:
        print(mainSheet.Cells(row, 1).Value + " - Error in traversing the DOM looking for " + currentPage + ".")
 
 
 
    currentPage = "Income Statement"
    xPathStr = "//*[text()='" + currentPage + "']"
    driver.get("https://finance.yahoo.com/quote/" + mainSheet.Cells(row, 1).Value + "/financials?q=" + mainSheet.Cells(row, 1).Value)
    time.sleep(pageLoadTime)
 
     
    for element in driver.find_elements_by_xpath(xPathStr):
        try:
            element.click()
            time.sleep(pageLoadTime)
 
            downloadFilePath = "C:\\" + currentPage + "s" + "\\"
            downloadFileName = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + "-" + mainSheet.Cells(row, 1).Value + "-from yahoo.html"
 
            with open(downloadFilePath + downloadFileName, "w") as fileWriteContainer:
                fileWriteContainer.write(driver.page_source)
 
            print(mainSheet.Cells(row, 1).Value + " - Found " + currentPage + " link, clicked it, loaded page, and saved it to the hard drive.")
 
            break
                    
                     
        except:
            print(mainSheet.Cells(row, 1).Value + " - Error in traversing the DOM looking for " + currentPage + ".")
 
 
 
    currentPage = "Balance Sheet"
    xPathStr = "//*[text()='" + currentPage + "']"
    driver.get("https://finance.yahoo.com/quote/" + mainSheet.Cells(row, 1).Value + "/financials?q=" + mainSheet.Cells(row, 1).Value)
    time.sleep(pageLoadTime)
 
 
 
     
    for element in driver.find_elements_by_xpath(xPathStr):
        try:
            element.click()
            time.sleep(pageLoadTime)
 
            downloadFilePath = "C:\\" + currentPage + "s" + "\\"
            downloadFileName = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + "-" + mainSheet.Cells(row, 1).Value + "-from yahoo.html"
 
            with open(downloadFilePath + downloadFileName, "w") as fileWriteContainer:
                fileWriteContainer.write(driver.page_source)
 
            print(mainSheet.Cells(row, 1).Value + " - Found " + currentPage + " link, clicked it, loaded page, and saved it to the hard drive.")
 
            break
                    
                     
        except:
            print(mainSheet.Cells(row, 1).Value + " - Error in traversing the DOM looking for " + currentPage + ".")
 
 
    row = row + 1
 
 
 
 
