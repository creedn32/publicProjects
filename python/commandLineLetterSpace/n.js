var path = require('path');
thisJSFile = path.basename(__filename);


const c = (textToLogToConsole) => {
    console.log(textToLogToConsole);
}

const getPathUpFolderTree = (pathToClimb, directoryToFind) => {

}




    // for x in range(0, len(pathToClimb.parts) - 1):

    //     # print(pathToClimb.parents[x])

    //     if pathToClimb.parents[x].name == directoryToFind:
    //         return pathToClimb.parents[x]

    // return pathToClimb




const mainFunction = (arrayOfArguments) => {

    c(`Searching for command '${arrayOfArguments[1]}.js' (created by Creed)...`);


}

if (require.main === module) {

    c(`${thisJSFile} (created by Creed) is not being imported. It is being run directly...`);
    mainFunction(process.argv.slice(1));

}
else {

    c(`${thisJSFile} (created by Creed) is being imported. It is not being run directly...`);

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







