print("Importing modules, setting up variables, and setting up objects...")

cutOffDate = 20181206000000
cutOffDate = cutOffDate * 1000000

import win32com.client, time, datetime, bs4, random, os, sys
import selenium.webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

#binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox")


def downloadFullPath(downloadFolder, currStock):
    return os.path.abspath("..") + "\\private_data\\stock_data\\downloaded html files\\" + downloadFolder + "\\" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "-" + currStock + "-from yahoo.html"


filePath = os.path.abspath("..") + "\\private_data\\stock_data"
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

colNum = {"topRow": 6,
          "statDownDate": 7,
          "bsDownDate": 17,
          "isDownDate": 25,
          "ticker": 3}


#Proxy
#PROXY = "162.243.108.161:8080" # IP:PORT or HOST:PORT
#chromeOptions = webdriver.ChromeOptions()
#chromeOptions.add_argument('--proxy-server=http://%s' % PROXY)
#chrome = webdriver.Chrome(chrome_options=chrome_options)




#Chrome
selenDriverCapabilities = selenium.webdriver.common.desired_capabilities.DesiredCapabilities.CHROME
selenDriverCapabilities["pageLoadStrategy"] = "none"
selenDriver = selenium.webdriver.Chrome(desired_capabilities=selenDriverCapabilities) #, options=chromeOptions)




#Edge
#selenDriverCapabilities = selenium.webdriver.common.desired_capabilities.DesiredCapabilities.EDGE
#selenDriverCapabilities["pageLoadStrategy"] = "none"
#selenDriver = selenium.webdriver.Edge(capabilities=selenDriverCapabilities) #desired_capabilities=selenDriverCapabilities) #, executable_path="C:\\Users\\creed\\Computer\\Setup Files\\Portable Applications\\MicrosoftWebDriver.exe")  #(desired_capabilities=selenDriverCapabilities)
#selenDriver = selenium.webdriver.Edge() #(capabilities=selenDriverCapabilities)



#Window
selenDriver.set_window_position(-1000, 0)
selenDriver.maximize_window()


randomOrderList = []

for row in range(colNum["topRow"], stockListSheet.Cells(colNum["topRow"] - 1, 1).End(win32com.client.constants.xlDown).Row + 1):
    if "No" in [str(stockListSheet.Cells(row, colNum["statDownDate"]).Value)[:2], str(stockListSheet.Cells(row, colNum["bsDownDate"]).Value)[:2], str(stockListSheet.Cells(row, colNum["isDownDate"]).Value)[2:]] or int(stockListSheet.Cells(row, colNum["statDownDate"]).Value) < cutOffDate or int(stockListSheet.Cells(row, colNum["bsDownDate"]).Value) < cutOffDate or int(stockListSheet.Cells(row, colNum["isDownDate"]).Value) < cutOffDate:
        randomOrderList.append(row)
    row = row + 1


#randomOrderList = list(range(6, stockListSheet.Cells(6, 1).End(win32com.client.constants.xlDown).Row + 1))

random.shuffle(randomOrderList)

print("Done")

print("Navigate to Yahoo! Finance...")

selenDriver.get("https://finance.yahoo.com/")
print(1)
time.sleep(pageLoadTime)

print(randomOrderList)


for stockListSheetRow in randomOrderList:

    currentStock = stockListSheet.Cells(stockListSheetRow, colNum["ticker"]).Value
    print("Navigate to general stock page for " + currentStock + "...")

    inputElement = selenDriver.find_element_by_xpath("//*[@id=\"fin-srch-assist\"]/input")

    for eachChar in currentStock:
        inputElement.send_keys(eachChar)
        time.sleep(1)

    time.sleep(pageLoadTime / 6)
    inputElement.send_keys(Keys.RETURN)
    time.sleep(pageLoadTime)
    print("Done")

    for i in range(0, 3):

        currentPage = stockPages[i]["name"]
        xPathStr = ""

        if currentPage == "Statistics":

            print("Build xPath for " + currentPage + " link to click for " + currentStock + ". Will print out xPath when it has been built...")

            bsObj = bs4.BeautifulSoup(selenDriver.page_source, "html.parser")

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

                selenDriver.get("https://finance.yahoo.com/quote/" + currentStock + "/financials?q=" + currentStock)
                time.sleep(pageLoadTime)
                print("Done")

            print("Build xPath for " + currentPage + " link to click for " + currentStock + ". Will print out xPath when it has been built..")
            xPathStr = "//*[text()='" + currentPage + "']"

        print(currentPage + " xPath has been built for " + currentStock + ": " + xPathStr)
        print("Using xPath, find " + currentPage + " link on page...")

        for selenDriverElem in selenDriver.find_elements_by_xpath(xPathStr):
            print("Using xPath, this link was found: " + str(selenDriverElem.get_attribute("outerHTML")))
            print("Click on the link...")

            try:
                selenDriver.execute_script("arguments[0].click();", selenDriverElem)
                time.sleep(pageLoadTime + 5)



                with open(downloadFullPath(stockPages[i]["folderName"], currentStock), "w") as fileWriteContainer:
                    fileWriteContainer.write(str(selenDriver.page_source.encode('utf-8')))

                print(
                    "Clicked " + currentPage + " link for " + currentStock + ", loaded page, and saved it to the hard drive.")

                break

            except Exception as e:
                print("Tried clicking " + currentPage + " link, for " + currentStock + ", but there was an error. " + str(e))


