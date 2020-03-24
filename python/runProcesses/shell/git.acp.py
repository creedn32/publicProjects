import subprocess
from pathlib import Path


thisPythonFilePath = Path(__file__).resolve()
pathToPublicProjectsPython = thisPythonFilePath.parents[1]
pathToRepos = pathToPublicProjectsPython.parents[1]

subprocess.run("git add .")
subprocess.run("git commit -m \"latest updates, using Python to automate git\"")
subprocess.run("git push")

