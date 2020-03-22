from pathlib import Path
from pprint import pprint as pp
import shutil, os


thisPythonFilePath = Path(__file__).resolve()
thisPythonFileStem = thisPythonFilePath.stem
pathToPublicProjectsPython = thisPythonFilePath.parents[1]
batchFilesFolderPath = Path(thisPythonFilePath.parents[0], 'batchFiles')
templateBatchFilePath = Path(batchFilesFolderPath, thisPythonFileStem + '.bat')


def listOfSubFolders(folderPath):
    subFolderArray = []
 
    for node in folderPath.iterdir():
        if not node.is_file():
            subFolderArray.append(node)

    return subFolderArray


folderArray = [pathToPublicProjectsPython]


for batchFile in os.listdir(batchFilesFolderPath):
    if batchFile != thisPythonFileStem + '.bat':
        shutil.move(Path(batchFilesFolderPath, batchFile), Path(batchFilesFolderPath.parents[0], "batchFilesTrashed", batchFile))
        # pp(batchFile)


while folderArray:
    currentFolder = folderArray.pop(0)
    folderArray.extend(listOfSubFolders(currentFolder))
    
    for node in currentFolder.iterdir():
        if node.is_file() and node.suffix == '.py':
            if node.stem != thisPythonFileStem:
                pp(node)
                newBatchFilePath = Path(batchFilesFolderPath, node.stem + '.bat')
                newBatchFileObj = open(newBatchFilePath, 'w+')
                newBatchFileObj.write('@echo off \npython ' + str(node) + ' %*')
                newBatchFileObj.close()
                # shutil.copy(templateBatchFilePath, newBatchFilePath)