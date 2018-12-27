print("Importing modules, setting up variables, and setting up objects...")

import time, datetime, os, sys, random, json
from selenium import webdriver

# with open(os.path.abspath("..") + "\\private_data\\stock_data\\config.json", "w") as outfile:
#     json.dump(data, outfile, sort_keys=True, indent=4)
#     # sort_keys, indent are optional and used for pretty-write

with open(os.path.abspath("..") + "\\private_data\\stock_data\\config.json") as dataFile:
    data = json.load(dataFile)


def downloadFullPath(limit):
    return os.path.abspath("..") + "\\private_data\\stock_data\\table html files\\" + str(limit) + "M" + "-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".html"

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

chromeDriver.get(data["website"])
time.sleep(pageLoadTime)

chromeDriver.find_element_by_xpath("//*[@id=\"blogin\"]/li[2]/a").click()
time.sleep(pageLoadTime / 3)

chromeDriver.find_element_by_xpath("//*[@id=\"Email\"]").send_keys(data["username"])
chromeDriver.find_element_by_xpath("//*[@id=\"Password\"]").send_keys(data["password"])
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
        fileWriteContainer.write(str(chromeDriver.page_source.encode('utf-8')))

