from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(pathToThisPythonFile.parents[3]))
from herokuGorilla.backend.python.myPythonLibrary import myPyFunc
from herokuGorilla.backend.python.myPythonLibrary import myPyAutoGui
from herokuGorilla.backend.python.googleSheets.myGoogleSheetsLibrary import myGspreadFunc

from pprint import pprint as p



def mainFunction(arrayOfArguments):

    def getArrayOfPDFFiles(pathToRoot, foldersToExclude):

        # p(foldersToExclude)

        def ifPDFFile(fileObj):

            # p(fileObj)

            if fileObj.is_file() and fileObj.suffix == '.pdf': return fileObj

            return False

        # folderPathsToExclude = []

        # for folderToExclude in foldersToExclude:

        #     folderPathsToExclude.append(Path(pathToRoot, folderToExclude))

        return myPyFunc.getArrayOfFileObjInTreeBreadthFirst(Path(pathToRoot), ifPDFFile, pathsToExclude=foldersToExclude)

    googleAccountUsername = arrayOfArguments[1]
    googleSpreadsheetTitle = arrayOfArguments[2]
    googleSheetTitleToSaveListTo = arrayOfArguments[3]
    pathToRootToBeginSearching = arrayOfArguments[4]
    arrayOfFoldersToExclude = arrayOfArguments[5:]

    arrayOfFoldersToExclude = [e.replace('\\\\', '\\') for e in arrayOfFoldersToExclude]

    pathBelowRepos = pathToThisPythonFile

    spreadsheetLevelObj = myGspreadFunc.getSpreadsheetLevelObj(True, pathBelowRepos, googleAccountUsername=googleAccountUsername).open(googleSpreadsheetTitle)
    
    arrayOfPDFFilesFromDisk = getArrayOfPDFFiles(pathToRootToBeginSearching, arrayOfFoldersToExclude)
    
    arrayOfPDFFilesFromDisk = [[str(e)] for e in arrayOfPDFFilesFromDisk]
    

    # arrayUploadToGoogleSheets = []

    # for filePath in arrayOfPDFFilesFromDisk:
    #     arrayUploadToGoogleSheets.append([filePath, ''])

    arrayOfPDFFilesFromDisk.insert(0, ['File Path'])
    # p(arrayOfPDFFilesFromDisk)


    clearAndResizeParameters = [
        {
            'sheetObj': spreadsheetLevelObj.worksheet(googleSheetTitleToSaveListTo),
            'resizeRows': 2,
            'startingRowIndexToClear': 0,
            'resizeColumns': 1
        },
    ]

    myGspreadFunc.clearAndResizeSheets(clearAndResizeParameters)
    myGspreadFunc.displayArray(spreadsheetLevelObj.worksheet(googleSheetTitleToSaveListTo), arrayOfPDFFilesFromDisk)
    # myGspreadFunc.autoAlignColumnsInSpreadsheet(spreadsheetLevelObj)


if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
    p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')