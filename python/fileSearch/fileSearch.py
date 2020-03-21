from pathlib import Path
from pprint import pprint as pp
import os

thisPythonFilePath = Path(__file__).resolve()
pathToPublicProjectsPython = thisPythonFilePath.parents[1]

def listOfSubFolders(folderPath):
    subFolderArray = []
 
    for node in folderPath.iterdir():
        if not node.is_file():
            subFolderArray.append(node)

    return subFolderArray


folderArray = [pathToPublicProjectsPython]

while folderArray:
    currentFolder = folderArray.pop(0)
    folderArray.extend(listOfSubFolders(currentFolder))
    
    for node in currentFolder.iterdir():
        if node.is_file() and node.suffix == '.py':
            pp(node.name)





