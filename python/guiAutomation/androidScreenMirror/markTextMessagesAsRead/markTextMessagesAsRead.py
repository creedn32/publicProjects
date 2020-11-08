from pathlib import Path
import sys
pathToThisPythonFile = Path(__file__).resolve()
# sys.path.append(str(pathToThisPythonFile.parents[1]))
# from myPythonLibrary import myPyFunc
from pprint import pprint as p

import pyautogui
import time
pyautogui.PAUSE = 0


# print(pyautogui.position())


def performMouseActions():

    # pyautogui.displayMousePosition()

    # coordinatesOfTextMessage = [1056, 737]
    # coordinatesOfArchiveButton = [1056, 90]
    # pyautogui.mouseDown(x=coordinatesOfTextMessage[0], y=coordinatesOfTextMessage[1], button='left')
    # time.sleep(.75)
    # pyautogui.mouseUp(x=coordinatesOfTextMessage[0], y=coordinatesOfTextMessage[1], button='left')
    # pyautogui.click(coordinatesOfArchiveButton[0], coordinatesOfArchiveButton[1])
    # time.sleep(2)
    


    for iterationCount in range(500):

        startingDragPosition = [770, 740]
        endingDragPosition = [1200, 740]
        xDrag = endingDragPosition[0] - startingDragPosition[0]
        yDrag = endingDragPosition[1] - startingDragPosition[1]

        
        pyautogui.mouseDown(startingDragPosition[0], startingDragPosition[1])
        # time.sleep(.75)
        pyautogui.moveTo(endingDragPosition[0], endingDragPosition[1], duration=.2)
        pyautogui.mouseUp(endingDragPosition[0], endingDragPosition[1])
        # time.sleep(.1)
        pyautogui.moveTo(startingDragPosition[0], startingDragPosition[1])
        time.sleep(1)
        p(iterationCount)

        
        # pyautogui.moveTo(startingDragPosition[0], startingDragPosition[1])
        # # time.sleep(5)
        # # pyautogui.moveTo(endingDragPosition[0], endingDragPosition[1])
        # pyautogui.dragRel(xDrag, yDrag, duration=1)
        # time.sleep(2)


    # pyautogui.displayMousePosition()
    # pyautogui.moveTo(1056, 737, duration=0)
    # time.sleep(2)
    # pyautogui.moveTo(1056, 90, duration=0)


    # pyautogui.click(840, 40)
    # time.sleep(1)

    # for i in range(500):
    #     pyautogui.moveTo(740, 200, duration=0)
    #     pyautogui.dragRel(160, 0, duration=1)
    #     time.sleep(1)


def mainFunction(arrayOfArguments):
    performMouseActions()


if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
    p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')
