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

for nodeInRepos in pathToRepos.glob('*'):

    for nodeInEachRepo in nodeInRepos.glob('*'):

        # p(nodeInEachRepo)

        if nodeInEachRepo.name == '.git':
            p(str(nodeInEachRepo.parents[0]))


            # def listOfSubFolders(folderPath):
            #     subFolderArray = []
 
            #     for node in folderPath.iterdir():
            #         if not node.is_file():
            #             subFolderArray.append(node)

            #     return subFolderArray


            # folderArray = [nodeInEachRepo.parents[0]]

            # while folderArray:

            #     currentFolder = folderArray.pop(0)
            #     folderArray.extend(listOfSubFolders(currentFolder))
                
            #     for node in currentFolder.iterdir():

            #         if node.is_file() and node.suffix == '.py' and node.stem != thisPythonFileStem and node.stem[:1] != '_':
                    
            #             additionalPath = ''

            #             for part in node.parts[len(pathToPublicProjectsPython.parts):]:
            #                 additionalPath = additionalPath + '/' + part

            #             newBatchFilePath = Path(batchFilesFolderPath, node.stem + '.bat')
            #             newBatchFileObj = open(newBatchFilePath, 'w+')

            #             newBatchFileObj.write('@echo off \npython %~dp0/../..' + additionalPath + ' %*')
            #             newBatchFileObj.close()




            if sys.argv[1] == 'acp':
                subprocess.run(
                    'git -C ' + str(nodeInEachRepo.parents[0]) + ' add .')
                subprocess.run(
                    'git -C ' + str(nodeInEachRepo.parents[0]) + ' commit -m \"' + commitMesssage + '\"')
                subprocess.run(
                    'git -C ' + str(nodeInEachRepo.parents[0]) + ' push')
                # subprocess.run('git -C ' + str(nodeInEachRepo.parents[0]) + ' status')
            else:
                subprocess.run(
                    'git -C ' + str(nodeInEachRepo.parents[0]) + ' ' + sys.argv[1])

