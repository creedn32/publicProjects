from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
import _myPyFunc

import subprocess, psutil
from runpy import run_path as runPath
from pprint import pprint as pp






def arrayOfProcesses():

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
  

    fileObj = open(Path(pathToRepos, 'privateData', 'python', 'shell', 'begin', 'runningProcesses.txt'), 'w')

    for line in processArray:
        fileObj.write(line + '\n')

    fileObj.close()


    return processArray




def processIsRunning(processToStart):
    def isValid(process):
        return process[3:] == processToStart \
         or process == processToStart  \
         or process[3:] == processToStart.replace('explorer ', '')
    
    return any(isValid(process) for process in arrayOfProcesses())



pathToThisPythonFileDirectory = pathToThisPythonFile.parents[0]
pathToRepos = _myPyFunc.getParentalDirectory(pathToThisPythonFile, 'repos')

currentMachine = runPath(str(_myPyFunc.replacePartOfPath(pathToThisPythonFileDirectory, 'publicProjects', 'privateData')) + '\\' + sys.argv[1] + '.py')


for processData in currentMachine.get('processesToStart'):
    
    processToStart = processData[0]

    if not processIsRunning(processToStart):
        pp('The process ' + processToStart + ' is not running and will be started.')
        
        if len(processData) > 1:
            processToStart = processData[1] + ' ' + processData[0]

        subprocess.Popen(processToStart)
    else:
        pp('The process ' + processToStart + ' is already running and will not be started.')

