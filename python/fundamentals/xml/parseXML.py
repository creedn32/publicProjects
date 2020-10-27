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


def removeDuplicatesFromRoot(root):
    
    checkedForDuplicatesSet = set()
    arrayOfUniques = []

    for element in root:
        if element not in checkedForDuplicatesSet:
            arrayOfUniques.append(element)
            checkedForDuplicatesSet.add(element)

    for element in root:
        element.getparent().remove(element)

    root.extend(arrayOfUniques)
    return root

def mainFunction(arrayOfArguments):

    def actionToPerformOnEachFileObjInTree(dataForActionObj):

        if dataForActionObj['currentFileObj'].suffix == '.xml' and dataForActionObj['currentFileObj'].stem in ['sms-made-by-creed-20201010', 'sms-made-by-creed-20201015-20201019']:

            currentFileObjXMLTreeRoot = et.parse(str(dataForActionObj['currentFileObj'])).getroot()
            
            p(dataForActionObj['currentFileObj'].name)
            p(len(currentFileObjXMLTreeRoot))
            
            if currentFileObjXMLTreeRoot.tag == 'smses':
                if 'newMessagesXMLTreeRoot' in dataForActionObj:
                    dataForActionObj['newMessagesXMLTreeRoot'].extend(myPyFunc.getUniqueArray(currentFileObjXMLTreeRoot))
                else:
                    dataForActionObj['newMessagesXMLTreeRoot'] = et.parse(arrayOfArguments[2]).getroot()
                    dataForActionObj['newMessagesXMLTreeRoot'].extend(myPyFunc.getUniqueArray(currentFileObjXMLTreeRoot))

            elif currentFileObjXMLTreeRoot.tag == 'calls':
                if 'newMessagesXMLTreeRoot' in dataForActionObj:
                    dataForActionObj['newMessagesXMLTreeRoot'].append('<hey>')
                else:
                    dataForActionObj['newMessagesXMLTreeRoot'] = et.parse(arrayOfArguments[3]).getroot()


        #     p('newXMLTreeRoot: ')
        #     p(len(newXMLTreeRoot))
        #     newXMLTreeRoot.extend(myPyFunc.getUniqueArray(currentFileObjXMLTreeRoot))
        #     p(len(removeDuplicatesFromRoot(newXMLTreeRoot)))

        return dataForActionObj
            
            # p(currentFileObjXMLTreeRoot.tag)
            # p(len(newMessagesXMLTreeRoot))
            # p(len(newCallsXMLTreeRoot))
            # p(rootLength - myPyFunc.reduceArray(currentFileObjXMLTreeRoot, getSMSCountCombine, 0) - myPyFunc.reduceArray(currentFileObjXMLTreeRoot, getMMSCountCombine, 0))
            
            # newestTextElement = myPyFunc.reduceArray(currentFileObjXMLTreeRoot, getNewestTextElementCombine, currentFileObjXMLTreeRoot[0])
            # newestTextDateInt = int(newestTextElement.get('date'))
            # newestTextDateObj = myPyFunc.addTimezoneToDateObj(myPyFunc.unixMillisecondsToDateObj(newestTextDateInt), 'US/Mountain')
            # p(newestTextDateObj.strftime('%Y-%m-%d %I:%M:%S %p'))
            # p(newestTextElement.get('contact_name'))
            # p(newestTextElement.get('address'))
            # p(newestTextElement.get('body'))
            # p(newestTextDateInt)

            # p(len(myPyFunc.filterArray(currentFileObjXMLTreeRoot, filterDateGreaterThanOct13)))
            # p(len(myPyFunc.getUniqueArray(currentFileObjXMLTreeRoot)))

            # p(myPyFunc.getArrayOfDuplicatedElements(currentFileObjXMLTreeRoot))

    p(len(myPyFunc.onAllFileObjInTreeBreadthFirst(Path(arrayOfArguments[1]), actionToPerformOnEachFileObjInTree)['newMessagesXMLTreeRoot']))



if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
	p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')




