
module.exports.c = (textToLogToConsole) => {

    console.log(textToLogToConsole);

};

module.exports.getPathUpFolderTree = (arrayOfPathToClimb, nameOfDirectoryToFind) => {

    for (directoryIndex = arrayOfPathToClimb.length; directoryIndex > 0; directoryIndex--) {

        if (arrayOfPathToClimb[directoryIndex] == nameOfDirectoryToFind) return arrayOfPathToClimb.slice(0, directoryIndex + 1);

    }

    return arrayOfPathToClimb;

};
