from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(pathToThisPythonFile.parents[3]))
from herokuGorilla.backend.python.myPythonLibrary import myPyFunc

from pprint import pprint as p
import lxml.etree as etree
from datetime import datetime, timedelta
import os
import csv
from pytz import timezone


def cleanPhoneNumber(phoneNumberStr):

    for stringToReplace in [' ', '+', '(', ')', '-']:
        phoneNumberStr = phoneNumberStr.replace(stringToReplace, '')

    return phoneNumberStr[1:] if phoneNumberStr.startswith('1') else phoneNumberStr

def convertCallType(callTypeNumber):

    callTypeNumberToWord = {
        '1': 'Incoming',
        '2': 'Outgoing',
        '3': 'Missed',
        '5': 'Declined'
    }

    callType = callTypeNumberToWord[callTypeNumber]

    return callType


def csvRowMatchesElement(currentCSVRow, currentElement):

    minutesInTimeBand = 4
    minutesToAdjust = round(minutesInTimeBand/2)

    currentElementDateObj = myPyFunc.unixStrToDateObjMST(currentElement.get('date')).replace(tzinfo=None)
    csvDateObjBefore = currentCSVRow[2] + timedelta(minutes=-minutesToAdjust)
    csvDateObjAfter = currentCSVRow[2] + timedelta(minutes=minutesToAdjust)

    if currentCSVRow[1] == cleanPhoneNumber(currentElement.get('number')):
        if currentCSVRow[5] == currentElement.get('duration'):
            if currentCSVRow[3] == convertCallType(currentElement.get('type')):
                if currentElementDateObj > csvDateObjBefore and currentElementDateObj < csvDateObjAfter: 
                    return True
    
    return False


def csvRowInXML(currentCSVRow, root):

    for currentElement in root:
        if csvRowMatchesElement(currentCSVRow, currentElement):
            return currentElement.attrib

    return None


def addToCalls(pathStrToPriorCallsFile, pathStrToCSVFile):

    pathStrToNewCallsXML = str(Path(pathStrToPriorCallsFile).parents[0]) + '\callsWithCallLogAnalytics.xml'

    eTreeObj = etree.parse(pathStrToPriorCallsFile)
    rootObj = eTreeObj.getroot()


    sortOrderDesc = True
    dateColumnIndexCSV = 2
    phoneNumberColumnIndexCSV = 1
    durationColumnIndexCSV = 5
    callTypeColumnIndexCSV = 3

    callTypeWordToNumber = {
        'Incoming': '1',
        'Outgoing': '2',
        'Missed': '3',
        'Declined': '5'
    }

    rootObj[:] = sorted(rootObj, key=lambda x: int(x.get('date')), reverse=sortOrderDesc)


    with open(pathStrToCSVFile) as csvFile:
        csvReader = list(csv.reader(csvFile, delimiter=','))[1:]

        for currentCSVRow in csvReader:
            currentCSVRow[dateColumnIndexCSV] = datetime.strptime(currentCSVRow[dateColumnIndexCSV], '%m/%d/%Y %H:%M')
            currentCSVRow[phoneNumberColumnIndexCSV] = cleanPhoneNumber(currentCSVRow[phoneNumberColumnIndexCSV])

        csvReader.sort(key=lambda x: x[dateColumnIndexCSV], reverse=sortOrderDesc)

        elementsToAppend = []

        for currentCSVRow in csvReader:

            if not csvRowInXML(currentCSVRow, rootObj):
                # p('CSV')
                # p('This row is not in XML')
                # p(currentCSVRow)

                
                dataForElement = {
                    'number': currentCSVRow[phoneNumberColumnIndexCSV],
                    'type': callTypeWordToNumber[currentCSVRow[callTypeColumnIndexCSV]],
                    'date': myPyFunc.dateObjToUnixMillisecondsStr(currentCSVRow[dateColumnIndexCSV]),
                    'duration': currentCSVRow[durationColumnIndexCSV],
                    # 'notes': 'from csv'
                }

                elementToAppend = etree.Element('call')


                for attributeKey, attributeValue in dataForElement.items():
                    # print(attributeKey, attributeValue)
                    elementToAppend.set(attributeKey, attributeValue)

                elementsToAppend.append(elementToAppend)


            # if csvRowInXML(currentCSVRow, rootObj):
            #     p('CSV')
            #     p('This row is in XML')
            #     p(currentCSVRow)
            #     p('Element')
            #     p(csvRowInXML(currentCSVRow, rootObj))

    # p(len(rootObj))

    for elementToAppend in elementsToAppend:
        rootObj.append(elementToAppend)

    p(myPyFunc.getArrayOfDuplicatedElements(rootObj))

    myPyFunc.writeXML(pathStrToNewCallsXML, rootObj)
    # p(len(rootObj))

    myPyFunc.printTimeSinceImport()

    
    # def getPhoneNumber(element):
    #     return cleanPhoneNumber(element.get('number'))

    # def allCallsFromCSV(array):

    #     for element in array:
    #         if element.get('notes') != 'from csv':
    #             # p(element.attrib)
    #             return False
    #     return True

    # def printArray(array):
    #     if array and not allCallsFromCSV(array):
    #         p('Sequential calls with same phone number:')
    #         for element in array:
    #             p(element.attrib)


    # arrayOfSamePhoneNumber = []

    # for elementIndex, element in enumerate(rootObj):

    #     if elementIndex > 0:

    #         if getPhoneNumber(element) == getPhoneNumber(rootObj[elementIndex - 1]):

    #             if len(arrayOfSamePhoneNumber) == 0:

    #                 arrayOfSamePhoneNumber.append(rootObj[elementIndex - 1])

    #             arrayOfSamePhoneNumber.append(element)
            
    #         else:
    #             printArray(arrayOfSamePhoneNumber)
    #             arrayOfSamePhoneNumber = []

    # printArray(arrayOfSamePhoneNumber)

    # myPyFunc.printTimeSinceImport()


def mainFunction(arrayOfArguments):
    addToCalls(arrayOfArguments[1], arrayOfArguments[2])


if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
	p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')



