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




def executeGitCommand(gitFolder, arrayOfArguments):

    p(str(gitFolder))

    if noGitIgnoreFileFound(gitFolder):

        fileObj = open(Path(gitFolder, '.gitignore'), 'w')
        fileObj.write('__pycache__')
        fileObj.close()

    executeGitCommandOnHerokuRepos = False

    if len(arrayOfArguments) > 2 and arrayOfArguments[2] in ['includeheroku', 'h']: executeGitCommandOnHerokuRepos = True

    if arrayOfArguments[1] in ['acp', 'commit']:
        
        if arrayOfArguments[1] == 'acp': subprocess.run('git -C ' + str(gitFolder) + ' add .')

        commitMessage = datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + ', added/committed/pushed using Creed\'s Python script'
        if len(arrayOfArguments) > 3: commitMessage = arrayOfArguments[3]

        subprocess.run('git -C ' + str(gitFolder) + ' commit -m \"' + commitMessage + '\"')

        if arrayOfArguments[1] == 'acp': subprocess.run('git -C ' + str(gitFolder) + ' push')

        if gitFolder.name[:6] == 'heroku' and executeGitCommandOnHerokuRepos:

            pass
            # subprocess.run('git -C ' + str(gitFolder) + ' push heroku master')


    else:
        subprocess.run('git -C ' + str(gitFolder) + ' ' + ' '.join(arrayOfArguments[1:]))



def mainFunction(arrayOfArguments):

    pathToRepos = myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')

    def returnGitFolder(fileObj):

        if fileObj.name == '.git': return fileObj

        return None

    gitFoldersToExecuteCommandOn = myPyFunc.getArrayOfFileObjInTreeBreadthFirst(pathToRepos, returnGitFolder, pathsToExclude=[Path(pathToRepos, '.history'), Path(pathToRepos, '.vscode'),  Path(pathToRepos, 'reposFromOthers'), 'node_modules'])

    for gitFolder in gitFoldersToExecuteCommandOn:

        executeGitCommand(gitFolder.parents[0], arrayOfArguments)



if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
	p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')

