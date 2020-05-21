#local application imports
from pathlib import Path
import sys
pathToThisPythonFile = Path(__file__).resolve()
sys.path.append(str(Path(pathToThisPythonFile.parents[3], 'herokuGorilla', 'backend', 'python')))
import horseStable.clydesdale as clydesdale

#standard library imports
import datetime
from pprint import pprint as p
import psutil
from runpy import run_path
import subprocess

#third-party imports
import gspread




def runGitProcesses(gitFolder, arrayOfArguments):

    p(str(gitFolder))
    

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
    
    pathToRepos = clydesdale.getPathUpFolderTree(pathToThisPythonFile, 'repos')

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


if __name__ == '__main__':
    mainFunction(sys.argv)

