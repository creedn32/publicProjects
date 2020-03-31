from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(Path(pathToThisPythonFile.parents[1]))

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

pathToRepos = pathToThisPythonFile.parents[3]
currentMachine = runPath(str(Path(pathToRepos, 'privateData', 'python', 'shell', 'begin', sys.argv[1] + '.py')))


for processData in currentMachine.get('processesToStart'):
    
    processToStart = processData[0]

    if not processIsRunning(processToStart):
        pp('The process ' + processToStart + ' is not running and will be started.')
        
        if len(processData) > 1:
            processToStart = processData[1] + ' ' + processData[0]

        subprocess.Popen(processToStart)
    else:
        pp('The process ' + processToStart + ' is already running and will not be started.')

