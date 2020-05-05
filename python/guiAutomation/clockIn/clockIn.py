from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
import _myPyFunc

import pyautogui as g
import time as t
from pprint import pprint as p

g.PAUSE = 1

g.click()
g.typewrite('1234')
g.moveRel(170, 125, .1)
g.click()
g.press('enter')
