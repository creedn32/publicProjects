"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""



import os



def compute_checksums(dirname, suffix, pathLabel, checkSumObject):
    """Computes checksums for all files with the given suffix.

    dirname: string name of directory to search
    suffix: string suffix to match

    Returns: map from checksum to list of files with that checksum
    """

    from pprint import pprint as p

    names = walk(dirname)
    # p(names)

    for name in names:
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
                checkSumObject[checksum].append({pathLabel: name})
            else:
                checkSumObject[checksum] = [{pathLabel: name}]

    # p(d)
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
            names.extend(walk(path))
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



def print_duplicates(d, pathLabel):
    """Checks for duplicate files.

    Reports any files with the same checksum and checks whether they
    are, in fact, identical.

    d: map from checksum to list of files with that checksum
    """
    for key, names in d.items():
        # print(names)
        
        if len(names) > 1:
            # print('The following files have the same checksum:')
            # for name in names:
                # print(name)

            if check_pairs(names, pathLabel):
                # pass
                print('The following files are identical: ')
                for name in names:
                    print(name[pathLabel])



def check_pairs(names, pathLabel):
    """Checks whether any in a list of files differs from the others.

    names: list of string filenames
    """
    for name1 in names:
        for name2 in names:
            if name1[pathLabel] < name2[pathLabel]:
                res, stat = check_diff(name1[pathLabel], name2[pathLabel])
                # print("res " + res)
                # print("stat " + str(stat))

                if res:
                    return False
    return True





def check_diff(name1, name2):
    """Computes the difference between the contents of two files.

    name1, name2: string filenames
    """
    cmd = 'diff %s %s' % (name1, name2)
    # print(cmd)
    return pipe(cmd)
            




if __name__ == '__main__':

    from pprint import pprint as p
    import pathlib
    pathToThisPythonFile = pathlib.Path(__file__).resolve()
    originalPath = pathlib.Path(pathToThisPythonFile.parents[1]) #, 'guiAutomation')


    checkSumObject = compute_checksums(str(originalPath), '', 'originalPath'. {})
    p(checkSumObject)

    
    # print_duplicates(d, 'originalPath')




    # d = compute_checksums(dirname='.', suffix='.py')