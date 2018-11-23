print("Importing modules, setting up variables, and setting up objects...")

import win32com.client, time, datetime, bs4, random, os
from selenium import webdriver


def downloadFullPath(downloadFolder, currStock):
    return os.path.abspath("..") + "\\Stock_Data_Data\\Downloaded HTML Files\\" + downloadFolder + "\\" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "-" + currStock + "-from yahoo.html"


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
chromeDriver.set_window_position(-1000, 0)
chromeDriver.maximize_window()
   
    
randomOrderList = list(range(6, stockListSheet.Cells(6, 1).End(win32com.client.constants.xlDown).Row + 1))
random.shuffle(randomOrderList)

stockPages = {0:
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

print("Navigate to Yahoo! Finance...")

chromeDriver.get("https://finance.yahoo.com/")
# chromeDriver.get("https://www.google.com/")
time.sleep(pageLoadTime * 2)

print("Done")


for stockListSheetRow in randomOrderList:

    currentStock = stockListSheet.Cells(stockListSheetRow, 1).Value
    print("Navigate to general stock page for " + currentStock + "...")

    inputElement = chromeDriver.find_element_by_name("yfin-usr-qry")

    for eachChar in currentStock:
        inputElement.send_keys(eachChar)
        time.sleep(1)

    time.sleep(pageLoadTime / 6)
    inputElement.submit()
    time.sleep(pageLoadTime)
    print("Done")

    for i in range(0, 3):

        currentPage = stockPages[i]["name"]
        xPathStr = ""

        if currentPage == "Statistics":

            print("Build xPath for " + currentPage + " link to click for " + currentStock + ". Will print out xPath when it has been built..")

            bsObj = bs4.BeautifulSoup(chromeDriver.page_source, "html.parser")

            for bsElem in bsObj(text=currentPage):
                bsParentElem = bsElem.parent
                print(
                    "On the " + currentStock + " general stock page, an element was found for building xPath for " + currentPage + ", bs element parent: " + str(
                        bsParentElem.parent))
                print(
                    "On the " + currentStock + " general stock page, an element was found for building xPath for " + currentPage + ", bs element parent attributes: " + str(
                        bsParentElem.attrs))
                print(
                    "On the " + currentStock + " general stock page, an element was found for building xPath for " + currentPage + ", bs element parent contents: " + str(
                        bsParentElem.contents))
                print(
                    "On the " + currentStock + " general stock page, an element was found for building xPath for " + currentPage + ", bs element parent name: " + str(
                        bsParentElem.name))

            xPathStr = "//" + bsParentElem.name + "[" + "text()='" + bsParentElem.contents[0] + "'"

            for key, value in bsParentElem.attrs.items():
                if isinstance(value, (list, tuple)):
                    for eachValue in value:
                        xPathStr = xPathStr + " and " + "@" + key + "=" + eachValue
                else:
                    xPathStr = xPathStr + " and " + "@" + key + "=" + value

            xPathStr = xPathStr + "]"

            # xPathStr = "//*[text()='" + currentPage + "']"

        else:
            if currentPage == "Income Statement":
                print("Navigate to Financials page for " + currentStock + "...")

                chromeDriver.get("https://finance.yahoo.com/quote/" + currentStock + "/financials?q=" + currentStock)
                time.sleep(pageLoadTime)
                print("Done")

            print("Build xPath for " + currentPage + " link to click for " + currentStock + ". Will print out xPath when it has been built..")
            xPathStr = "//*[text()='" + currentPage + "']"

        print(currentPage + " xPath has been built for " + currentStock + ": " + xPathStr)
        print("Using xPath, find " + currentPage + " link on page...")

        for chromeDriverElem in chromeDriver.find_elements_by_xpath(xPathStr):
            print("Using xPath, this link was found: " + str(chromeDriverElem.get_attribute("outerHTML")))
            print("Click on the link...")

            try:
                chromeDriver.execute_script("arguments[0].click();", chromeDriverElem)
                time.sleep(pageLoadTime + 5)

                with open(downloadFullPath(stockPages[i]["folderName"], currentStock), "w") as fileWriteContainer:
                    fileWriteContainer.write(chromeDriver.page_source)

                print(
                    "Clicked " + currentPage + " link for " + currentStock + ", loaded page, and saved it to the hard drive.")

                break

            except:
                print("Tried clicking " + currentPage + " link, for " + currentStock + ", but there was an error.")


