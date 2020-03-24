import subprocess
from pathlib import Path
from pprint import pprint as pp


thisPythonFilePath = Path(__file__).resolve()
pathToRepos = thisPythonFilePath.parents[4]
# pp(pathToRepos)

for nodeInRepos in pathToRepos.glob('*'):

    for nodeInEachRepo in nodeInRepos.glob('*'):
        if nodeInEachRepo.name == '.git':
            pp(str(nodeInEachRepo.parents[0]))
            
            # subprocess.run('git -C ' + str(nodeInEachRepo.parents[0]) + ' status')
            subprocess.run('git -C ' + str(nodeInEachRepo.parents[0]) + ' add .')
            subprocess.run('git -C ' + str(nodeInEachRepo.parents[0]) + ' commit -m \"latest updates, using Python to automate git\"')
            # subprocess.run('git -C ' + str(nodeInEachRepo.parents[0]) + ' push')


# subprocess.run("git add .")
# subprocess.run("git commit -m \"latest updates, using Python to automate git\"")
# subprocess.run("git push")

