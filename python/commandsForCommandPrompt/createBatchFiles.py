# import os, shutil
# from pathlib import Path as path
# from pprint import pprint as pp


# thisPythonFilePath = path(__file__).resolve()
# thisPythonFile = thisPythonFilePath.stem
# thisPythonFileContainingFolder = thisPythonFilePath.parents[0]

# listOfPythonFiles = list(thisPythonFileContainingFolder.glob("*"))
# batchFilesFolderPath = path(thisPythonFileContainingFolder.parents[0], "batchFiles")
# templateBatchFilePath = path(batchFilesFolderPath, thisPythonFile + ".bat")

# for pythonFile in listOfPythonFiles:
    
#     if pythonFile.name != thisPythonFilePath.name:
#         newBatchFilePath = path(batchFilesFolderPath, pythonFile.stem + ".bat")
#         shutil.copy(templateBatchFilePath, newBatchFilePath)



from pathlib import Path
from pprint import pprint as pp


thisPythonFilePath = Path(__file__).resolve()
pathToPublicProjectsPython = thisPythonFilePath.parents[1]
# pp(pathToPublicProjectsPython)
batchFilesFolderPath = Path(thisPythonFilePath.parents[0], "batchFiles")
# pp(batchFilesFolderPath)


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
            pass
            # pp(node)