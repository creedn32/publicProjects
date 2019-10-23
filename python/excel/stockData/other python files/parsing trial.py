import bs4
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome()
driver.get("https://finance.yahoo.com/quote/OPHT?p=OPHT&.tsrc=fin-srch")

#currentHTMLFile = open("" + "\\OPHT 2.43 -0.06 -2.41% _ Ophthotech Corporation - Yahoo Finance.html", encoding="utf-8")
bsObj = bs4.BeautifulSoup(driver.page_source, "html.parser")
#bsObj = bs4.BeautifulSoup("<b class='hey there' id='yo'>Statistics</b>", "html.parser")



for bsElem in bsObj(text="Statistics"):
    bsParentElem = bsElem.parent
    #print("bs element parent: " + str(bsParentElem))
    #print("bs element parent attributes: " + str(parentElem.attrs))
    #print("bs element parent contents: " + str(parentElem.contents))
    #print("bs element parent name: " + str(parentElem.name))

xPathStr = "//" + bsParentElem.name + "[" + "contains(text(), '" + bsParentElem.contents[0] + "')"

for key, value in bsParentElem.attrs.items():
    if isinstance(value, (list, tuple)):
        for eachValue in value:
            xPathStr = xPathStr + " and " + "@" + key + "=" + eachValue
    else:
        xPathStr = xPathStr + " and " + "@" + key + "=" + value
    

xPathStr = xPathStr + "]"

print(xPathStr)


#time.sleep(15)

for driverElem in driver.find_elements_by_xpath(xPathStr):
    print("selenium " + str(driverElem.get_attribute('outerHTML')))

driver.execute_script("arguments[0].click();", driverElem)

