print("Importing modules, setting up variables, and setting up objects...")

import win32com.client, time, datetime, bs4, os, config
from selenium import webdriver



pageLoadTime = 15
chromeDriverCapabilities = webdriver.common.desired_capabilities.DesiredCapabilities.CHROME
chromeDriverCapabilities["pageLoadStrategy"] = "none"
chromeDriver = webdriver.Chrome(desired_capabilities=chromeDriverCapabilities)
chromeDriver.set_window_position(-1000, 0)
chromeDriver.maximize_window()

limits = [50, 500, 1000]

chromeDriver.get(config.website)
time.sleep(pageLoadTime)

chromeDriver.find_element_by_xpath("//*[@id=\"blogin\"]/li[2]/a").click()
time.sleep(pageLoadTime / 3)

chromeDriver.find_element_by_xpath("//*[@id=\"Email\"]").send_keys(config.username)
chromeDriver.find_element_by_xpath("//*[@id=\"Password\"]").send_keys(config.password)
chromeDriver.find_element_by_xpath("//*[@id=\"login\"]").click()
time.sleep(pageLoadTime)




