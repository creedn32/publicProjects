#local application imports
from pathlib import Path
import sys
pathToThisPythonFile = Path(__file__).resolve()
sys.path.append(str(pathToThisPythonFile.parents[1]))
import myPythonLibrary._myPyFunc as _myPyFunc

#standard library imports
import datetime
from pprint import pprint as p
import psutil
from runpy import run_path
import subprocess

#third-party imports
import gspread


nowObj = datetime.datetime.now()

pathToRepos = _myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')
commitMesssage = nowObj.strftime("%Y-%m-%d %H:%M") + ', latest updates, using Python to commit'

def runGitProcesses(gitFolder):

    p(strgitFolder)
    
    if sys.argv[1] == 'acp':
        subprocess.run('git -C ' + str(gitFolder) + ' add .')
        subprocess.run('git -C ' + str(gitFolder) + ' commit -m \"' + commitMesssage + '\"')
        subprocess.run('git -C ' + str(gitFolder) + ' push')
        # subprocess.run('git -C ' + str(gitFolder) + ' status')
    else:
        subprocess.run('git -C ' + str(gitFolder) + ' ' + sys.argv[1])


# p(pathToRepos)

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
                    p('this is likely a submodule')
                    p(currentObject.parents[0])
                    runGitProcesses(currentObject.parents[0])



            runGitProcesses(gitIndividualRepoFolder)
