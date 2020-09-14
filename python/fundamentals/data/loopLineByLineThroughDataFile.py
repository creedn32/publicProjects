from pathlib import Path
from pprint import pprint as pp

thisPythonFilePath = Path(__file__).resolve()
pathToRepos = thisPythonFilePath.parents[4]
pathToDataFile = Path(pathToRepos, 'privateData', 'python', 'fundamentals', 'data', 'gitDifferences.patch')


with open(pathToDataFile, 'r') as dataFile:
    for line in dataFile:
        if line[0:4] == 'diff': 
            if line[-5:] != '.bat\n':
                print(line)
