from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(pathToThisPythonFile.parents[3]))
from herokuGorilla.backend.python.myPythonLibrary import myPyFunc

from pprint import pprint as p
import lxml.etree as et
from datetime import datetime



def countTags(xmlTreeObjRoot, tagToCount):

    count = 0

    for child in xmlTreeObjRoot:
        if child.tag == tagToCount:
            count = count + 1

    return count


def mainFunction(arrayOfArguments):

    def actionToPerform(fileObj):
        
        if fileObj.stem[0:3] == 'sms':

            p(fileObj.stem)
            xmlTreeObj = et.parse(str(fileObj))
            xmlTreeObjRoot = xmlTreeObj.getroot()

            rootLength = len(xmlTreeObjRoot)
            smsCount = countTags(xmlTreeObjRoot, 'sms')
            mmsCount = countTags(xmlTreeObjRoot, 'mms')

            p(rootLength)
            p(smsCount)
            p(mmsCount)
            p(rootLength - smsCount - mmsCount)

            newestTextTimeStamp = 0
            newestTextElement = None

            for child in xmlTreeObjRoot:
                if int(child.attrib['date']) > newestTextTimeStamp:
                    newestTextTimeStamp = int(child.attrib['date'])
                    newestTextElement = child

            # p(newestTextTimeStamp)
            newestTextDateObj = myPyFunc.addTimezoneToDateObj(myPyFunc.unixMillisecondsToDateObj(newestTextTimeStamp), 'US/Mountain')
            p(newestTextDateObj.strftime('%Y-%m-%d %I:%M:%S %p'))
            # p(newestTextElement.attrib['contact_name'])
            # p(newestTextElement.attrib['address'])
            # p(newestTextElement.attrib['body'])
            # p(newestTextElement.attrib['readable_date'])

    myPyFunc.onAllFileObjInDir(arrayOfArguments[1], actionToPerform)

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