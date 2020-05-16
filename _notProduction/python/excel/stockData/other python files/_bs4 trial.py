import bs4, re

currentPage = "Income Statements"
downloadedFolder = "" + currentPage + "\\"

currentHTMLFile = open(downloadedFolder + "20180911110000-FTSI-from yahoo.html")
bSoupObj = bs4.BeautifulSoup(currentHTMLFile, "html.parser")
for script in bSoupObj(["script", "style"]):
    script.decompose()

elements = bSoupObj.findAll(text="Net Income") #> tbody > tr > td > span

for element in elements:
    if "Fz(15px)" not in str(element.parent.parent):
        print(element.parent.parent)
