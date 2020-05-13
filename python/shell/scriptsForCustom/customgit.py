#local application imports
from pathlib import Path
import sys
pathToThisPythonFile = Path(__file__).resolve()
sys.path.append(str(pathToThisPythonFile.parents[2]))
import myPythonLibrary._myPyFunc as _myPyFunc

#standard library imports
import datetime
from pprint import pprint as p
import psutil
from runpy import run_path
import subprocess

#third-party imports
import gspread




def runGitProcesses(gitFolder, arrayOfArguments):

    nowObj = datetime.datetime.now()
    commitMessage = nowObj.strftime("%Y-%m-%d %H:%M") + ', latest updates, using Python to commit'

    p(str(gitFolder))
    
    if arrayOfArguments[1] == 'acp':
        subprocess.run('git -C ' + str(gitFolder) + ' add .')
        subprocess.run('git -C ' + str(gitFolder) + ' commit -m \"' + commitMessage + '\"')
        subprocess.run('git -C ' + str(gitFolder) + ' push')
    else:
        subprocess.run('git -C ' + str(gitFolder) + ' ' + arrayOfArguments[1])


def main(arrayOfArguments):

    if arrayOfArguments[0] == 'all':

        pathToRepos = _myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')

        for objInReposFolder in pathToRepos.glob('*'):

            for objInIndividualRepoFolder in objInReposFolder.glob('*'):

                if objInIndividualRepoFolder.name == '.git':

                    gitObjInIndividualRepoFolder = objInIndividualRepoFolder
                    gitIndividualRepoFolder = gitObjInIndividualRepoFolder.parents[0]

                    # p(str(gitObjInIndividualRepoFolder))

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

                        if currentObject.name == '.git' and currentObject != gitObjInIndividualRepoFolder:
                            # p('this is likely a submodule')
                            # p(currentObject.parents[0])
                            runGitProcesses(currentObject.parents[0], arrayOfArguments)

                    runGitProcesses(gitIndividualRepoFolder, arrayOfArguments)


if __name__ == "__main__":
    main(sys.argv)

