from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(pathToThisPythonFile.parents[3]))
from herokuGorilla.backend.python.myPythonLibrary import myPyFunc
from herokuGorilla.backend.python.myPythonLibrary import myPyAutoGui
from herokuGorilla.backend.python.googleSheets.myGoogleSheetsLibrary import myGspreadFunc

from pprint import pprint as p


def getArrayOfPDFFiles(pathToRoot):

    def ifPDFFile(fileObj):

        if fileObj.is_file() and fileObj.suffix == '.pdf': return str(fileObj)

        return False

    return myPyFunc.getArrayOfFileObjInTreeBreadthFirst(Path(pathToRoot), ifPDFFile)

def mainFunction(arrayOfArguments):

    pathBelowRepos = pathToThisPythonFile
    spreadsheetLevelObj = myGspreadFunc.getSpreadsheetLevelObj(True, pathBelowRepos, googleAccountUsername=arrayOfArguments[3]).open(arrayOfArguments[2])

    arrayOfPDFFilesFromDisk = getArrayOfPDFFiles(arrayOfArguments[1])

    arrayUploadToGoogleSheets = []

    for filePath in arrayOfPDFFilesFromDisk:
        arrayUploadToGoogleSheets.append([filePath, ''])

    arrayUploadToGoogleSheets.insert(0, ['File Path', 'Completed?'])


    clearAndResizeParameters = [
        {
            'sheetObj': spreadsheetLevelObj.worksheet(arrayOfArguments[4]),
            'resizeRows': 2,
            'startingRowIndexToClear': 0,
            'resizeColumns': 1
        },
    ]

    myGspreadFunc.clearAndResizeSheets(clearAndResizeParameters)
    myGspreadFunc.displayArray(spreadsheetLevelObj.worksheet(arrayOfArguments[4]), arrayUploadToGoogleSheets)
    myGspreadFunc.autoAlignColumnsInSpreadsheet(spreadsheetLevelObj)


if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
    p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')