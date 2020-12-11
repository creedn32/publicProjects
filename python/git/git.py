#local application imports
from pathlib import Path
import sys
pathToThisPythonFile = Path(__file__).resolve()
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'herokuGorilla', 'backend', 'python')))
import myPythonLibrary.myPyFunc as myPyFunc

#standard library imports
import datetime
from pprint import pprint as p
import subprocess
import json

def noGitIgnoreFileFound(gitFolder):

    for obj in gitFolder.glob('*'):

        if obj.name == '.gitignore':

            fileObj = open(obj, 'r+')

            for line in fileObj:

                if '__pycache__' in line: return False

            fileObj.write('\n__pycache__')
            fileObj.close()

            return False

    return True

def mainFunction(arrayOfArguments):

    includeWorkFiles = False

    if arrayOfArguments[1] == 'includeWorkFiles':

        includeWorkFiles = True
        del arrayOfArguments[1]

    pathToRepos = myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')

    def returnGitFolder(fileObj):

        if fileObj.name == '.git': return fileObj

        return None

    gitFoldersToExecuteCommandOn = myPyFunc.getArrayOfFileObjInTreeBreadthFirst(pathToRepos, returnGitFolder, pathsToExclude=[Path(pathToRepos, '.history'), Path(pathToRepos, '.vscode'),  Path(pathToRepos, 'reposFromOthers'), 'node_modules'])

    # p(Path(pathToRepos, 'privateData', 'python', 'git', 'git.txt').read_text())

    # with open(Path(pathToRepos, 'privateData', 'python', 'git', 'git.json'), 'w') as filehandle:
    #     json.dump(['hi', 'bue'], filehandle)

    if includeWorkFiles and pathToRepos.parents[0].name == 'cnaylor':

        with open(Path(pathToRepos, 'privateData', 'python', 'git', 'git.json'), 'r') as filehandle:
            arrayOfOtherFolders = json.load(filehandle)

        for otherFolder in arrayOfOtherFolders:
            gitFoldersToExecuteCommandOn.append(Path(otherFolder[1]))

    # gitFoldersToExecuteCommandOn = gitFoldersToExecuteCommandOn[:-1]

    for gitFolder in gitFoldersToExecuteCommandOn:

        if str(gitFolder)[0:3] == 'C:\\': 
        
            gitFolderParent = gitFolder.parents[0]
            gitCommandPrefix = 'git -C \"' + str(gitFolderParent) + "\""

            if noGitIgnoreFileFound(gitFolderParent):

                fileObj = open(Path(gitFolderParent, '.gitignore'), 'w')
                fileObj.write('__pycache__')
                fileObj.close()

        elif str(gitFolder)[0:3] == 'Y:\\':

            gitFolderParent = gitFolder
            gitCommandPrefix = 'git --git-dir=\"' + arrayOfOtherFolders[0][0] + '\" --work-tree=\"' + arrayOfOtherFolders[0][1] + "\""

        p(str(gitFolderParent))

        if arrayOfArguments[1] in ['acp', 'commit']:
            
            if arrayOfArguments[1] == 'acp': 
                
                p(gitCommandPrefix + ' add .')
                subprocess.run(gitCommandPrefix + ' add .')

            commitMessage = datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + ', added/committed/pushed using Creed\'s Python script'
            if len(arrayOfArguments) > 3: commitMessage = arrayOfArguments[3]

            subprocess.run(gitCommandPrefix + ' commit -m \"' + commitMessage + '\"')

            if arrayOfArguments[1] == 'acp': subprocess.run(gitCommandPrefix + ' push')

            # if gitFolderParent.name[:6] == 'heroku' and 'includeheroku' in arrayOfArguments:
                # subprocess.run('git -C ' + str(gitFolderParent) + ' push heroku master')

        else:

            subprocess.run(gitCommandPrefix + ' ' + ' '.join(arrayOfArguments[1:]))



if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
	p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')

