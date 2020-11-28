from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
pathToAppend = Path(pathToThisPythonFile.parents[2], 'herokuGorilla', 'backend', 'python', 'myPythonLibrary')
sys.path.append(str(pathToAppend))
import myPyFunc

from pprint import pprint as p
import importlib.util


def mainFunction(arrayOfArguments):

    p("Searching for command '{}.py' (created by Creed)...".format(arrayOfArguments[1]))

    pathToRepos = myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')

    def ifPythonFileToImport(fileObj):

        if fileObj.is_file() and fileObj.suffix == '.py':

            if fileObj.stem == arrayOfArguments[1]: return True

        return False

    pathToPythonFileForImport = myPyFunc.findFilePathBreadthFirst(pathToRepos, ifPythonFileToImport, pathsToExclude=[str(Path(pathToRepos, 'privateData', 'python', 'dataFromStocks')), str(Path(pathToRepos, '.history')), str(Path(pathToRepos, '.vscode')), str(Path(pathToRepos, 'reposFromOthers')), '.git', 'node_modules'])


    importedModuleSpec = importlib.util.spec_from_file_location(arrayOfArguments[1], pathToPythonFileForImport)
    importedModule = importlib.util.module_from_spec(importedModuleSpec)
    importedModuleSpec.loader.exec_module(importedModule)
    importedModule.mainFunction(arrayOfArguments[1:])
    # importedModule.MyClass()
    

if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' (created by Creed) is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
	p(str(pathToThisPythonFile.name) + ' (created by Creed) is being imported. It is not being run directly...')







