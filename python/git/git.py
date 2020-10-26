#local application imports
from pathlib import Path
import sys
pathToThisPythonFile = Path(__file__).resolve()
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'herokuGorilla', 'backend', 'python')))
import myPythonLibrary.myPyFunc as myPyFunc

#standard library imports
import datetime
from pprint import pprint as p
import psutil
from runpy import run_path
import subprocess
import os

#third-party imports
import gspread



def noGitIgnoreFileFound(gitFolder):

    for obj in gitFolder.glob('*'):

        if obj.name == '.gitignore':

            fileObj = open(obj, 'r+')

            for line in fileObj:

                # p(line)

                if '__pycache__' in line:
                
                    return False

            fileObj.write('\n__pycache__')
            fileObj.close()

            return False

    return True




def runGitProcesses(gitFolder, arrayOfArguments):

    p(str(gitFolder))

    if noGitIgnoreFileFound(gitFolder):
        fileObj = open(Path(gitFolder, '.gitignore'), 'w')
        fileObj.write('__pycache__')
        fileObj.close()


    if len(arrayOfArguments) > 2 and arrayOfArguments[2] in ['includeheroku', 'h']:
        runGitProcessOnHerokuRepos = True
    else:
        runGitProcessOnHerokuRepos = False

    if len(arrayOfArguments) > 3:
        commitMessage = arrayOfArguments[3]    
    else:
        nowObj = datetime.datetime.now()
        commitMessage = nowObj.strftime("%Y-%m-%d %H:%M") + ', added/committed/pushed using custom Python script'
    

    gitProcessToRun = arrayOfArguments[1]


    if gitProcessToRun in ['acp', 'addcommitpush']:
        subprocess.run('git -C ' + str(gitFolder) + ' add .')
        subprocess.run('git -C ' + str(gitFolder) + ' commit -m \"' + commitMessage + '\"')
        subprocess.run('git -C ' + str(gitFolder) + ' push')
        
        if gitFolder.name[:6] == 'heroku' and runGitProcessOnHerokuRepos:
            subprocess.run('git -C ' + str(gitFolder) + ' push heroku master')

    else:
        subprocess.run('git -C ' + str(gitFolder) + ' ' + gitProcessToRun)



def mainFunction(arrayOfArguments):

    pathToRepos = myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')

    def actionToPerformOnEachFileObj(currentFolder, dataForAction):

        for node in currentFolder.iterdir():
            if node.name == '.git':
                runGitProcesses(node.parents[0], arrayOfArguments)


    myPyFunc.onAllFileObjInTreeBreadthFirst(pathToRepos, actionToPerformOnEachFileObj, dataForAction={}, pathsToExclude=[Path(pathToRepos, '.history'), Path(pathToRepos, '.vscode'), Path(pathToRepos, 'reposFromOthers')])


if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
	p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')

