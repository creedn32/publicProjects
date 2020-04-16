from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[1], 'myPythonLibrary')))
import _myPyFunc


from pprint import pprint as pp
import shutil, os


thisPythonFilePath = Path(__file__).resolve()
thisPythonFileStem = thisPythonFilePath.stem
pathToPublicProjectsPython = _myPyFunc.getPathUpFolderTree(thisPythonFilePath, 'python')
batchFilesFolderPath = Path(_myPyFunc.getPathUpFolderTree(thisPythonFilePath, 'batchScripts'), 'scripts')
templateBatchFilePath = Path(batchFilesFolderPath, thisPythonFileStem + '.bat')


def listOfSubFolders(folderPath):
    subFolderArray = []
 
    for node in folderPath.iterdir():
        if not node.is_file():
            subFolderArray.append(node)

    return subFolderArray



for batchFile in os.listdir(batchFilesFolderPath):
    if batchFile != thisPythonFileStem + '.bat':
        shutil.move(Path(batchFilesFolderPath, batchFile), Path(batchFilesFolderPath.parents[0], "scriptsTrashed", batchFile))


folderArray = [pathToPublicProjectsPython]



while folderArray:
    currentFolder = folderArray.pop(0)
    folderArray.extend(listOfSubFolders(currentFolder))
    
    for node in currentFolder.iterdir():

        if node.is_file() and node.suffix == '.py' and node.stem != thisPythonFileStem and node.stem[:1] != '_':
           
            additionalPath = ''

            for part in node.parts[len(pathToPublicProjectsPython.parts):]:
                additionalPath = additionalPath + '/' + part

            newBatchFilePath = Path(batchFilesFolderPath, node.stem + '.bat')
            newBatchFileObj = open(newBatchFilePath, 'w+')

            newBatchFileObj.write('@echo off \npython %~dp0/../..' + additionalPath + ' %*')
            newBatchFileObj.close()
