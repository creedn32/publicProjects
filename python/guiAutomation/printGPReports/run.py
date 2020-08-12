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

startTime = time.time()

pandasDateRange = pd.date_range('7/31/20', '8/9/20')
p(type(pandasDateRange))

if _myPyFunc.numLockIsOff():
    g.press('numlock')


for singleDate in pandasDateRange:
    p(singleDate.strftime('%m/%d/%Y'))

    gpClearCoordinates = None

    while not gpClearCoordinates:
        gpClearCoordinates = g.locateCenterOnScreen('gpClear.png', confidence=.9)

    g.click(gpClearCoordinates)    

    _myPyFunc.typeCharactersOnRemoteDesktop('Summary', g.PAUSE, pause=.5)
    g.press(['tab']*4)
    g.press(['down', 'up', 'up', 'up'])
    g.write(singleDate.strftime('%m/%d/%Y'))
    g.press(['tab']*20)
    g.press(['enter'])

    while not g.locateOnScreen('gpReportDestination.png'):
        pass
    
    g.press('enter')


    gpHATBScreenOutputPrintCoordinates = None

    while not gpHATBScreenOutputPrintCoordinates:
        gpHATBScreenOutputPrintCoordinates = g.locateCenterOnScreen('gpHATBScreenOutput.png')

    g.click(gpHATBScreenOutputPrintCoordinates)

    while not g.locateOnScreen('gpPrint.png'):
        pass

    g.press(['c', 'u', 'enter'])
    
    while not g.locateOnScreen('gpSaveAs.png'):
        pass
    
    g.press(['tab']*5)

    _myPyFunc.typeCharactersOnRemoteDesktop('Y:\\GL Reconciliations\\GP Reports - Historical Aged Trial Balance\\' + singleDate.strftime('%Y%m%d'), g.PAUSE
    )

    g.press('enter')
    g.hotkey('alt', 'f4')

    _myPyFunc.printElapsedTime(startTime, 'Saved Historical Aged Trial Balance dated ' + singleDate.strftime('%m/%d/%Y') + '.')
    # break

if not _myPyFunc.numLockIsOff():
    g.press('numlock')


