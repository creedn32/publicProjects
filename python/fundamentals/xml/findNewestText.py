from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(pathToThisPythonFile.parents[3]))
from herokuGorilla.backend.python.myPythonLibrary import myPyFunc

from pprint import pprint as p
import lxml.etree as et
from datetime import datetime



def getNewestTextElementCombine(currentResultOfReduce, element):
    
    if int(currentResultOfReduce.get('date')) > int(element.get('date')):
        return currentResultOfReduce
        
    return element


def getSMSCountCombine(currentResultOfReduce, element):

    if element.tag == 'sms':
        return currentResultOfReduce + 1

    return currentResultOfReduce



def getMMSCountCombine(currentResultOfReduce, element):

    if element.tag == 'mms':
        return currentResultOfReduce + 1

    return currentResultOfReduce



def filterArray(array, test):

    passed = []

    for element in array:
        if test(element):
            passed.append(element)

    return passed


def dateGreaterThanOct13(element):

    if int(element.get('date')) >= 1602639501397:
        return True
    
    return False


def getUniqueArray(array):

    checkedForDuplicatesSet = set()
    uniqueArray = []

    for element in array:
        if element not in checkedForDuplicatesSet:
            uniqueArray.append(element)
            checkedForDuplicatesSet.add(element)
            
    return uniqueArray


def getArrayOfDuplicatedElements(array):
    
    checkedForDuplicatesSet = set()
    # dupes = []

    # for x in a:
    #     if x not in checkedForDuplicatesSet:
    #         checkedForDuplicatesSet[x] = 1
    #     else:
    #         if checkedForDuplicatesSet[x] == 1:
    #             dupes.append(x)
    #         checkedForDuplicatesSet[x] += 1



def mainFunction(arrayOfArguments):

    def performOnEachFileObj(fileObj):

        if fileObj.stem[0:3] == 'sms':

            p(fileObj.stem)
            xmlTreeObj = et.parse(str(fileObj))
            xmlTreeObjRoot = xmlTreeObj.getroot()

            rootLength = len(xmlTreeObjRoot)
            p(rootLength - myPyFunc.reduceArray(xmlTreeObjRoot, getSMSCountCombine, 0) - myPyFunc.reduceArray(xmlTreeObjRoot, getMMSCountCombine, 0))
            
            newestTextElement = myPyFunc.reduceArray(xmlTreeObjRoot, getNewestTextElementCombine, xmlTreeObjRoot[0])
            newestTextDateInt = int(newestTextElement.get('date'))
            newestTextDateObj = myPyFunc.addTimezoneToDateObj(myPyFunc.unixMillisecondsToDateObj(newestTextDateInt), 'US/Mountain')
            p(newestTextDateObj.strftime('%Y-%m-%d %I:%M:%S %p'))
            p(newestTextElement.get('contact_name'))
            p(newestTextElement.get('address'))
            p(newestTextElement.get('body'))
            p(newestTextDateInt)

            p(len(filterArray(xmlTreeObjRoot, dateGreaterThanOct13)))

            p(len(getUniqueArray(xmlTreeObjRoot)))


    myPyFunc.onAllFileObjInDir(arrayOfArguments[1], performOnEachFileObj)

if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
	p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')




