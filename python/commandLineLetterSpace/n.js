var path = require('path');
pathToThisJSFile = path.resolve(__dirname, __filename)

const c = (textToLogToConsole) => {
    console.log(textToLogToConsole);
}

const getPathUpFolderTree = (pathToClimb, directoryToFind) => {
    
    pathToClimbArray = pathToClimb.split(path.sep)

    for (directoryLevel = pathToClimbArray.length; directoryLevel > 0; directoryLevel--) {

        if (pathToClimbArray[directoryLevel] == directoryToFind) {
            return pathToClimbArray.slice(0, directoryLevel + 1).join(path.sep) 
        }
    }
    
    return pathToClimb
}

const findFilePathBreadthFirst = (rootDirectory, ifCorrectFileObj, pathsToExclude=[]) => {

    currentArrayOfFileObj = [rootDirectory]

    // while currentArrayOfFileObj:
    
    //     currentFileObj = currentArrayOfFileObj.pop(0)
    
    //     if currentFileObj.is_dir(): currentArrayOfFileObj.extend(getArrayOfFileObjFromDir(currentFileObj, pathsToExclude))
    
    //     if ifCorrectFileObj(currentFileObj): return currentFileObj

}






const mainFunction = (arrayOfArguments) => {

    c(`Searching for command '${arrayOfArguments[1]}.js' (created by Creed)...`);

    pathToRepos = getPathUpFolderTree(pathToThisJSFile, 'repos')

    // pathToJSFileForImport = findFilePathBreadthFirst(pathToRepos, rifPythonFileToImport, pathsToExclude=[str(Path(pathToRepos, '.history')), str(Path(pathToRepos, '.vscode')), str(Path(pathToRepos, 'reposFromOthers')), 'node_modules'])
}

if (require.main === module) {

    c(`${path.basename(pathToThisJSFile)} (created by Creed) is not being imported. It is being run directly...`);
    mainFunction(process.argv.slice(1));

}
else {

    c(`${path.basename(pathToThisJSFile)} (created by Creed) is being imported. It is not being run directly...`);

}


//     pathToRepos = myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')

//     def ifPythonFileToImport(fileObj):

//         if fileObj.is_file() and fileObj.suffix == '.py':

//             if fileObj.stem == sys.argv[1]: return True

//         return False

//     pathToPythonFileForImport = myPyFunc.findFilePathBreadthFirst(pathToRepos, ifPythonFileToImport, pathsToExclude=[str(Path(pathToRepos, '.history')), str(Path(pathToRepos, '.vscode')), str(Path(pathToRepos, 'reposFromOthers')), 'node_modules'])


//     importedModuleSpec = importlib.util.spec_from_file_location(sys.argv[1], pathToPythonFileForImport)
//     importedModule = importlib.util.module_from_spec(importedModuleSpec)
//     importedModuleSpec.loader.exec_module(importedModule)
//     importedModule.mainFunction(sys.argv[1:])
//     # importedModule.MyClass()







