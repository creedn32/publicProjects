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


def dateGreaterThanOct13():
    pass


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
            p(newestDateInt)

            # filterArray(xmlTreeObjRoot, dateGreaterThanOct13)


    myPyFunc.onAllFileObjInDir(arrayOfArguments[1], performOnEachFileObj)

if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
	p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')




# # Use a `set` to keep track of "visited" elements with good lookup time.
# visited = set()
# # The iter method does a recursive traversal
# for el in root.iter('element'):
#     # Since the id is what defines a duplicate for you
#     if 'id' in el.attr:
#         current = el.get('id')
#         # In visited already means it's a duplicate, remove it
#         if current in visited:
#             el.getparent().remove(el)
#         # Otherwise mark this ID as "visited"
#         else:
#             visited.add(current)