# import glob

# for py in glob.glob("*.py"):
#     print(py)
    

from pathlib import Path
from pprint import pprint as p

    
pathToThisPythonFile = Path(__file__).resolve().parents[1]

for fileObj in pathToThisPythonFile.rglob("*"):
    if fileObj.name == '.git':
        p(fileObj.name)