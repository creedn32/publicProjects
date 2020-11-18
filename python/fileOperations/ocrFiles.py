from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(pathToThisPythonFile.parents[2]))
from herokuGorilla.backend.python.myPythonLibrary import myPyFunc

from pprint import pprint as p


def ocrFiles(arrayOfArguments):

    def printCurrentFile(dataForActionObj):
        
        if dataForActionObj['currentFileObj'].is_file() and dataForActionObj['currentFileObj'].suffix == '.pdf':
            p(str(dataForActionObj['currentFileObj']))
        return dataForActionObj

    myPyFunc.onAllFileObjInTreeBreadthFirst(Path(arrayOfArguments[1]), printCurrentFile)



def mainFunction(arrayOfArguments):

    ocrFiles(arrayOfArguments)


if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
    p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')