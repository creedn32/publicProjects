#local application imports
from pathlib import Path
import sys
pathToThisPythonFile = Path(__file__).resolve()
sys.path.append(str(pathToThisPythonFile.parents[2]))
import myPythonLibrary._myPyFunc as _myPyFunc, googleSheets.myGoogleSheetsLibrary._myGoogleSheetsFunc as _myGoogleSheetsFunc, googleSheets.myGoogleSheetsLibrary._myGspreadFunc as _myGspreadFunc

#standard library imports
from pprint import pprint as p
import psutil
from runpy import run_path
import subprocess

#third-party imports
import gspread

# p(dir())


def getArrayOfProcesses(pathToSaveProcesses):

    arrayOfRunningProcesses = [['Name', 'Process ID', 'Exe', 'Current Directory', 'Execution Module', 'Command Line (0)']]

    for runningProcess in psutil.process_iter():
           
        processToAppend = [runningProcess.name()]
        processToAppend.append(runningProcess.pid)

        try:
            processToAppend.append(runningProcess.exe())
        except psutil.AccessDenied:
            processToAppend.append('')


        try:
            processToAppend.append(runningProcess.cwd())
        except psutil.AccessDenied:
            processToAppend.append('')

        try:
            for cmdLineOfProcess in runningProcess.cmdline():
                processToAppend.append(cmdLineOfProcess)
        except psutil.AccessDenied:
            pass

        arrayOfRunningProcesses.append(processToAppend)
  
    
    numberOfTotalColumns = max([len(i) for i in arrayOfRunningProcesses])

    for rowIndex, row in enumerate(arrayOfRunningProcesses):

        if len(row) < numberOfTotalColumns:

            numberOfColumnsToAdd = numberOfTotalColumns - len(row)

            if rowIndex == 0:

                for columnNumberToAdd in range(1, numberOfColumnsToAdd):
                    row.append('Command Line (' + str(columnNumberToAdd) + ')')

            else:
                row.extend([''] * numberOfColumnsToAdd)


    _myGspreadFunc.updateCells(objOfSheets['currentlyRunningProcesses']['sheetObj'], arrayOfRunningProcesses)

    return arrayOfRunningProcesses




def processIsRunning(processToStart, pathToSaveProcesses):

    for process in getArrayOfProcesses(pathToSaveProcesses):
        if processToStart in process:
            return True
    return False



objOfSheets = _myGspreadFunc.getObjOfSheets('Computer Processes')

clearAndResizeParameters = [{
    'sheetObj': objOfSheets['currentlyRunningProcesses']['sheetObj'],
    'resizeRows': 2,
    'resizeColumns': 6,
    'startingRowIndexToClear': 1
}]

_myGspreadFunc.clearAndResizeSheets(clearAndResizeParameters)


pathToThisPythonFileDirectoryPrivate = _myPyFunc.replacePartOfPath(pathToThisPythonFile.parents[0], 'publicProjects', 'privateData')
pathToAppCollectionsToStart = Path(pathToThisPythonFileDirectoryPrivate, 'appCollectionsToStart.py')
appCollectionsToStart = run_path(str(pathToAppCollectionsToStart))
argumentFromCommandLine = sys.argv[1]

# p(processesToStartFromFile)
appCollectionToStart = appCollectionsToStart.get(argumentFromCommandLine)
# p(appCollectionToStart)

for appToStart in appCollectionToStart:

    processToStart = appToStart[0]
    # p(processToStart)

    if not processIsRunning(processToStart, pathToThisPythonFileDirectoryPrivate):
        p('The process ' + processToStart + ' is not running and will be started.')
        
        if len(appToStart) > 1:
            processToStart = appToStart[1] + ' ' + processToStart

        subprocess.Popen(processToStart)
    else:
        p('The process ' + processToStart + ' is already running and will not be started.')

