from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
pathToAppend = Path(pathToThisPythonFile.parents[2], 'herokuGorilla', 'backend', 'python', 'myPythonLibrary')
sys.path.append(str(pathToAppend))
import myPyFunc

from pprint import pprint as p
import importlib.util


def mainFunction():

    p("Searching for command '{}.py' (created by Creed)...".format(sys.argv[1]))

    pathToRepos = myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')

    # def actionToPerformOnEachFileObj(dataForActionObj):

    #     if dataForActionObj['currentFileObj'].is_file() and dataForActionObj['currentFileObj'].suffix == '.py':
    #         if dataForActionObj['currentFileObj'].stem == sys.argv[1]:
    #             dataForActionObj['pathToPythonFileForImport'] = dataForActionObj['currentFileObj']
    #             return dataForActionObj
        
    #     return dataForActionObj

    # returnedDataObj = myPyFunc.onAllFileObjInTreeBreadthFirst(pathToRepos, actionToPerformOnEachFileObj, otherDataObj={'pathsToExclude': [Path(pathToRepos, '.history'), Path(pathToRepos, '.vscode'), Path(pathToRepos, 'reposFromOthers')]})
    
    
    def ifCorrectFileObj(fileObj):

        if fileObj.is_file() and fileObj.suffix == '.py':
            if fileObj.stem == sys.argv[1]:
                return True

        return False


    pathToPythonFileForImport = myPyFunc.findFilePathBreadthFirst(pathToRepos, ifCorrectFileObj, pathsToExclude=[Path(pathToRepos, '.history'), Path(pathToRepos, '.vscode'), Path(pathToRepos, 'reposFromOthers')])



    importedModuleSpec = importlib.util.spec_from_file_location(sys.argv[1], pathToPythonFileForImport)
    importedModule = importlib.util.module_from_spec(importedModuleSpec)
    importedModuleSpec.loader.exec_module(importedModule)
    importedModule.mainFunction(sys.argv[1:])
    # importedModule.MyClass()
    

if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' (created by Creed) is not being imported. It is being run directly...')
    mainFunction()
else:
	p(str(pathToThisPythonFile.name) + ' (created by Creed) is being imported. It is not being run directly...')







