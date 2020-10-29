from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(pathToThisPythonFile.parents[3]))
from herokuGorilla.backend.python.myPythonLibrary import myPyFunc

from pprint import pprint as p
import lxml.etree as et
from datetime import datetime
import os
import csv



def csvRowMatchesElement(currentCSVRow, element):
    for currentCSVColumnNum, currentCSVColumn in enumerate(currentCSVRow):
        if currentCSVColumn != element[currentCSVColumnNum]:
            return False
    return True


def csvRowNotInXML(currentCSVRow, root):
    
    for element in root:
        if csvRowMatchesElement(currentCSVRow, element):
            return False
    
    return True


def mainFunction(arrayOfArguments):

    currentFileObjXMLTreeRoot = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]   #et.parse(arrayOfArguments[1]).getroot()

    with open(arrayOfArguments[2]) as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')

        for currentCSVRowNum, currentCSVRow in enumerate(csvReader):
            if currentCSVRowNum > 0:
                if csvRowNotInXML(currentCSVRow, currentFileObjXMLTreeRoot):
                    p('CSV Row not in XML')
                    currentFileObjXMLTreeRoot.append(currentCSVRow)
    
    p(currentFileObjXMLTreeRoot)



if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
	p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')



