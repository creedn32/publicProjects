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

