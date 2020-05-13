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
functionToCall = firstArgumentStr[:firstArgumentStr.index('.')]
remainingFirstArgumentStr = firstArgumentStr[firstArgumentStr.index('.') + 1:]
remainingFirstArgumentArray = remainingFirstArgumentStr.split('.')
remainingArguments = remainingFirstArgumentArray + sys.argv[2:]


pythonFilesObj = {
    "git": "asdf"
}

p(pythonFilesObj[functionToCall])





