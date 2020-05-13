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
moduleToImport = firstArgumentStr[:firstArgumentStr.index('.')]
moduleToImportRelativePath = 'scriptsForCustom.' + moduleToImport
remainingFirstArgumentStr = firstArgumentStr[firstArgumentStr.index('.') + 1:]
remainingFirstArgumentArray = remainingFirstArgumentStr.split('.')
remainingArgumentsArray = remainingFirstArgumentArray + sys.argv[2:]

# is equivalent to: from os import path as imported
# importedModule = getattr(__import__(moduleToImportRelativePath, fromlist=[moduleToImport]), moduleToImport)



# moduleToImportRelativePath = "math"
# importedModule = __import__(moduleToImportRelativePath)
# method_to_call = getattr(importedModule, moduleToImport)
# result = method_to_call()

# p(result)
# p(importedModule.customgit.thisconstant)
# importedModule.main(remainingArgumentsArray)

from scriptsForCustom import customgit





