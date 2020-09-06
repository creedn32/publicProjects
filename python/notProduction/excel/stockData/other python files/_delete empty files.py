

import bs4, re, os, win32com.client, sys

currentPage = "Statistics"
downloadedFolder = "\\" + currentPage + "\\"

for fileName in os.listdir(downloadedFolder):
        print(fileName.split("-")[1])
