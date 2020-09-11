from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
pathToAppend = Path(pathToThisPythonFile.parents[2], 'herokuGorilla', 'backend', 'python', 'myPythonLibrary')
sys.path.append(str(pathToAppend))
import _myPyFunc

from pprint import pprint as p
import importlib.util


def mainFunction():

    p("Searching for command '{}.py' ...".format(sys.argv[1]))

    # argumentsArray = sys.argv[1].split('.') + sys.argv[2:]
    # print(sys.argv)
    
    pathToRepos = _myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')
    # p(pathToRepos)

    def actionToPerformOnEachFileObj(currentFolder):

        for node in currentFolder.iterdir():
            if node.is_file() and node.suffix == '.py':
                if node.stem == 'git':
                    return node
        
        return None

    pathToPythonFileForImport = _myPyFunc.operateOnAllFileObj(pathToRepos, actionToPerformOnEachFileObj, pathsToExclude=[Path(pathToRepos, '.history'), Path(pathToRepos, '.vscode'), Path(pathToRepos, 'reposFromOthers')])

    importedModuleSpec = importlib.util.spec_from_file_location(sys.argv[1], pathToPythonFileForImport)
    importedModule = importlib.util.module_from_spec(importedModuleSpec)
    importedModuleSpec.loader.exec_module(importedModule)
    importedModule.mainFunction(sys.argv[1:])
    # importedModule.MyClass()
    

if __name__ == '__main__':
    mainFunction()





