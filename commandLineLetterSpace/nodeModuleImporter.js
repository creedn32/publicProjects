let path = require('path');
let fs = require('fs');
let mainLibrary = require('../node/creedLibrary/mainLibrary/mainLibrary')
let c = console.log.bind(console);

pathArrayThIsFile = path.resolve(__dirname, __filename).split(path.sep);
pathArrayThisFileParent = pathArrayThIsFile.slice(0, pathArrayThIsFile.length - 1)
configJSON = JSON.parse(fs.readFileSync([...pathArrayThisFileParent, 'nodeModuleImporterConfig.json'].join(path.sep)));
nameOfAuthor = configJSON['nameOfAuthor'];


const pathArrayIsDirectory = (pathArrayFileObj) => {

    return fs.statSync(mainLibrary.pathArrayToStr(pathArrayFileObj)).isDirectory();

};


const pathArrayIsFile = (pathArrayFileObj) => {

    return fs.statSync(mainLibrary.pathArrayToStr(pathArrayFileObj)).isFile();

};

const getPathArraySuffix = (pathArrayFileObj) => {

    arrayOfFileNameParts = pathArrayFileObj[pathArrayFileObj.length - 1].split('.');

    if (arrayOfFileNameParts.length > 1) return '.'.concat(arrayOfFileNameParts[arrayOfFileNameParts.length - 1]);

    return '';

};


const getPathArrayStem = (pathArrayFileObj) => {

    arrayOfFileNameParts = pathArrayFileObj[pathArrayFileObj.length - 1].split('.');

    if (arrayOfFileNameParts.length > 1) return arrayOfFileNameParts.slice(0, arrayOfFileNameParts.length - 1).join('.');

    return arrayOfFileNameParts[0];
};


const getArrayOfFileObjArraysFromDir = (pathArrayFileObj, arrayOfPathArraysToExclude) => {

    const fileObjHasPathToExclude = (fileObj, arrayOfPathArraysToExclude) => {

        for (let pathToExclude of arrayOfPathArraysToExclude) {

            if (mainLibrary.pathArrayToStr(fileObj).includes(mainLibrary.pathArrayToStr(pathToExclude))) return true;

        }

        return false;

    }

    arrayOfFileObjArraysFromDir = [];

    fs.readdirSync(mainLibrary.pathArrayToStr(pathArrayFileObj)).forEach(filename => {

        pathArrayFileObjInDirToAdd = [...pathArrayFileObj, filename];

        if (!fileObjHasPathToExclude(pathArrayFileObjInDirToAdd, arrayOfPathArraysToExclude)) arrayOfFileObjArraysFromDir.push(pathArrayFileObjInDirToAdd);

    });

    // c(arrayOfFileObjArraysFromDir);
    return arrayOfFileObjArraysFromDir;
};


const findPathArrayToFileBreadthFirst = (pathArrayRoot, isJSFileToImport, arrayOfPathArraysToExclude=[]) => {

    arrayOfFileObjects = [pathArrayRoot];

    while (arrayOfFileObjects.length) {

        pathArrayFileObj = arrayOfFileObjects.shift();

        if (isJSFileToImport(pathArrayFileObj)) return pathArrayFileObj;

        if (pathArrayIsDirectory(pathArrayFileObj)) arrayOfFileObjects.push(...getArrayOfFileObjArraysFromDir(pathArrayFileObj, arrayOfPathArraysToExclude));

        // if (getPathArraySuffix(pathArrayFileObj) == '.js') c(pathArrayFileObj);
        // // c(getPathArraySuffix(pathArrayFileObj));

    }

};

const importJSFile = (arrayOfArguments) => {

    // c(arrayOfArguments)
    c(`Searching for command '${arrayOfArguments[0]}.js' (created by ${nameOfAuthor})...`);

    pathArrayRoot = mainLibrary.getPathArrayUpFolderTree(pathArrayThIsFile, configJSON['nameOfDirectoryToSetAsRoot']);

    // c(pathArrayRoot);
    
    pathArrayFileForImport = findPathArrayToFileBreadthFirst(pathArrayRoot, (pathArrayFileObj) => {

        if (getPathArraySuffix(pathArrayFileObj) == '.js' && getPathArrayStem(pathArrayFileObj) == arrayOfArguments[0] && pathArrayIsFile(pathArrayFileObj)) return true;

        return false;

    }, arrayOfPathArraysToExclude=[[...pathArrayRoot, '.history'], [...pathArrayRoot, '.vscode'], [...pathArrayRoot, 'reposFromOthers'], [...pathArrayRoot, 'privateData', 'python', 'dataFromStocks'], ['node_modules'], ['.git']]);

    // c(pathArrayFileForImport)

    // c(pathArrayThisFileParent);
    // c(pathArrayFileForImport);

    pathStrRelativeJSFileForImport = './'.concat(path.relative(mainLibrary.pathArrayToStr(pathArrayThisFileParent), mainLibrary.pathArrayToStr(pathArrayFileForImport)))
    // c(pathStrRelativeJSFileForImport);
    // c(arrayOfArguments.slice(1));

    require(pathStrRelativeJSFileForImport)(arrayOfArguments.slice(1));
    // mainFunctionImportedJSFile(arrayOfArguments.slice(1));

};


if (require.main === module) {

    c(`${pathArrayThIsFile[pathArrayThIsFile.length - 1]} (created by ${nameOfAuthor}) is not being imported. It is being run directly...`);
    // c(process.argv)
    importJSFile(process.argv.slice(2));

} else {

    c(`${pathArrayThIsFile[pathArrayThIsFile.length - 1]} (created by ${nameOfAuthor}) is being imported. It is not being run directly...`);

}




