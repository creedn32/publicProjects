#local application imports
from pathlib import Path
import sys
pathToThisPythonFile = Path(__file__).resolve()
sys.path.append(str(Path(pathToThisPythonFile.parents[3], 'herokuGorilla', 'backend', 'python')))
import myPythonLibrary._myPyFunc as _myPyFunc

#standard library imports
import datetime
from pprint import pprint as p
import psutil
from runpy import run_path
import subprocess

#third-party imports
import gspread


def noGitIgnoreFileFound(gitFolder):

    for obj in gitFolder.glob('*'):

        if obj.name == '.gitignore':

            fileObj = open(obj, 'r+')

            for line in fileObj:

                p(line)

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
        commitMessage = nowObj.strftime("%Y-%m-%d %H:%M") + ', latest updates, using Python to commit'
    

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

    # p(arrayOfArguments)
    
    pathToRepos = _myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')

    for objInReposFolder in pathToRepos.glob('*'):

        for objInIndividualRepoFolder in objInReposFolder.glob('*'):

            if objInIndividualRepoFolder.name == '.git':

                gitFolderInIndividualRepoFolder = objInIndividualRepoFolder
                gitIndividualRepoFolder = gitFolderInIndividualRepoFolder.parents[0]

                # p(str(gitFolderInIndividualRepoFolder))

                def getArrayOfChildrenObjects(folderPath):

                    arrayOfChildrenObjects = []
    
                    for obj in folderPath.iterdir():

                        arrayOfChildrenObjects.append(obj)

                    return arrayOfChildrenObjects

                
                arrayOfObjects = [gitIndividualRepoFolder]

                while arrayOfObjects:

                    def isFolder(obj):
                        if obj.is_file():
                            return False
                        else:
                            return True    

                    currentObject = arrayOfObjects.pop(0)

                    if isFolder(currentObject):
                        arrayOfObjects.extend(getArrayOfChildrenObjects(currentObject))               

                    if currentObject.name == '.git' and currentObject != gitFolderInIndividualRepoFolder:
                        # p('this is likely a submodule')
                        # p(currentObject.parents[0])
                        runGitProcesses(currentObject.parents[0], arrayOfArguments)

                runGitProcesses(gitIndividualRepoFolder, arrayOfArguments)


if __name__ == '__main__':
    mainFunction(sys.argv)

