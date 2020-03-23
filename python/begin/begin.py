from pathlib import Path
import sys
from runpy import run_path as runPath


thisPythonFilePath = Path(__file__).resolve()
pathToPublicProjectsPython = thisPythonFilePath.parents[1]
pathToRepos = pathToPublicProjectsPython.parents[1]
# sys.path.append(str(pathToPublicProjectsPython))

import json, subprocess, sys, psutil
from pprint import pprint as pp


pathToPythonDataFile = Path(pathToRepos, 'privateData', 'python', 'begin', sys.argv[1] + '.py')
currentMachine = runPath(pathToPythonDataFile)
thisPythonFileStem = thisPythonFilePath.stem
# jsonPath = str(thisPythonFilePath).replace('publicProjects', 'privateData').replace('.py', '.' + currentMachine + '.json') # + thisPythonFileStem + currentMachine + '.json')


# with open(jsonPath, 'r') as filePathObj:
#     fileObj = json.load(filePathObj)


for process in currentMachine.get('processesToStart'):
    if process != '':
        # subprocess.Popen(process)
        pass


# pathToGoogleCredentials = Path(pathToPublicProjectsPython.parents[1], 'privateData', 'python', 'googleCredentials')


for proc in psutil.process_iter ():
    # print ('-' * 30)
    # print (f'process ID: {proc.pid} ')
    try:

        # print (f'execution module: {proc.exe ()} ')
        
        cmdLineDetailCount = 0

        for cmdLineDetail in proc.cmdline():
            if cmdLineDetailCount < 2:
                pass
                # print(str(cmdLineDetailCount) + ': ' + cmdLineDetail)
            cmdLineDetailCount += 1


        # if len(proc.cmdline()) > 1:
            # pp(proc.cmdline()[0])
            # pp(proc.cmdline()[1])
        
        # print (f'current directory: {proc.cwd ()} ')
    except psutil.AccessDenied:
        pass
        # print ('(You do not have access to this process)')


# for process in psutil.process_iter():
    # pass
    # pp(process.name())
    # pp(process.exe())
    # pp(process.cmdline())