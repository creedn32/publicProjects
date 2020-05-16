import bs4, os, shutil

currentPage = "Balance Sheets"
filesToRename = []

for fileNameOld in os.listdir(filePath):
        currentHTMLFile = open(filePath + fileNameOld)
        beautifulSoupObject = bs4.BeautifulSoup(currentHTMLFile, "html.parser")

        #print(fileNameOld.split("-")[1] + " = " + beautifulSoupObject.find("title").contents[0].split(" ")[0])

        if fileNameOld.split("-")[1] != beautifulSoupObject.find("title").contents[0].split(" ")[0]:
                fileNameNew = fileNameOld.replace("-" + fileNameOld.split("-")[1] + "-", "-" + beautifulSoupObject.find("title").contents[0].split(" ")[0] + "-")
                #print(fileNameOld)
                #print(fileNameNew)
                filesToRename.append([filePath + fileNameOld, filePath + fileNameNew])
                

for f in filesToRename:
        print(f)
        #shutil.move(f[0], f[1])







                
##        try:
##                os.rename(f[0], f[1])
##        except WindowsError:
##                os.remove(f[1])
##                os.rename(f[0], f[1])   
               
        


