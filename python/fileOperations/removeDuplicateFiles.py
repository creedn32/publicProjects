"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""



import os



def compute_checksums(pathsToWalk, suffix):
    """Computes checksums for all files with the given suffix.

    originalPath: string name of directory to search
    suffix: string suffix to match

    Returns: map from checksum to list of files with that checksum
    """

    from pprint import pprint as p

    checkSumObject = {}

    for pathToWalk in pathsToWalk:

        if pathsToWalk.index(pathToWalk) == 0:
            pathLabel = 'originalPath'
        elif pathsToWalk.index(pathToWalk) == 1:
            pathLabel = 'pathToRemoveFrom'
            
        names = walk(pathToWalk)
        
        # p(names)
        print('checksum calcated for ' + pathLabel + ':')

        for count, name in enumerate(names):
            if name.endswith(suffix):
                # print(compute_checksum(name)[0])
                # print(compute_checksum(name)[1])
                res, stat = compute_checksum(name)
                # print(res)

                numberOfSplits = 1
                checksum = res.split(' ', numberOfSplits)[numberOfSplits - 1]
                # _ = res.split(' ', numberOfSplits)[numberOfSplits]
                # print(_)


                if checksum in checkSumObject:
                    if pathLabel in checkSumObject[checksum]:
                        checkSumObject[checksum][pathLabel].append(name)
                    else:
                        checkSumObject[checksum][pathLabel] = [name]
                else:
                    checkSumObject[checksum] = {pathLabel: [name]}

            print(str(count + 1) + '/' + str(len(names)))

    return checkSumObject



def walk(dirname):
    """Finds the names of all files in dirname and its subdirectories.

    dirname: string name of directory
    """
    names = []
    for name in os.listdir(dirname):
        path = os.path.join(dirname, name)

        if os.path.isfile(path):
            names.append(path)
        else:
            try:
                names.extend(walk(path))
            except Exception as e:
                pass
                # print('Error is ' + str(e))
                # print(path)
    return names




def compute_checksum(filename):
    """Computes the MD5 checksum of the contents of a file.

    filename: string
    """

    # print(filename)
    cmd = 'md5sum \"' + filename + '\"'
    return pipe(cmd)




def pipe(cmd):
    """Runs a command in a subprocess.

    cmd: string Unix command

    Returns (res, stat), the output of the subprocess and the exit status.
    """
    fp = os.popen(cmd)
    res = fp.read()
    stat = fp.close()
    assert stat is None
    return res, stat



def get_duplicates(checkSumObject):
    """Checks for duplicate files.

    Reports any files with the same checksum and checks whether they
    are, in fact, identical.

    d: map from checksum to list of files with that checksum
    """

    pathsToRemove = []

    for pathObject in checkSumObject.values():

        lengthOfOriginalPathArray = len(pathObject.get('originalPath', []))
        strLengthOfOriginalPathArray = str(lengthOfOriginalPathArray)
        totalPathsInPathObject = lengthOfOriginalPathArray + len(pathObject.get('pathToRemoveFrom', []))

        if totalPathsInPathObject > 1 and lengthOfOriginalPathArray > 0:
 
            print('originalPath has ' + strLengthOfOriginalPathArray + ' file(s) with a matching checksum to files in the pathToRemove. Checked if duplicates exist: ')

            for count, pathOriginal in enumerate(pathObject['originalPath']):
                for pathToRemove in pathObject['pathToRemoveFrom']:
                    res, stat = check_diff(pathOriginal, pathToRemove)

                    if not res:
                        # print(pathOriginal + " is identical to " + pathToRemove)
                        # print(pathToRemove + " will be removed")
                        pathsToRemove.append(pathToRemove)
                        return pathsToRemove

                print(str(count + 1) + '/' + strLengthOfOriginalPathArray)

    return pathsToRemove



def check_diff(name1, name2):
    """Computes the difference between the contents of two files.

    name1, name2: string filenames
    """
    cmd = 'diff %s %s' % (name1, name2)
    # print(cmd)
    return pipe(cmd)
            


def remove_files(fileList):

    for fileToRemove in fileList:
        if os.path.exists(fileToRemove):
            print('This file will be removed: ' + fileToRemove)
            removeFilePythonCode = 'os.unlink(fileToRemove)'
            print(removeFilePythonCode)
            # exec(removeFilePythonCode)




if __name__ == '__main__':

    from pprint import pprint as p
    import pathlib
    pathToThisPythonFile = pathlib.Path(__file__).resolve()
    originalPath = pathlib.Path(pathToThisPythonFile.parents[1], 'gui') #, 'guiAutomation')
    pathToRemoveFrom = pathlib.Path(pathToThisPythonFile.parents[0])



    pathsToWalk = [str(pathlib.Path(pathToThisPythonFile.parents[0])),
                    str(pathlib.Path(pathToThisPythonFile.parents[1], 'gui'))]

    checkSumObject = compute_checksums(pathsToWalk, '')

    # p(checkSumObject)
    remove_files(list(dict.fromkeys(get_duplicates(checkSumObject))))




    # d = compute_checksums(dirname='.', suffix='.py')


    