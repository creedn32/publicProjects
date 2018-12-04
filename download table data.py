print("Importing modules, setting up variables, and setting up objects...")

import time, datetime, os, config, sys, random
from selenium import webdriver

def downloadFullPath(limit):
    return os.path.abspath("..") + "\\Stock_Data_Data\\Table HTML Files\\" + str(limit) + "M" + "-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".html"

limitsList = []

for i in range(50, 1050, 50):
    limitsList.append(i)

random.shuffle(limitsList)

# for x in limitsList:
#     print(x)

#sys.exit()


pageLoadTime = 15
chromeDriverCapabilities = webdriver.common.desired_capabilities.DesiredCapabilities.CHROME
chromeDriverCapabilities["pageLoadStrategy"] = "none"
chromeDriver = webdriver.Chrome(desired_capabilities=chromeDriverCapabilities)
chromeDriver.set_window_position(-1000, 0)
chromeDriver.maximize_window()

chromeDriver.get(config.website)
time.sleep(pageLoadTime)

chromeDriver.find_element_by_xpath("//*[@id=\"blogin\"]/li[2]/a").click()
time.sleep(pageLoadTime / 3)

chromeDriver.find_element_by_xpath("//*[@id=\"Email\"]").send_keys(config.username)
chromeDriver.find_element_by_xpath("//*[@id=\"Password\"]").send_keys(config.password)
chromeDriver.find_element_by_xpath("//*[@id=\"login\"]").click()
time.sleep(pageLoadTime)


for i in limitsList:
    print(i)
    chromeDriver.find_element_by_xpath("//*[@id=\"MinimumMarketCap\"]").clear()
    chromeDriver.find_element_by_xpath("//*[@id=\"MinimumMarketCap\"]").send_keys(i)
    chromeDriver.find_element_by_xpath("//*[@id=\"Select30\"][@value=\"false\"]").click()
    chromeDriver.find_element_by_xpath("//*[@id=\"stocks\"]").click()
    time.sleep(pageLoadTime)

    with open(downloadFullPath(i), "w") as fileWriteContainer:
        fileWriteContainer.write(chromeDriver.page_source)

