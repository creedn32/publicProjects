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
from pytz import timezone


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
        'date': '{dt.month}/{dt.day}/{dt.year} {dt.hour}:{dt.minute}'.format(dt = myPyFunc.unixStrToDateObjMST(element.get('date'))),
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
    sortOrderDesc = True
    dateColumnIndexCSV = 2
    minutesInTimeBand = 120
    minutesToAdjust = round(minutesInTimeBand/2)

    currentFileObjXMLTreeRoot = sorted(currentFileObjXMLTreeRoot, key=lambda x: int(x.get('date')), reverse=sortOrderDesc)
    # p(myPyFunc.unixStrToDateObjMST(currentFileObjXMLTreeRoot[0].get('date'))

    with open(pathStrToCSVFile) as csvFile:
        csvReader = list(csv.reader(csvFile, delimiter=','))[1:]

        for currentCSVRow in csvReader:
            currentCSVRow[dateColumnIndexCSV] = myPyFunc.addMSTToDateObj(datetime.strptime(currentCSVRow[dateColumnIndexCSV], '%m/%d/%Y %H:%M'))

        csvReader.sort(key=lambda x: x[dateColumnIndexCSV], reverse=sortOrderDesc)
        # p(csvReader[0][2])

        for currentCSVRow in csvReader:

            for currentElement in currentFileObjXMLTreeRoot:
                
                csvDateObjBefore = currentCSVRow[dateColumnIndexCSV] + timedelta(minutes=-minutesToAdjust)
                csvDateObjAfter = currentCSVRow[dateColumnIndexCSV] + timedelta(minutes=minutesToAdjust)
                timeToCompare = myPyFunc.unixStrToDateObjMST(currentElement.get('date'))

                if timeToCompare > csvDateObjBefore and timeToCompare < csvDateObjAfter:                    
                    p(currentCSVRow)
                    p(currentElement.attrib)


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



