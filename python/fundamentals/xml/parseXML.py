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



def filterDateGreaterThanOct13(element):

    if int(element.get('date')) >= 1602639501397:
        return True
    
    return False




def getUniqueArray(array):

    checkedForDuplicatesSet = set()
    arrayOfUniques = []

    for element in array:
        if element not in checkedForDuplicatesSet:
            arrayOfUniques.append(element)
            checkedForDuplicatesSet.add(element)
            
    return arrayOfUniques


def getArrayOfDuplicatedElements(array):
    
    checkedForDuplicatesSet = {}
    arrayOfDuplicates = []

    for element in array:
        if element not in checkedForDuplicatesSet:
            checkedForDuplicatesSet[element] = 1
        else:
            if checkedForDuplicatesSet[element] == 1:
                arrayOfDuplicates.append(element)
            checkedForDuplicatesSet[element] += 1

    return arrayOfDuplicates



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

            p(len(myPyFunc.filterArray(xmlTreeObjRoot, filterDateGreaterThanOct13)))
            p(len(getUniqueArray(xmlTreeObjRoot)))

            p(getArrayOfDuplicatedElements(xmlTreeObjRoot))



    myPyFunc.onAllFileObjInDir(arrayOfArguments[1], performOnEachFileObj)

if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
	p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')




