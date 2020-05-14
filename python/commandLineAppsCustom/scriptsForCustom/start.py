#local application imports
from pathlib import Path
import sys
pathToThisPythonFile = Path(__file__).resolve()
sys.path.append(str(pathToThisPythonFile.parents[2]))
import myPythonLibrary._myPyFunc as _myPyFunc
import googleSheets.processIsNotRunning.processIsNotRunning as processIsNotRunning

#standard library imports
from pprint import pprint as p
from runpy import run_path
import subprocess


#try from commandline as well
#delete b.py


def mainFunction(arrayOfArguments):

    pathToProcessCollectionsToStart = Path(_myPyFunc.replacePartOfPath(pathToThisPythonFile.parents[0], 'publicProjects', 'privateData'), 'start', 'processCollectionsToStart.py')
    importedProcessCollectionsToStart = run_path(str(pathToProcessCollectionsToStart))
    processCollectionsToStartObj = importedProcessCollectionsToStart.get('processCollectionsToStartObj')
    processCollectionToStart = processCollectionsToStartObj[arrayOfArguments[0]][arrayOfArguments[1]]

    arrayOfArguments[0] = '{}.{}'.format(arrayOfArguments[0], arrayOfArguments[1])

    if len(arrayOfArguments) < 3:
        arrayOfArguments.append('dontOutputToGoogleSheets')

    for processToStart in processCollectionToStart:

        arrayOfArguments[1] = processToStart

        if processIsNotRunning.mainFunction(arrayOfArguments):
            p('Starting the process...')
            subprocess.Popen(processToStart)


if __name__ == "__main__":
    mainFunction(sys.argv)

