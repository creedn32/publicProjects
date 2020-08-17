from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'herokuGorilla', 'backend', 'python', 'myPythonLibrary')))
import _myPyFunc

import re, time
from pprint import pprint as p

def phraseNotInArrays(phraseToCheck, phrasesToExclude, partialPhrasesToExclude):

    for phraseFromArray in phrasesToExclude:
        # p(phraseFromArray)
        # p(phraseToCheck)

        if phraseFromArray.lower() == phraseToCheck:
            return False

    for phraseFromArray in partialPhrasesToExclude:
        if phraseFromArray.lower() in phraseToCheck:
            return False

    return True


startTime = time.time()
strOfTextFilePath = str(Path(pathToThisPythonFile.parents[4], 'organizingFiles', 'google', 'gmail', 'singleTextFile', 'singleTextFile.txt'))

with open(strOfTextFilePath, 'r', encoding='utf8') as fileObj:
    strToSearch = fileObj.read() #.replace('\n', '')

strToSearch = ''.join(strToSearch).lower()
# strToSearch = strToSearch[:1000000]


phrasesToExclude = ['audio', 'work', 'of', 'on', 'e', 'All', 'reading', 'Kindle', 'in', 'many', 'Note', 'quality', 'memory', 'favorite', 'the', 'five', 'major', 'my', 'bestselling', 'flagship', 'i', 'signed', 'help', 'by', 'more', 'used', 'cook', 'fitness', '400', 'BiggerPockets', 'leather', 'print', 'Audible', 'additional', 'newest', 'new', 'great', 'collectible', 'from', 'selling', 'text', 'rehab', 'browse', 'rare', 'for', 'nook', 'digital', 'free', 'read', 'photo', 'paperback', 'level', 'with', 'our', 'your', 's', 'hand', 'option', 'buying', 'Advantage', 'Owls', \
    'their', 'Dalton', 'papers', 'grid', 'rewards', 'hymn', 'two', 'pitch', 'atex', 'noble', ]

partialPhrasesToExclude = ['Quick', 'abe', 'BYU', 'thrift', 'discover', 'nevada', 'nook', 'kindle', 'world', 'noble', 'owls' ]

# phrasesToExclude = []
# partialPhrasesToExclude = []

# regExPattern = re.compile(r'(?i)(.{,20})(\s*books)(.{,20})')
# regExPattern = re.compile(r'(?i)(\s*)(\S*)(\s*)(books)(\s*)(.{,10})')
# regExPattern = re.compile(r'(?i)\b(?!Quick|audio|work|of|on|e|All|reading|Kindle|in|many|Note|Abe|quality|memory|favorite|the|five|major|my|bestselling|flagship|i|signed|help|by|more|used|cook|fitness|400|BiggerPockets|leather|print|Audible|additional|newest|new|great|collectible|from|selling|text|rehab|browse|rare|for|nook|digital|free|read|photo|paperback|level|with|our|your|s|hand|option|buying|noreplyface)\w+(?=\s?books)')
# findAllResults = re.findall(regExPattern, strToSearch)


arrayOfStartIndices = [i.start() for i in re.finditer('books', strToSearch)] 



# p(phraseNotInArrays('byu', phrasesToExclude, partialPhrasesToExclude))

count = 0
prefacesObj = {}

for startIndex in arrayOfStartIndices:

    strBegin = strToSearch[startIndex - 20:startIndex]
    strMiddle = strToSearch[startIndex:startIndex + 5]
    strEnd = strToSearch[startIndex + 5:startIndex + 25]

    strPreface = strBegin.rstrip()

    try:
        strPreface = strPreface[strPreface.rindex(' ') + 1:]
    except:
        pass


    if phraseNotInArrays(strPreface, phrasesToExclude, partialPhrasesToExclude):
        # p([strBegin, strMiddle, strEnd, strPreface])
        if strPreface not in prefacesObj:
            prefacesObj[strPreface] = 1
        else:
            prefacesObj[strPreface] = prefacesObj[strPreface] + 1
        count = count + 1


def lambdaReplacement(prefaceAndPrefaceCountTuple):
    return prefaceAndPrefaceCountTuple[1]


sortedObj = sorted(prefacesObj.items(), key=lambdaReplacement, reverse=True)

for i in sortedObj:
	print(i[0], i[1])

# p(prefacesObj)
p(count)
p(len(arrayOfStartIndices))

# p(prefacesObj.items())




bookstores = ['Advantage Books', 'Owls Books', 'Abe Books', 'Dalton Books', 'Barnes & Noble', 'thriftbooks', 'discover-books', 'nevada books', 'world books', 'big river', 'planet']

_myPyFunc.printElapsedTime(startTime, 'Done')
