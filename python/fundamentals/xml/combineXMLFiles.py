from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(pathToThisPythonFile.parents[3]))
from herokuGorilla.backend.python.myPythonLibrary import myPyFunc

from pprint import pprint as p
import lxml.etree as et
from datetime import datetime
import os


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

        elementItemsTuple = tuple(element.items())
        
        if elementItemsTuple not in checkedForDuplicatesSet:
            arrayOfUniques.append(element)
            checkedForDuplicatesSet.add(elementItemsTuple)

    for element in root:
        element.getparent().remove(element)

    root.extend(arrayOfUniques)

    return root


def mainFunction(arrayOfArguments):

    pathStrToTopOfFileTree = arrayOfArguments[1]
    pathStrToNewXMLFileFolder = arrayOfArguments[2]

    def actionToPerformOnEachFileObjInTree(dataForActionObj):

        if dataForActionObj['currentFileObj'].suffix == '.xml':   # and dataForActionObj['currentFileObj'].stem in ['sms-made-by-creed-20201010', 'sms-made-by-creed-20201015-20201019', 'calls-20200927034234']:    #['try1']: #, 'try2']:

            currentFileObjXMLTreeRoot = et.parse(str(dataForActionObj['currentFileObj'])).getroot()
            
            p(str(dataForActionObj['currentFileObj'])[-40:])
            
            if currentFileObjXMLTreeRoot.tag == 'smses':
                
                total = len(currentFileObjXMLTreeRoot) - myPyFunc.reduceArray(currentFileObjXMLTreeRoot, getSMSCountCombine, 0) - myPyFunc.reduceArray(currentFileObjXMLTreeRoot, getMMSCountCombine, 0)
                
                if total != 0:
                    p('Messages don\'t add up: ' + str(total))
                    sys.exit()

            newestTextElement = myPyFunc.reduceArray(currentFileObjXMLTreeRoot, getNewestTextElementCombine, currentFileObjXMLTreeRoot[0])
            newestTextDateInt = int(newestTextElement.get('date'))
            newestTextDateObj = myPyFunc.unixIntToDateObj(newestTextDateInt, 'US/Mountain')
            p(newestTextDateObj.strftime('%Y-%m-%d %I:%M:%S %p'))
            p(newestTextElement.get('contact_name'))
            p(newestTextElement.get('address'))
            p(newestTextElement.get('body'))
            p(newestTextDateInt)
            
            p(len(myPyFunc.filterArray(currentFileObjXMLTreeRoot, filterDateGreaterThanOct13)))


            def buildNewRoot(dataForActionObj, root):
            
                def extendAndDeduplicate():
                    p(root.tag + ', length of file being added: ' + str(len(currentFileObjXMLTreeRoot)))
                    uniqueArray = myPyFunc.getUniqueArrayOfObj(root)
                    p(root.tag + ', length of file after being deduplicated: ' + str(len(uniqueArray)))
                    dataForActionObj[xmlRootStr].extend(uniqueArray)
                    p(root.tag + ', length of accumulated file: ' + str(len(dataForActionObj[xmlRootStr])))
                    dataForActionObj[xmlRootStr] = removeDuplicatesFromRoot(dataForActionObj[xmlRootStr])
                    p(root.tag + ', length of accumulated file after deduplication: ' + str(len(dataForActionObj[xmlRootStr])))

                xmlRootStr = 'new' + root.tag.capitalize() + 'XMLTreeRoot'

                if xmlRootStr not in dataForActionObj:
                    dataForActionObj[xmlRootStr] = et.parse(pathStrToNewXMLFileFolder + '\\' + root.tag + 'XMLEmpty.xml').getroot()

                extendAndDeduplicate()

            buildNewRoot(dataForActionObj, currentFileObjXMLTreeRoot)


        return dataForActionObj

    def createXMLFile(returnedDataObj, tag):

        xmlTreeRootKey = 'new' + tag.capitalize() + 'XMLTreeRoot'
        fileToCreateStr = pathStrToNewXMLFileFolder + '\\' + tag + 'XML.xml'
        root = returnedDataObj[xmlTreeRootKey]
        
        myPyFunc.writeXML(fileToCreateStr, root)


    returnedDataObj = myPyFunc.onAllFileObjInTreeBreadthFirst(Path(pathStrToTopOfFileTree), actionToPerformOnEachFileObjInTree)
    
    for tag in ['smses', 'calls']:
        createXMLFile(returnedDataObj, tag)



if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
	p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')




