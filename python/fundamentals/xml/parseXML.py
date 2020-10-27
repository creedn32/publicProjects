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

        if dataForActionObj['currentFileObj'].suffix == '.xml' and dataForActionObj['currentFileObj'].stem in ['try1']: #, 'try2']:

            currentFileObjXMLTreeRoot = et.parse(str(dataForActionObj['currentFileObj'])).getroot()
            
            p(dataForActionObj['currentFileObj'].name)
            p('Length of file being added: ' + str(len(currentFileObjXMLTreeRoot)))


            def buildNewRoot(dataForActionObj, root):
            
                def extendAndDeduplicate():
                    uniqueArray = myPyFunc.getUniqueArray(root)
                    p('Length of file after being deduplicated: ' + str(len(uniqueArray)))
                    dataForActionObj[xmlRootStr].extend(uniqueArray)
                    p('Length of accumulated file: ' + str(len(dataForActionObj[xmlRootStr])))
                    dataForActionObj[xmlRootStr] = removeDuplicatesFromRoot(dataForActionObj[xmlRootStr])
                    p('Length of accumulated file after deduplication: ' + str(len(dataForActionObj[xmlRootStr])))

                xmlRootStr = 'new' + root.tag.upper() + 'XMLTreeRoot'

                if currentFileObjXMLTreeRoot.tag == 'smses':
                    argumentToUse = 2
                else:
                    argumentToUse = 3

                if xmlRootStr in dataForActionObj:
                    extendAndDeduplicate()

                else:
                    dataForActionObj[xmlRootStr] = et.parse(arrayOfArguments[argumentToUse]).getroot()
                    extendAndDeduplicate()

            buildNewRoot(dataForActionObj, currentFileObjXMLTreeRoot)



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

    p(len(myPyFunc.onAllFileObjInTreeBreadthFirst(Path(arrayOfArguments[1]), actionToPerformOnEachFileObjInTree)['newSMSESXMLTreeRoot']))



if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
	p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')




