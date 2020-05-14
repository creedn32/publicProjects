#local application imports
from pathlib import Path
import sys
pathToThisPythonFile = Path(__file__).resolve()
sys.path.append(str(pathToThisPythonFile.parents[2]))
import myPythonLibrary._myPyFunc as _myPyFunc

# #standard library imports
# import datetime
from pprint import pprint as p
from runpy import run_path
# import psutil
# from runpy import run_path
# import subprocess

# #third-party imports
# import gspread




def main(arrayOfArguments):
    pathToAppCollectionsToStart = Path(_myPyFunc.replacePartOfPath(pathToThisPythonFile.parents[0], 'publicProjects', 'privateData'), 'start', 'appCollectionsToStart.py')
    importedAppCollectionsToStart = run_path(str(pathToAppCollectionsToStart))
    appCollectionsToStartObj = importedAppCollectionsToStart.get('appCollectionsToStartObj')
    appCollectionToStart = appCollectionsToStartObj[arrayOfArguments[0]][arrayOfArguments[1]]

    p(appCollectionToStart)

    # p(pathToAppCollectionsToStart)
    p(arrayOfArguments)



if __name__ == "__main__":
    main(sys.argv)

