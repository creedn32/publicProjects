import subprocess, sys
from pathlib import Path
from pprint import pprint as pp


thisPythonFilePath = Path(__file__).resolve()
pathToRepos = thisPythonFilePath.parents[3]
# pp(pathToRepos)

for nodeInRepos in pathToRepos.glob('*'):

    for nodeInEachRepo in nodeInRepos.glob('*'):
        if nodeInEachRepo.name == '.git':
            pp(str(nodeInEachRepo.parents[0]))
            
            if sys.argv[1] == 'acp':
                subprocess.run('git -C ' + str(nodeInEachRepo.parents[0]) + ' add .')
                subprocess.run('git -C ' + str(nodeInEachRepo.parents[0]) + ' commit -m \"latest updates, using Python to automate git\"')
                subprocess.run('git -C ' + str(nodeInEachRepo.parents[0]) + ' push')
                # subprocess.run('git -C ' + str(nodeInEachRepo.parents[0]) + ' status')
            else:
                subprocess.run('git -C ' + str(nodeInEachRepo.parents[0]) + ' ' + sys.argv[1])
 


