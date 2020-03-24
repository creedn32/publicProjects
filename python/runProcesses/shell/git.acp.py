import subprocess
from pathlib import Path
from pprint import pprint as pp


thisPythonFilePath = Path(__file__).resolve()
pathToRepos = thisPythonFilePath.parents[4]
# pp(pathToRepos)

for nodeInRepos in pathToRepos.glob('*'):

    for nodeInEachRepo in nodeInRepos.glob('*'):
        if nodeInEachRepo.name == '.git':
            pp(nodeInEachRepo)

            subprocess.run('git --git-dir=c:\users\cnaylor\portableGit\repos\publicProjects status')

# subprocess.run("git add .")
# subprocess.run("git commit -m \"latest updates, using Python to automate git\"")
# subprocess.run("git push")

