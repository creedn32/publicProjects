let path = require('path');

module.exports.getPathArrayUpFolderTree = (arrayOfPathToClimb, nameOfDirectoryToFind) => {

    for (directoryIndex = arrayOfPathToClimb.length; directoryIndex > 0; directoryIndex--) {

        if (arrayOfPathToClimb[directoryIndex] == nameOfDirectoryToFind) return arrayOfPathToClimb.slice(0, directoryIndex + 1);

    }

    return arrayOfPathToClimb;

};

module.exports.pathArrayToStr = (pathArray) => {

    return pathArray.join(path.sep);

};
