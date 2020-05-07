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

    arrayOfRunningProcesses = [['Process ID', 'Execution Module', 'Current Directory', 'Name', 'Exe']]
    arrayOfRunningProcessesForTxt = []

    for runningProcess in psutil.process_iter():
            
        arrayOfRunningProcessesForTxt.append('-' * 30)

        processToAppend = []
        processToAppend.append(runningProcess.pid)

        arrayOfRunningProcessesForTxt.append(f'{runningProcess.pid} (process ID)')

        try:

            arrayOfRunningProcessesForTxt.append(f'{runningProcess.exe()} (execution module)')
            
            for i in range(0, len(runningProcess.cmdline())):
                arrayOfRunningProcessesForTxt.append(str(i) + ': ' + runningProcess.cmdline()[i])

            arrayOfRunningProcessesForTxt.append(f'{runningProcess.cwd()} (current directory)')
            arrayOfRunningProcessesForTxt.append(f'{runningProcess.name()} (name)')
            arrayOfRunningProcessesForTxt.append(f'{runningProcess.exe()} (exe)')

        except psutil.AccessDenied:
            pass
            arrayOfRunningProcessesForTxt.append('You do not have access to this process')




        try:
            processToAppend.append(runningProcess.exe())
        except psutil.AccessDenied:
            processToAppend.append('')
            
            # for i in range(0, len(runningProcess.cmdline())):
                # arrayOfRunningProcessesForTxt.append(str(i) + ': ' + runningProcess.cmdline()[i])

        try:
            processToAppend.append(runningProcess.cwd())
        except psutil.AccessDenied:
            processToAppend.append('')

        try:
            processToAppend.append(runningProcess.name())           
        except psutil.AccessDenied:
            processToAppend.append('')

        try:
            processToAppend.append(runningProcess.exe())
        except psutil.AccessDenied:
            processToAppend.append('')


        arrayOfRunningProcesses.append(processToAppend)
  
    # p(arrayOfRunningProcessesForTxt)


    fileObj = open(Path(pathToSaveProcesses, 'runningProcesses.txt'), 'w')

    for line in arrayOfRunningProcessesForTxt:
        fileObj.write(line + '\n')

    fileObj.close()


    # p(arrayOfRunningProcesses[0:4])
    _myGspreadFunc.updateCells(gspCurrentlyRunningProcessesSheet, arrayOfRunningProcesses)

    return arrayOfRunningProcessesForTxt




def processIsRunning(processToStart, pathToSaveProcesses):

    def isValid(process):
        return process[3:] == processToStart \
         or process == processToStart  \
         or process[3:] == processToStart.replace('explorer ', '')
    
    return any(isValid(process) for process in getArrayOfProcesses(pathToSaveProcesses))


gspSpreadsheet = _myGspreadFunc.getGspSpreadsheetObj('Computer Processes')

gspCurrentlyRunningProcessesSheet = gspSpreadsheet.worksheet('currentlyRunningProcesses')
gspAppCollectionsToStartSheet = gspSpreadsheet.worksheet('appCollectionsToStart')

appCollectionsToStartArrayFromSheet = gspAppCollectionsToStartSheet.get_all_values()
_myGspreadFunc.clearAndResizeSheets([gspCurrentlyRunningProcessesSheet])


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

