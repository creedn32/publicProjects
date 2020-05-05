from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
import _myPyFunc

import pyautogui as g
import time as t
from pprint import pprint as p

g.click()
t.sleep(.2)
g.typewrite('1234')
t.sleep(.2)
g.moveRel(170, 125, .1)
t.sleep(.2)
g.click()
t.sleep(.2)
g.press('enter')
# pyautogui.moveRel(80, 0, .1)
