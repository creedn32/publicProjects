from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
pathToAppend = Path(pathToThisPythonFile.parents[2], 'herokuGorilla', 'backend', 'python', 'myPythonLibrary')
sys.path.append(str(pathToAppend))
import _myPyFunc

from pprint import pprint as p

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
                    return node.parents[0]
        
        return None

    pathToPythonFileForImport = _myPyFunc.operateOnAllFileObj(pathToRepos, actionToPerformOnEachFileObj, pathsToExclude=[Path(pathToRepos, '.history'), Path(pathToRepos, '.vscode'), Path(pathToRepos, 'reposFromOthers')])


    # is equivalent to: from os import path as imported
    importedModule = getattr(__import__('pythonScripts', fromlist=[sys.argv[1]]), sys.argv[1])
    importedModule.mainFunction(sys.argv[1:])


if __name__ == '__main__':
    mainFunction()





