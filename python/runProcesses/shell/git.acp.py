import subprocess
from pathlib import Path
from pprint import pprint as pp


thisPythonFilePath = Path(__file__).resolve()
pathToRepos = thisPythonFilePath.parents[2]
pp(pathToRepos)



subprocess.run("git add .")
subprocess.run("git commit -m \"latest updates, using Python to automate git\"")
subprocess.run("git push")

