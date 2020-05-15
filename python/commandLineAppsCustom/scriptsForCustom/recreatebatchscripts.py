#local application imports
from pathlib import Path
import sys
pathToThisPythonFile = Path(__file__).resolve()
sys.path.append(str(pathToThisPythonFile.parents[2]))
import myPythonLibrary._myPyFunc as _myPyFunc
import googleSheets.processIsNotRunning.processIsNotRunning as processIsNotRunning

#standard library imports
import os
from pprint import pprint as p
import shutil


def mainFunction(arrayOfArguments):
    pathToThisPythonFile = Path(__file__).resolve()
    p(1)


if __name__ == "__main__":
    mainFunction(sys.argv)




# thisPythonFileStem = pathToThisPythonFile.stem
p(pathToThisPythonFile.stem)
pathToPublicProjectsPython = _myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'python')
pathToBatchScriptsFolder = Path(pathToPublicProjectsPython, 'commandLineAppsCustom', 'batchScripts', 'scripts')
# templateBatchFilePath = Path(pathToBatchScriptsFolder, thisPythonFileStem + '.bat')


def listOfSubFolders(folderPath):
    subFolderArray = []
 
    for fileObj in folderPath.iterdir():
        if not fileObj.is_file():
            subFolderArray.append(fileObj)

    return subFolderArray



for batchFile in os.listdir(pathToBatchScriptsFolder):
    pass
    shutil.move(Path(pathToBatchScriptsFolder, batchFile), Path(pathToBatchScriptsFolder.parents[0], "scriptsTrashed", batchFile))

folderArray = [pathToPublicProjectsPython]

while folderArray:

    currentFolder = folderArray.pop(0)
    folderArray.extend(listOfSubFolders(currentFolder))
    
    if currentFolder != 'scriptsForCustom':

        for fileObj in currentFolder.iterdir():

            if fileObj.is_file() and fileObj.suffix == '.py' and fileObj.stem[:1] != '_':
            
                additionalPath = ''

                # p(fileObj.parts)

                for part in fileObj.parts[len(pathToPublicProjectsPython.parts):]:
                    additionalPath = additionalPath + '/' + part

                p(additionalPath)

                newBatchFilePath = Path(pathToBatchScriptsFolder, fileObj.stem + '.bat')
                newBatchFileObj = open(newBatchFilePath, 'w+')

                newBatchFileObj.write('@echo off \npython %~dp0/../../..' + additionalPath + ' %*')
                newBatchFileObj.close()
