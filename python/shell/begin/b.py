from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
import _myPyFunc

import subprocess, psutil
from runpy import run_path
from pprint import pprint as p






def arrayOfProcesses(pathToSaveProcesses):

    processArray = []

    for runningProcess in psutil.process_iter():
            
        processArray.append('-' * 30)
        processArray.append(f'{runningProcess.pid} (process ID)')

        try:

            processArray.append(f'{runningProcess.exe()} (execution module)')
            
            for i in range(0, len(runningProcess.cmdline())):
                processArray.append(str(i) + ': ' + runningProcess.cmdline()[i])

            processArray.append(f'{runningProcess.cwd()} (current directory)')
            processArray.append(f'{runningProcess.name()} (name)')
            processArray.append(f'{runningProcess.exe()} (exe)')

        except psutil.AccessDenied:
            pass
            processArray.append('You do not have access to this process')
  

    fileObj = open(Path(pathToSaveProcesses, 'runningProcesses.txt'), 'w')

    for line in processArray:
        fileObj.write(line + '\n')

    fileObj.close()


    return processArray




def processIsRunning(processToStart, pathToSaveProcesses):
    def isValid(process):
        return process[3:] == processToStart \
         or process == processToStart  \
         or process[3:] == processToStart.replace('explorer ', '')
    
    return any(isValid(process) for process in arrayOfProcesses(pathToSaveProcesses))



pathToThisPythonFileDirectory = pathToThisPythonFile.parents[0]
pathToThisPythonFileDirectoryPrivate = _myPyFunc.replacePartOfPath(pathToThisPythonFileDirectory, 'publicProjects', 'privateData')
pathToProcessesToStartData = Path(pathToThisPythonFileDirectoryPrivate, 'processesToStartData.py')
processesToStartData = run_path(str(pathToProcessesToStartData))


arrayOfProcessesToStart = processesToStartData.get(sys.argv[1])

for processToStartData in arrayOfProcessesToStart:

    processToStart = processToStartData[0]

    if not processIsRunning(processToStart, pathToThisPythonFileDirectoryPrivate):
        p('The process ' + processToStart + ' is not running and will be started.')
        
        if len(processToStartData) > 1:
            processToStart = processToStartData[1] + ' ' + processToStartData[0]

        subprocess.Popen(processToStart)
    else:
        p('The process ' + processToStart + ' is already running and will not be started.')

