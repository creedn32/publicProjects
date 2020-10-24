from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(pathToThisPythonFile.parents[3]))
from herokuGorilla.backend.python.myPythonLibrary import myPyFunc

from pprint import pprint as p
import lxml.etree as et
from datetime import datetime



def getNewestTextElementCombine(currentReduceResult, element):
    
    if int(currentReduceResult.get('date')) > int(element.get('date')):
        return currentReduceResult
        
    return element


def getSMSCountCombine(currentReduceResult, element):

    if element.tag == 'sms':
        return currentReduceResult + 1

    return currentReduceResult



def getMMSCountCombine(currentReduceResult, element):

    if element.tag == 'mms':
        return currentReduceResult + 1

    return currentReduceResult



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


def getDuplicateElements(root):

    elementsCheckedForDuplicates = set()
    # The iter method does a recursive traversal

    for element in root:
        pass

        # Since the id is what defines a duplicate for you
        # if 'id' in element.attr:
        #     current = element.get('id')
        #     # In elementsCheckedForDuplicates already means it's a duplicate, remove it
        #     if current in elementsCheckedForDuplicates:
        #         element.getparent().remove(element)
        #     # Otherwise mark this ID as "elementsCheckedForDuplicates"
        #     else:
        #         elementsCheckedForDuplicates.add(current)


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

            p(getDuplicateElements(xmlTreeObjRoot))


    myPyFunc.onAllFileObjInDir(arrayOfArguments[1], performOnEachFileObj)

if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
	p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')




