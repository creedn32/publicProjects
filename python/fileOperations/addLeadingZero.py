from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
pathToAppend = Path(pathToThisPythonFile.parents[2], 'herokuGorilla', 'backend', 'python', 'myPythonLibrary')
sys.path.append(str(pathToAppend))
import _myPyFunc

from pprint import pprint as p
import os
import re


for fileObj in Path(sys.argv[1]).iterdir():
    # result = re.search('(.*-)(.*)(\..*)', fileObj.name)
    
    newFilePath = fileObj
    
    # if len(result.group(2)) == 1:
    #     newFilePath = str(fileObj.parents[0]) + result.group(1) + '0' + result.group(2) + result.group(3)
    #     p(str(fileObj.parents[0]) + result.group(1) + '0' + result.group(2) + result.group(3))
    
    if 'ytellingStorytelling' in fileObj.name:
        strToUse = str(fileObj.parents[0]) + '\\' + str(fileObj.name[8:])
        p(strToUse)
        # newFilePath = str(fileObj.parents[0]) + result.group(1) + '0' + result.group(2) + result.group(3)
        newFilePath = strToUse
        
    os.rename(str(fileObj), newFilePath)
    



