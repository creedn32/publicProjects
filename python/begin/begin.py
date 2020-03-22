from pathlib import Path
import sys

thisPythonFilePath = Path(__file__).resolve()
pathToPublicProjectsPython = thisPythonFilePath.parents[1]
# sys.path.append(str(pathToPublicProjectsPython))

import json, subprocess, sys, psutil
from pprint import pprint as pp


currentMachine = sys.argv[1]
thisPythonFileStem = thisPythonFilePath.stem
jsonPath = str(thisPythonFilePath).replace('publicProjects', 'privateData').replace('.py', '.' + currentMachine + '.json') # + thisPythonFileStem + currentMachine + '.json')


with open(jsonPath, 'r') as filePathObj:
    fileObj = json.load(filePathObj)


for process in fileObj['processesToStart']:
    if process != '':
        # subprocess.Popen(process)
        pass


# pathToGoogleCredentials = Path(pathToPublicProjectsPython.parents[1], 'privateData', 'python', 'googleCredentials')


for proc in psutil.process_iter ():
    # print ('-' * 30)
    # print (f'process ID: {proc.pid} ')
    try:

        # print (f'execution module: {proc.exe ()} ')
        
        if len(proc.cmdline()) > 1:
            pp(proc.cmdline()[0])
            pp(proc.cmdline()[1])
        
        # print (f'current directory: {proc.cwd ()} ')
    except psutil.AccessDenied:
        print ('(You do not have access to this process)')


# for process in psutil.process_iter():
    # pass
    # pp(process.name())
    # pp(process.exe())
    # pp(process.cmdline())