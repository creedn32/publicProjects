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

for individualRepoFolder in pathToRepos.glob('*'):

    for folderInIndividualRepoFolder in individualRepoFolder.glob('*'):

        # p(folderInIndividualRepoFolder)

        if folderInIndividualRepoFolder.name == '.git':
            p(str(folderInIndividualRepoFolder.parents[0]))


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


            arrayOfFolders = [folderInIndividualRepoFolder.parents[0]]

            while arrayOfFolders:

                currentFolder = arrayOfFolders.pop(0)
                arrayOfFolders.extend(getArrayOfChildrenFolders(currentFolder))
                

                #do what you want with node


                # for node in currentFolder.iterdir():

                #     if node.is_file() and node.suffix == '.py' and node.stem != thisPythonFileStem and node.stem[:1] != '_':
                    
                #         additionalPath = ''

                #         for part in node.parts[len(pathToPublicProjectsPython.parts):]:
                #             additionalPath = additionalPath + '/' + part

                #         newBatchFilePath = Path(batchFilesFolderPath, node.stem + '.bat')
                #         newBatchFileObj = open(newBatchFilePath, 'w+')

                #         newBatchFileObj.write('@echo off \npython %~dp0/../..' + additionalPath + ' %*')
                #         newBatchFileObj.close()




            if sys.argv[1] == 'acp':
                subprocess.run(
                    'git -C ' + str(folderInIndividualRepoFolder.parents[0]) + ' add .')
                subprocess.run(
                    'git -C ' + str(folderInIndividualRepoFolder.parents[0]) + ' commit -m \"' + commitMesssage + '\"')
                subprocess.run(
                    'git -C ' + str(folderInIndividualRepoFolder.parents[0]) + ' push')
                # subprocess.run('git -C ' + str(folderInIndividualRepoFolder.parents[0]) + ' status')
            else:
                subprocess.run(
                    'git -C ' + str(folderInIndividualRepoFolder.parents[0]) + ' ' + sys.argv[1])

