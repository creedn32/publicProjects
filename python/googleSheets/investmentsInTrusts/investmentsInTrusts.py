#local application imports
from pathlib import Path
import sys
pathToThisPythonFile = Path(__file__).resolve()
sys.path.append(str(pathToThisPythonFile.parents[2]))
import myPythonLibrary._myPyFunc as _myPyFunc
import googleSheets.myGoogleSheetsLibrary._myGoogleSheetsFunc as _myGoogleSheetsFunc
import googleSheets.myGoogleSheetsLibrary._myGspreadFunc as _myGspreadFunc

#standard library imports
from pprint import pprint as p
import psutil


#third-party imports
import gspread




def mainFunction():

    objOfSheets = _myGspreadFunc.getObjOfSheets('Data For Apps')
    
    p(objOfSheets['investmentsInTrusts']['array'])


if __name__ == '__main__':
    mainFunction()
