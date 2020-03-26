from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(pathToThisPythonFile.parents[0])

import json, subprocess, psutil
from runpy import run_path as runPath
from pprint import pprint as pp






def arrayOfProcesses():

    processArray = []

    for proc in psutil.process_iter():
            
        processArray.append('-' * 30)
        processArray.append(f'{proc.pid} (process ID)')

        try:

            processArray.append(f'{proc.exe()} (execution module)')
            
            for i in range(0, len(proc.cmdline())):
                processArray.append(str(i) + ': ' + proc.cmdline()[i])

            processArray.append(f'{proc.cwd()} (current directory)')
            processArray.append(f'{proc.name()} (name)')
            processArray.append(f'{proc.exe()} (exe)')

        except psutil.AccessDenied:
            pass
            processArray.append('You do not have access to this process')
  

    fileObj = open(Path(pathToRepos, 'privateData', 'python', 'begin', 'runningProcesses.txt'), 'w')

    for line in processArray:
        fileObj.write(line + '\n')

    fileObj.close()


    return processArray




def processIsRunning(processToStart):

    for runningProcess in arrayOfProcesses():

        if runningProcess[3:] == processToStart or runningProcess == processToStart or runningProcess[3:] == processToStart.replace('explorer ', ''):
            
            return True

    return False




pathToRepos = pathToThisPythonFile.parents[4]
currentMachine = runPath(Path(pathToRepos, 'privateData', 'python', 'begin', sys.argv[1] + '.py'))


for processData in currentMachine.get('processesToStart'):
    processToStart = processData[0]
    if not processIsRunning(processToStart):
        pp('The process ' + processToStart + ' is not already running and will now be started.')
        subprocess.Popen(processToStart)
    else:
        pp('The process ' + processToStart + ' is already running and will not be started.')

