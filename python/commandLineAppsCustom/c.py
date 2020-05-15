#local application imports
# from pathlib import Path
import sys
# pathToThisPythonFile = Path(__file__).resolve()
# sys.path.append(str(pathToThisPythonFile.parents[1]))
# import myPythonLibrary._myPyFunc as _myPyFunc

#standard library imports
# import datetime
from pprint import pprint as p
# import psutil
# from runpy import run_path
# import subprocess

#third-party imports
# import gspread

firstArgumentStr = sys.argv[1]

if '.' in firstArgumentStr:
    endingChar = firstArgumentStr.index('.')
else:
    endingChar = len(firstArgumentStr)

moduleToImport = firstArgumentStr[:endingChar]
# is equivalent to: from os import path as imported
importedModule = getattr(__import__('scriptsForCustom', fromlist=[moduleToImport]), moduleToImport)

argumentsArray = sys.argv[1].split('.') + sys.argv[2:]

importedModule.mainFunction(argumentsArray)




