from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[3], 'herokuGorilla', 'backend', 'python', 'myPythonLibrary')))
import _myPyFunc

import pyautogui as g
from pprint import pprint as p
import time
import pandas as pd
import pynput


daterange = pd.date_range('7/26/20', '8/9/20')

for single_date in daterange:
    print (single_date.strftime('%m/%d/%Y'))

    with pynput.mouse.Listener(on_click=_myPyFunc.functionOnClick) as listenerObj:
        print("Click on 'Clear' to begin...")
        listenerObj.join()
    
    # locatedBoxFrom = g.locateOnScreen('gpHATB.png')
    # g.moveTo(locatedBoxFrom.left + 40, locatedBoxFrom.top + 10)
    # g.click()

    # g.press(['delete']*10)
    # g.write('01/01/' + str(year))
    # g.press('tab')
    # g.write('12/31/' + str(year))
    # g.press('tab')

    # time.sleep(1)
    # locatedBoxNetCashFlow = g.locateOnScreen('quickBooksNoCashFlow.png')

    # if locatedBoxNetCashFlow:
    #     p('There are no cash flows')
    # else: 
    #     p('There are cash flows')
    #     g.hotkey('alt', 'x')
    #     g.press('n')
    #     time.sleep(1)
    #     g.hotkey('alt', 'x')
    #     time.sleep(5)
    #     # g.press['alt', 'f', exce]



    break