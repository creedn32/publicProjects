from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
# sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
# import _myPyFunc

import pyautogui as g
from pprint import pprint as p
import time
import pywin32

for year in range(2010, 2011):

    locatedBoxFrom = g.locateOnScreen('quickBooksFrom.png')
    g.moveTo(locatedBoxFrom.left + 40, locatedBoxFrom.top + 10)
    g.click()

    g.press(['delete']*10)
    g.write('01/01/' + str(year))
    g.press('tab')
    g.write('12/31/' + str(year))
    g.press('tab')

    time.sleep(1)
    locatedBoxNetCashFlow = g.locateOnScreen('quickBooksNoCashFlow.png')

    if locatedBoxNetCashFlow:
        p('There are no cash flows')
    else: 
        p('There are cash flows')
        g.hotkey('alt', 'x')
        g.press('n')
        time.sleep(1)
        g.hotkey('alt', 'x')
        time.sleep(5)
        g.press['alt', 'f', exce]

