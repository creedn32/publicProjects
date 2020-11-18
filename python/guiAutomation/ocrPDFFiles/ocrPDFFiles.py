from pathlib import Path

import pyautogui
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(pathToThisPythonFile.parents[3]))
from herokuGorilla.backend.python.myPythonLibrary import myPyFunc
from herokuGorilla.backend.python.myPythonLibrary import myPyAutoGui

from pprint import pprint as p

def addFileToOCRList(dataForActionObj):
        
        if dataForActionObj['currentFileObj'].is_file() and dataForActionObj['currentFileObj'].suffix == '.pdf':

            myPyAutoGui.clickWhenLocalPNGAppears('addFilesButton', pathToThisPythonFile.parents[0])
            p('found add files button')

            pyautogui.press('f')
            myPyAutoGui.getCoordinatesWhenLocalPNGAppears('addFilesDialogBox', pathToThisPythonFile.parents[0])
            
            pyautogui.keyDown('shift')
            
            while not myPyAutoGui.getCoordinatesIfLocalPNGIsShowing('pathArrow', pathToThisPythonFile.parents[0]):
                pyautogui.press('tab')


            pyautogui.keyUp('shift')
        
            pyautogui.press('enter')
            pyautogui.write(str(dataForActionObj['currentFileObj'].parents[0]))
            pyautogui.press('enter')

            myPyAutoGui.getCoordinatesWhenLocalPNGAppears('folderBoxReady', pathToThisPythonFile.parents[0])

            while not myPyAutoGui.getCoordinatesIfLocalPNGIsShowing('filenameBoxReady', pathToThisPythonFile.parents[0], confidence=.95):
                pyautogui.press('tab')

            pyautogui.write(str(dataForActionObj['currentFileObj'].name))
            pyautogui.press('enter')
            myPyAutoGui.waitUntilLocalPNGDisappears('addFilesDialogBox', pathToThisPythonFile.parents[0])

        return dataForActionObj

def ocrPDFFiles(arrayOfArguments):

    def ifPDFFile(fileObj):

        if fileObj.is_file() and fileObj.suffix == '.pdf': return fileObj

        return False

    arrayOfPDFFiles = myPyFunc.getArrayOfFileObjInTreeBreadthFirst(Path(arrayOfArguments[1]), ifPDFFile)
    # p(arrayOfPDFFiles)

    # myPyAutoGui.clickWhenLocalPNGAppears('nextButtonBeginOCR', pathToThisPythonFile.parents[0])



def mainFunction(arrayOfArguments):

    ocrPDFFiles(arrayOfArguments)


if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
    p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')