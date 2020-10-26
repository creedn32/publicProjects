from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
pathToAppend = Path(pathToThisPythonFile.parents[2], 'herokuGorilla', 'backend', 'python', 'myPythonLibrary')
sys.path.append(str(pathToAppend))
import myPyFunc

from pprint import pprint as p
import importlib.util


def mainFunction():

    p("Searching for command '{}.py' ...".format(sys.argv[1]))

    # argumentsArray = sys.argv[1].split('.') + sys.argv[2:]
    # print(sys.argv)
    
    pathToRepos = myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')
    dataForActionKey = 'pythonFileToFind'

    def actionToPerformOnEachFileObj(currentFolder, dataForAction):

        for node in currentFolder.iterdir():
            if node.is_file() and node.suffix == '.py':
                if node.stem == dataForAction[dataForActionKey]:
                    return node
        
        return None

    pathToPythonFileForImport = myPyFunc.onAllFileObjInTreeBreadthFirst(pathToRepos, actionToPerformOnEachFileObj, dataForAction={dataForActionKey: sys.argv[1]}, pathsToExclude=[Path(pathToRepos, '.history'), Path(pathToRepos, '.vscode'), Path(pathToRepos, 'reposFromOthers')])

    importedModuleSpec = importlib.util.spec_from_file_location(sys.argv[1], pathToPythonFileForImport)
    importedModule = importlib.util.module_from_spec(importedModuleSpec)
    importedModuleSpec.loader.exec_module(importedModule)
    importedModule.mainFunction(sys.argv[1:])
    # importedModule.MyClass()
    

if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction()
else:
	p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')







