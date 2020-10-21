from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys

from pprint import pprint as p
import lxml.etree as et
from datetime import datetime



def mainFunction(arrayOfArguments):

    xmlTreeObj = et.parse(arrayOfArguments[1])
    xmlTreeObjRoot = xmlTreeObj.getroot()

    p('root length: ' + str(len(xmlTreeObjRoot)))
    counter = 0

    for child in xmlTreeObjRoot:
        dateStr = child.attrib['readable_date']

        if not (dateStr[0:4] == 'Oct ' and dateStr[6:12] == ', 2020'):
            # p(dateStr)
            child.getparent().remove(child)
            counter = counter + 1
            #  timeStamp = int(child.attrib['date'])//1000
            # p(timeStamp)
            # p(datetime.utcfromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S'))
            # p(child.attrib)
            # p(child)
            # if you encounter a "year is out of range" error the timestamp
            # may be in milliseconds, try `ts /= 1000` in that case
            # print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
    
    p(counter)
    p('root length: ' + str(len(xmlTreeObjRoot)))
    xmlTreeObj.write(arrayOfArguments[2], pretty_print=True, xml_declaration=True, encoding='utf-8')



if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
	p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')


