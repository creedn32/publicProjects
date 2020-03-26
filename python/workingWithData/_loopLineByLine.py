from pathlib import Path
from pprint import pprint as pp

thisPythonFilePath = Path(__file__).resolve()
pathToRepos = thisPythonFilePath.parents[3]
pathToDataFile = Path(pathToRepos, 'privateData', 'python', 'workingWithData', 'gitDifferences.patch')


with open(pathToDataFile, 'r') as dataFile:
    for line in dataFile:
        if line[0:4] == 'diff': 
            if line[-5:] != '.bat\n':
                print(line)
