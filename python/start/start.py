#local application imports
from pathlib import Path
import sys
pathToThisPythonFile = Path(__file__).resolve()
# print(pathToThisPythonFile)
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'herokuGorilla', 'backend', 'python')))
import myPythonLibrary.myPyFunc as myPyFunc
import googleSheetsApps.processIsNotRunning as processIsNotRunning

#standard library imports
from pprint import pprint as p
from runpy import run_path
import subprocess



def mainFunction(arrayOfArguments):

    pathToProcessCollectionsToStart = Path(myPyFunc.replacePartOfPath(pathToThisPythonFile.parents[0], 'publicProjects', 'privateData'), 'processCollectionsToStart.py')
    importedProcessCollectionsToStart = run_path(str(pathToProcessCollectionsToStart))
    processCollectionsToStartObj = importedProcessCollectionsToStart.get('processCollectionsToStartObj')
    processCollectionToStart = processCollectionsToStartObj[arrayOfArguments[1]]

    for machineLocation, pathToRoot in importedProcessCollectionsToStart.get('pathToRoot').items():
        if pathToRoot in str(pathToThisPythonFile):
            pathToRootOnThisMachine = pathToRoot


    for processToStart in processCollectionToStart:

        replacedProcessToStart = processToStart.replace('!root!', pathToRootOnThisMachine)
        arrayOfArguments[1] = replacedProcessToStart

        if len(arrayOfArguments) < 3:
            arrayOfArguments.append('dontOutputToGoogleSheets')
        
        if processIsNotRunning.mainFunction(arrayOfArguments):
            p('Starting the process...')
            subprocess.Popen(replacedProcessToStart)


if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
	p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')


