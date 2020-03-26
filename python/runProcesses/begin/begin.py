from pathlib import Path
import sys
from runpy import run_path as runPath



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


    # pp(processArray)


    return processArray




def processIsRunning(processToStart):


    for runningProcess in arrayOfProcesses():

        if runningProcess[3:] == processToStart or runningProcess == processToStart or runningProcess.replace('explorer ', '') == runningProcess:
            pp('The process ' + processToStart + ' is already running and will not be started.')
            return True

    pp('The process ' + processToStart + ' is not already running and will now be started.')
    return False





thisPythonFilePath = Path(__file__).resolve()
pathToPublicProjectsPython = thisPythonFilePath.parents[2]
pathToRepos = pathToPublicProjectsPython.parents[1]


import json, subprocess, sys, psutil
from pprint import pprint as pp


pathToPythonDataFile = Path(pathToRepos, 'privateData', 'python', 'begin', sys.argv[1] + '.py')
currentMachine = runPath(pathToPythonDataFile)
thisPythonFileStem = thisPythonFilePath.stem



for processToStart in currentMachine.get('processesToStart'):
    if not processIsRunning(processToStart):
        subprocess.Popen(processToStart)



    





