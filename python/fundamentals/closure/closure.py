import pathlib, sys
sys.path.append(str(pathlib.Path(__file__).resolve().parents[0]))
from moduleToImport import functionToCall


def mainFunction(arrayOfArguments):

    a = 5

    def printThis():
        print(a)
        # print(b)
        c = 7

    # print(c)
    functionToCall(printThis)

# mainFunction(sys.argv)

