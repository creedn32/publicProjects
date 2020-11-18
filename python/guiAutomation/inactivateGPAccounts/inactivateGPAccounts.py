from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[3], 'herokuGorilla', 'backend', 'python', 'myPythonLibrary')))
import _myPyFunc

import pyautogui as g
from pprint import pprint as p
import time
from tkinter import Tk as tk



for repetition in range(0, 300):

    _myPyFunc.clickImageWhenAppears('accountsSearch.png')
    _myPyFunc.getCoordinatesWhenImageAppears('accountsWindow.png')

    accountsWindowCoordinates = g.locateOnScreen('accountsWindow.png')
    g.click(x=(accountsWindowCoordinates.left + accountsWindowCoordinates.width - 1), y=(accountsWindowCoordinates.top + accountsWindowCoordinates.height - 1))

    g.press(['3', '0', '8', '0', '0', '1', '3', '0', '0', 'tab'])

    _myPyFunc.getCoordinatesWhenImageAppears('accountSearchComplete.png')

    for downRepetition in range(0, repetition):
        time.sleep(.3)
        g.press(['down'])
    

    g.press('enter')
    _myPyFunc.getCoordinatesWhenImageAppears('accountFound.png')
    

    time.sleep(3)
    if g.locateOnScreen('saveChanges.png'):
        p('saveChanges found.')
        g.hotkey('alt', 's')

    _myPyFunc.waitUntilImageDisappears('saveChanges.png')

    g.hotkey('ctrl', 'c')

    g.press(['tab'] * 2)

    inactivatedCoordinates = None

    while not inactivatedCoordinates:
        g.press('space')
        time.sleep(2)
        p('Looking for inactivated box checked...')
        inactivatedCoordinates = g.locateCenterOnScreen('inactiveBoxInactivated.png')

    p(f'{repetition} is complete. Account description: ' + tk().clipboard_get())

