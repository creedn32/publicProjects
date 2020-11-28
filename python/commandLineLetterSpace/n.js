var path = require('path');
var fs = require('fs');
thisFilePathArray = path.resolve(__dirname, __filename).split(path.sep);

const c = (textToLogToConsole) => {
    console.log(textToLogToConsole);
}

const getPathUpFolderTree = (arrayOfPathToClimb, nameOfDirectoryToFind) => {

    for (directoryIndex = arrayOfPathToClimb.length; directoryIndex > 0; directoryIndex--) {

        if (arrayOfPathToClimb[directoryIndex] == nameOfDirectoryToFind) {
            return arrayOfPathToClimb.slice(0, directoryIndex + 1);
        }
    }
    
    return arrayOfPathToClimb;
}

const isDirectory = (fileObjPathArray) => {
    return fs.statSync(pathArrayToStr(fileObjPathArray)).isDirectory();
}
const isFile = (fileObjPathArray) => {

    return fs.statSync(pathArrayToStr(fileObjPathArray)).isFile();
}

const pathArrayToStr = (pathArray) => {

    return pathArray.join(path.sep);

}

const getSuffix = (fileObjPathArray) => {

    arrayOfFileNameParts = fileObjPathArray.slice(-1)[0].split('.');

    if (arrayOfFileNameParts.length > 1) return '.'.concat(arrayOfFileNameParts.slice(-1)[0]);
    
    return '';

}

const getStem = (fileObjPathArray) => {

    arrayOfFileNameParts = fileObjPathArray.slice(-1)[0].split('.');

    if (arrayOfFileNameParts.length > 1) return arrayOfFileNameParts.slice(0, arrayOfFileNameParts.length - 1).join('.');

    return arrayOfFileNameParts[0];
}

const getArrayOfFileObjFromDir = (fileObjPathArray, pathsToExclude) => {

    const fileObjHasPathToExclude = (fileObj, pathsToExclude) => {

        for (let pathToExclude of pathsToExclude) {

            if (pathArrayToStr(fileObj).includes(pathArrayToStr(pathToExclude))) return true;

        }

        return false;

    }

    arrayOfFileObjFromDir = [];

    fs.readdirSync(pathArrayToStr(fileObjPathArray)).forEach(filename => {

        fileObjInDirToAdd = [...fileObjPathArray, filename];

        if (!fileObjHasPathToExclude(fileObjInDirToAdd, pathsToExclude)) arrayOfFileObjFromDir.push(fileObjInDirToAdd);

    });

    return arrayOfFileObjFromDir;
}

const findFilePathBreadthFirst = (rootPathArray, isJSFileToImport, pathsToExclude=[]) => {

    arrayOfFileObjs = [rootPathArray];

    while (arrayOfFileObjs.length) {

        fileObjPathArray = arrayOfFileObjs.shift();

        if (isDirectory(fileObjPathArray)) arrayOfFileObjs.push(...getArrayOfFileObjFromDir(fileObjPathArray, pathsToExclude));

        // if (getSuffix(fileObjPathArray) == '.js') c(fileObjPathArray);
        // // c(getSuffix(fileObjPathArray));

        if (isJSFileToImport(fileObjPathArray)) return fileObjPathArray;

    }

}



const mainFunction = (arrayOfArguments) => {

    c(`Searching for command '${arrayOfArguments[1]}.js' (created by Creed)...`);

    reposPathArray = getPathUpFolderTree(thisFilePathArray, 'repos');

    pathToJSFileForImport = findFilePathBreadthFirst(reposPathArray, (fileObjPathArray) => {

        if (isFile(fileObjPathArray) && getSuffix(fileObjPathArray) == '.js' && getStem(fileObjPathArray) == arrayOfArguments[1]) return true;

        return false;

    }, pathsToExclude=[[...reposPathArray, '.history'], [...reposPathArray, '.vscode'], [...reposPathArray, 'reposFromOthers'], [...reposPathArray, 'privateData', 'python', 'dataFromStocks'], ['node_modules'], ['.git']]);

    // var importedModule = require('hi.js')
    c(path.relative(pathArrayToStr(thisFilePathArray), pathArrayToStr(pathToJSFileForImport)))

}


if (require.main === module) {

    c(`${thisFilePathArray.slice(-1)[0]} (created by Creed) is not being imported. It is being run directly...`);
    mainFunction(process.argv.slice(1));

} else {

    c(`${thisFilePathArray.slice(-1)[0]} (created by Creed) is being imported. It is not being run directly...`);

}


//     importedModuleSpec = importlib.util.spec_from_file_location(sys.argv[1], pathToPythonFileForImport)
//     importedModule = importlib.util.module_from_spec(importedModuleSpec)
//     importedModuleSpec.loader.exec_module(importedModule)
//     importedModule.mainFunction(sys.argv[1:])
//     # importedModule.MyClass()







