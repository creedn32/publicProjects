#standard library imports
from pprint import pprint as p
import sys



def mainFunction():

    firstArgumentStr = sys.argv[1]

    if '.' in firstArgumentStr:
        endingChar = firstArgumentStr.index('.')
    else:
        endingChar = len(firstArgumentStr)

    moduleToImport = firstArgumentStr[:endingChar]
    # is equivalent to: from os import path as imported
    importedModule = getattr(__import__('scriptsForCustom', fromlist=[moduleToImport]), moduleToImport)

    argumentsArray = sys.argv[1].split('.') + sys.argv[2:]

    importedModule.mainFunction(argumentsArray)


if __name__ == '__main__':
    mainFunction()





