from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(pathToThisPythonFile.parents[3]))
from herokuGorilla.backend.python.myPythonLibrary import myPyFunc

from pprint import pprint as p
import lxml.etree as et
from datetime import datetime, timedelta
import os
import csv



def cleanPhoneNumber(phoneNumberStr):
    phoneNumberStr = phoneNumberStr.replace(' ', '').replace('+', '')

    return phoneNumberStr[1:] if phoneNumberStr.startswith('1') else phoneNumberStr


def csvRowMatchesElement(currentCSVRow, element):

    csvRowObj = {
        'person': [currentCSVRow[0], cleanPhoneNumber(currentCSVRow[1])],
        'date':  currentCSVRow[2],
        'callType': currentCSVRow[3],
        'duration': currentCSVRow[5]
    }

    callType = element.get('type')

    if callType in ['1', '3', '5']:
        callType = 'Incoming'
    elif callType in ['2']:
        callType = 'Outgoing'

    if callType not in ['Incoming', 'Outgoing']:
        p('New Call Type Found')

    elementObj = {
        'person': [element.get('name'), cleanPhoneNumber(element.get('number'))],
        'date': '{dt.month}/{dt.day}/{dt.year} {dt.hour}:{dt.minute}'.format(dt = myPyFunc.unixIntToDateObj(int(element.get('date')), 'US/Mountain')),
        'callType': callType,
        'duration': element.get('duration')
    }

    # p('csvRow')
    # p(csvRowObj)
    # p('element')
    # p(elementObj)

    for csvKey, csvValue in csvRowObj.items():
        if isinstance(csvValue, list):
            if elementObj[csvKey] not in csvValue:
                return False
        else:
            if elementObj[csvKey] != csvKey:
                return False

    return True



def csvRowNotInXML(currentCSVRow, root):
    
    for element in root:
        if csvRowMatchesElement(currentCSVRow, element):
            return False
    return True


def mainFunction(arrayOfArguments):

    pathStrToCallsXMLFile = arrayOfArguments[1]
    pathStrToCSVFile = arrayOfArguments[2]
    currentFileObjXMLTreeRoot = et.parse(pathStrToCallsXMLFile).getroot()

    with open(pathStrToCSVFile) as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')

        for currentCSVRowNum, currentCSVRow in enumerate(csvReader):

            if currentCSVRowNum > 0:

                csvDateObj = datetime.strptime(currentCSVRow[2], '%m/%d/%Y %H:%M')
                csvDateObjFiveBefore = csvDateObj + timedelta(minutes=-5)
                csvDateObjFiveAfter = csvDateObj + timedelta(minutes=5)
                timeToCompare = datetime(2014, 7, 2, 13, 8)

                if timeToCompare > csvDateObjFiveBefore and timeToCompare < csvDateObjFiveAfter:
                    p(currentCSVRow[2])
                    p(csvDateObj)
                    p(csvDateObjFiveBefore)
                    p(csvDateObjFiveAfter)


                # if csvRowNotInXML(currentCSVRow, currentFileObjXMLTreeRoot):
                #     pass
                    # p(currentCSVRow)
                    # p('CSV Row not in XML')
                    # currentFileObjXMLTreeRoot.append(currentCSVRow)
    
    p(len(currentFileObjXMLTreeRoot))
    # myPyFunc.writeXML(pathStrToCallsXMLFile, currentFileObjXMLTreeRoot)



if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
	p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')



