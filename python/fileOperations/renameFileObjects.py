from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
pathToAppend = Path(pathToThisPythonFile.parents[2], 'herokuGorilla', 'backend', 'python', 'myPythonLibrary')
sys.path.append(str(pathToAppend))
import myPyFunc

from pprint import pprint as p
import os, re



def mainFunction(arrayOfArguments):
    

    def actionToPerform(fileObj):

        originalPath = Path(fileObj.parents[0], fileObj.name)
        if fileObj.name[2:3] == ' ':
            newPath = Path(fileObj.parents[0], fileObj.name[3:])
            p('originalPath: ' + str(originalPath) + '; newPath: ' + str(newPath))
            try:
                os.rename(originalPath, newPath)
            except:
                pass

    myPyFunc.onAllFileObjInDir(arrayOfArguments[1], actionToPerform)




if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
	p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')







    # startingPath = Path(arrayOfArguments[1])
    # dataForActionKey = 'suffixToFind'
    # # p(arrayOfArguments[1])

    # def actionToPerformOnEachFileObj(currentFolder, dataForAction):
        
    #     for node in currentFolder.iterdir():
            
    #         # p(node)
            
    #         if node.suffix == dataForAction[dataForActionKey] and node.name[0] == '_':
                
    #             # p(node.parents[0])
    #             p(node)
    #             # os.rename(Path(node.parents[0], node.name), Path(node.parents[0], node.name[1:]))
    #             # pass

    # myPyFunc.onAllFileObjInTreeBreadthFirst(startingPath, actionToPerformOnEachFileObj, dataForAction={dataForActionKey: '.py'}, pathsToExclude=[Path(startingPath, '.history'), Path(startingPath, '.vscode'), Path(startingPath, 'reposFromOthers')])





    # arrayToUse = fileObj.name.split(' ')
    
    # if len(arrayToUse[1]) == 2:
    #     trackNumber = '0' + arrayToUse[1]
    # else: 
    #     trackNumber = arrayToUse[1]

    # newTitle = arrayToUse[0] + ' ' + trackNumber + ' ' + ' '.join(arrayToUse[2:])

    # newFilePath = str(fileObj.parents[0]) + '\\' + newTitle 
    

    # p(newFilePath)

    # os.rename(fileObj, newFilePath)




# for fileObj in Path(sys.argv[1]).iterdir():

#     newFilePath = fileObj

#     arrayToUse = fileObj.name.split(' ')
    
#     if len(arrayToUse[1]) == 2:
#         trackNumber = '0' + arrayToUse[1]
#     else: 
#         trackNumber = arrayToUse[1]

#     newTitle = arrayToUse[0] + ' ' + trackNumber + ' ' + ' '.join(arrayToUse[2:])

#     newFilePath = str(fileObj.parents[0]) + '\\' + newTitle 
    

#     p(newFilePath)

#     os.rename(fileObj, newFilePath)





# for fileObj in Path(sys.argv[1]).iterdir():

#     newFilePath = fileObj

#     arrayToUse = fileObj.name.split(' ')
    
#     if len(arrayToUse[1]) == 2:
#         trackNumber = '0' + arrayToUse[1]
#     else: 
#         trackNumber = arrayToUse[1]

#     newTitle = arrayToUse[0] + ' ' + trackNumber + ' ' + ' '.join(arrayToUse[2:])

#     newFilePath = str(fileObj.parents[0]) + '\\' + newTitle 
    

#     p(newFilePath)

#     os.rename(fileObj, newFilePath)






# for fileObj in Path(sys.argv[1]).iterdir():

#     newFilePath = fileObj
    
#     strToUse = fileObj.name.split(' ')[0]

#     if len(strToUse) == 1:
#         newFilePath = str(fileObj.parents[0]) + '\\' + '0' + fileObj.name

#     p(newFilePath)

    

#     os.rename(str(fileObj), newFilePath)






# for fileObj in Path(sys.argv[1]).iterdir():

    # result = re.search('(.*-)(.*)(\..*)', fileObj.name)
    
    # newFilePath = fileObj
    
    # if len(result.group(2)) == 1:
    #     strToUse = str(fileObj.parents[0]) + '//' + result.group(1) + result.group(2) + '0' + result.group(3)
    #     newFilePath = strToUse
        
    #     p(strToUse)

    # if result.group(2) == '10':
    #     strToUse = str(fileObj.parents[0]) + '//' + result.group(1) + '19' + result.group(3)
    #     newFilePath = strToUse
        
    #     p(strToUse)
    
    # if 'ytellingStorytelling' in fileObj.name:
    #     strToUse = str(fileObj.parents[0]) + '\\' + str(fileObj.name[8:])
    #     p(strToUse)
    #     # newFilePath = str(fileObj.parents[0]) + result.group(1) + '0' + result.group(2) + result.group(3)
    #     newFilePath = strToUse

    # strToUse = str(fileObj.parents[0]) + '\\' + 'Re - Spoken Books - ' + str(fileObj.name)
    # newFilePath = strToUse
    # p(strToUse)

    # os.rename(str(fileObj), newFilePath)