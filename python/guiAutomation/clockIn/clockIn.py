from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
import _myPyFunc

import pyautogui as g
import time as t
import json as j
from pprint import pprint as p

pathToRepos = _myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')
pathToJSON = Path(pathToRepos, 'privateData', 'all', 'forImport.json')

importedData = j.load(open(pathToJSON))

g.PAUSE = 1

g.click()
g.typewrite(importedData['lastFour'])
g.moveRel(170, 125, .1)
g.click()
g.press('enter')