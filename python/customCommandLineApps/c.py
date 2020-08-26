#standard library imports
from pprint import pprint as p
import sys



def mainFunction():

    argumentsArray = sys.argv[1].split('.') + sys.argv[2:]
    # firstArgumentStr = sys.argv[1]

    # if '.' in firstArgumentStr:
    #     endingChar = firstArgumentStr.index('.')
    # else:
    #     endingChar = len(firstArgumentStr)

    moduleToImport = firstArgumentStr[:endingChar]
    # is equivalent to: from os import path as imported
    importedModule = getattr(__import__('pythonScripts', fromlist=[moduleToImport]), moduleToImport)

    

    importedModule.mainFunction(argumentsArray)


if __name__ == '__main__':
    mainFunction()





