import subprocess
import sys
from pathlib import Path
from pprint import pprint as pp

import datetime
nowObj = datetime.datetime.now()

thisPythonFilePath = Path(__file__).resolve()
pathToRepos = thisPythonFilePath.parents[3]
commitMesssage = nowObj.strftime("%Y-%m-%d %H:%M") + ', latest updates, using Python to commit'



# pp(pathToRepos)

for nodeInRepos in pathToRepos.glob('*'):

    for nodeInEachRepo in nodeInRepos.glob('*'):
        if nodeInEachRepo.name == '.git':
            pp(str(nodeInEachRepo.parents[0]))

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

