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



# p(pathToRepos)

for objInReposFolder in pathToRepos.glob('*'):

    for objInIndividualRepoFolder in objInReposFolder.glob('*'):

        if objInIndividualRepoFolder.name == '.git':

            individualRepoFolderWithGit = objInIndividualRepoFolder.parents[0]
            p(str(individualRepoFolderWithGit))

            def getArrayOfChildrenFolders(folderPath):

                arrayOfChildrenFolders = []
 
                for fileOrFolder in folderPath.iterdir():

                    def isFolder(fileOrFolder):
                        if fileOrFolder.is_file():
                            return False
                        else:
                            return True
                
                    if isFolder(fileOrFolder):
                        arrayOfChildrenFolders.append(fileOrFolder)

                return arrayOfChildrenFolders

            
            arrayOfFolders = [individualRepoFolderWithGit]

            while arrayOfFolders:

                currentFolder = arrayOfFolders.pop(0)
                arrayOfFolders.extend(getArrayOfChildrenFolders(currentFolder))               

                if currentFolder.name == '.git':
                    pass
                    p('this folder is a git folder')
                    p(currentFolder)

                if currentFolder.name == 'herokuHelloJavascript':
                    p('heroku')




            if sys.argv[1] == 'acp':
                subprocess.run(
                    'git -C ' + str(objInIndividualRepoFolder.parents[0]) + ' add .')
                subprocess.run(
                    'git -C ' + str(objInIndividualRepoFolder.parents[0]) + ' commit -m \"' + commitMesssage + '\"')
                subprocess.run(
                    'git -C ' + str(objInIndividualRepoFolder.parents[0]) + ' push')
                # subprocess.run('git -C ' + str(objInIndividualRepoFolder.parents[0]) + ' status')
            else:
                subprocess.run(
                    'git -C ' + str(objInIndividualRepoFolder.parents[0]) + ' ' + sys.argv[1])

