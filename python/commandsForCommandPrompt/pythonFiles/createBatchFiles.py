import os, shutil
from pathlib import Path as path
from pprint import pprint as pp


thisPythonFilePath = path(__file__).resolve()
thisPythonFile = thisPythonFilePath.stem
thisPythonFileContainingFolder = thisPythonFilePath.parents[0]

listOfPythonFiles = list(thisPythonFileContainingFolder.glob("*"))
batchFilesFolderPath = path(thisPythonFileContainingFolder.parents[0], "batchFiles")
templateBatchFilePath = path(batchFilesFolderPath, thisPythonFile + ".bat")

for pythonFile in listOfPythonFiles:
    
    if pythonFile.name != thisPythonFilePath.name:
        newBatchFilePath = path(batchFilesFolderPath, pythonFile.stem + ".bat")
        shutil.copy(templateBatchFilePath, newBatchFilePath)
