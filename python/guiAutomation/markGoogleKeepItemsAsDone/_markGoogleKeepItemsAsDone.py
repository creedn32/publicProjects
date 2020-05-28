import sys, pathlib
pathToAdd = str(pathlib.Path.cwd().parents[1])
sys.path.append(str(pathlib.Path.cwd().parents[1]))
from myPyLib import _myPyFunc


splitTime = _myPyFunc.printElapsedTime(False, "Starting code")
splitTime = _myPyFunc.printElapsedTime(False, "A path was added that can now be imported from. Here is the path: " + pathToAdd)

import pyautogui, pynput.mouse, time
from pprint import pprint as pp



def funcOnClick(x, y, button, pressed):
    if not pressed:
        mouseUpPositionObj.upXPosition = x
        mouseUpPositionObj.upYPosition = y

        print("Mouse {2} was {0} at {1}.".format("pressed" if pressed else "released", (x, y), button))
        return False


class mouseUpPositionClass:
    pass

mouseUpPositionObj = mouseUpPositionClass


splitTime = _myPyFunc.printElapsedTime(False, "Finished importing modules and setting up functions, classes, and objects")



with pynput.mouse.Listener(on_click=funcOnClick) as listenerObj:
    listenerObj.join()



for clickCount in range(0, 50):
    pyautogui.click(mouseUpPositionObj.upXPosition, mouseUpPositionObj.upYPosition)
    # time.sleep(.0000001)




splitTime = _myPyFunc.printElapsedTime(False, "Code finished")