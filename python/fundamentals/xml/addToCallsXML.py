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



def cleanPhoneNumber(phoneNumberStr):
    phoneNumberStr = phoneNumberStr.replace(' ', '').replace('+', '')

    return phoneNumberStr[1:] if phoneNumberStr.startswith('1') else phoneNumberStr


def csvRowMatchesElement(currentCSVRow, element):

    callType = element.get('type')

    if callType in ['1', '3', '5']:
        callType = 'Incoming'
    elif callType in ['2']:
        callType = 'Outgoing'
    
    if callType not in ['Incoming', 'Outgoing'] and int(element.get('date')) > 1559073522412:
        p('New Call Type Found')

    
    mappedElement = ['', cleanPhoneNumber(element.get('number')), element.get('date'), callType, '', element.get('duration')]
    p(mappedElement)

    for currentCSVColumnNum, currentCSVColumn in enumerate(currentCSVRow):
        if currentCSVColumn != 1:   #element[currentCSVColumnNum]:
            return False
    return True


def csvRowNotInXML(currentCSVRow, root):
    
    for element in root:
        if csvRowMatchesElement(currentCSVRow, element):
            return False
    return True


def mainFunction(arrayOfArguments):

    currentFileObjXMLTreeRoot = et.parse(arrayOfArguments[1]).getroot()

    with open(arrayOfArguments[2]) as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')

        for currentCSVRowNum, currentCSVRow in enumerate(csvReader):
            if currentCSVRowNum > 0:
                
                # if currentCSVRow[0] == 'Rob Shaw':
                #     p(currentCSVRow)
                
                if csvRowNotInXML(currentCSVRow, currentFileObjXMLTreeRoot):
                    pass
                    # p('CSV Row not in XML')
                    # currentFileObjXMLTreeRoot.append(currentCSVRow)
    
    p(len(currentFileObjXMLTreeRoot))
    # myPyFunc.writeXML(arrayOfArguments[1], currentFileObjXMLTreeRoot)



if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
	p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')



