import sys, pathlib
pathToAdd = str(pathlib.Path.cwd().parents[1])
sys.path.append(str(pathlib.Path.cwd().parents[1]))
from myPyLib import myPyFunc


splitTime = myPyFunc.printElapsedTime(False, "Starting code")
splitTime = myPyFunc.printElapsedTime(False, "A path was added that can now be imported from. Here is the path: " + pathToAdd)

import pyautogui, pynput.mouse, time
from pprint import pprint as pp

class mouseUpPositionClass:
    pass

mouseUpPositionObj = mouseUpPositionClass
mouseUpPositionObj.upXPosition = 0
mouseUpPositionObj.upYPosition = 0


# myPyFunc.printPythonInfo(mouseUpPositionObj, 50)

with pynput.mouse.Listener(on_click=myPyFunc.functionOnClick) as listenerObj:
    listenerObj.join()




# time.sleep(.5)
# pyautogui.click(840, 40)

splitTime = myPyFunc.printElapsedTime(False, "Code finished")