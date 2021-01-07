from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(pathToThisPythonFile.parents[4]))
from herokuGorilla.backend.python.myPythonLibrary import myPyFunc
from herokuGorilla.backend.python.myPythonLibrary import myPyAutoGui
from herokuGorilla.backend.python.googleSheets.myGoogleSheetsLibrary import myGspreadFunc

from pprint import pprint as p
import pyautogui as g
import time

def mainFunction(arrayOfArguments):

    time.sleep(5)

    # g.click()
    # g.moveRel(50, 50)
    
    for i in range(0, 10000):
        g.press('space')
        g.press('down')


if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
    p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')