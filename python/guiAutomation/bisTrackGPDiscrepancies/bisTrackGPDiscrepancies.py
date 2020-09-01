from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[3], 'herokuGorilla', 'backend', 'python', 'myPythonLibrary')))
import _myPyFunc

import pyautogui as g
from pprint import pprint as p
import time
from tkinter import Tk as tk



for repetition in range(0, 1):

    _myPyFunc.clickImageAfterWaiting('accountsSearch.png')
    # _myPyFunc.getCoordinatesAfterWaiting('accountsWindow.png')

    # accountsWindowCoordinates = g.locateOnScreen('accountsWindow.png')
    # g.click(x=(accountsWindowCoordinates.left + accountsWindowCoordinates.width - 1), y=(accountsWindowCoordinates.top + accountsWindowCoordinates.height - 1))

    # g.press(['3', '0', '8', '0', '0', '1', '3', '0', '0', 'tab'])

    # _myPyFunc.getCoordinatesAfterWaiting('accountSearchComplete.png')

    # for downRepetition in range(0, repetition):
    #     time.sleep(.3)
    #     g.press(['down'])
    

    # g.press('enter')
    # _myPyFunc.getCoordinatesAfterWaiting('accountFound.png')
    

    # time.sleep(3)
    # if g.locateOnScreen('saveChanges.png'):
    #     p('saveChanges found.')
    #     g.hotkey('alt', 's')

    # _myPyFunc.waitUntilGone('saveChanges.png')

    # g.hotkey('ctrl', 'c')

    # g.press(['tab'] * 2)

    # inactivatedCoordinates = None

    # while not inactivatedCoordinates:
    #     g.press('space')
    #     time.sleep(2)
    #     p('Looking for inactivated box checked...')
    #     inactivatedCoordinates = g.locateCenterOnScreen('inactiveBoxInactivated.png')

    p(f'{repetition} is complete.')

