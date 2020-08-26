#standard library imports
from pprint import pprint as p
import sys



def mainFunction():

    argumentsArray = sys.argv[1].split('.') + sys.argv[2:]

    # is equivalent to: from os import path as imported
    importedModule = getattr(__import__('pythonScripts', fromlist=[argumentsArray[0]]), argumentsArray[0])

    importedModule.mainFunction(argumentsArray)


if __name__ == '__main__':
    mainFunction()





