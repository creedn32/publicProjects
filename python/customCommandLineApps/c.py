#standard library imports
from pprint import pprint as p
import sys



def mainFunction():

    # argumentsArray = sys.argv[1].split('.') + sys.argv[2:]

    # print(sys.argv)
    # is equivalent to: from os import path as imported
    importedModule = getattr(__import__('pythonScripts', fromlist=[sys.argv[1]]), sys.argv[1])

    importedModule.mainFunction(sys.argv[1:])


if __name__ == '__main__':
    mainFunction()





