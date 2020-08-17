from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'herokuGorilla', 'backend', 'python', 'myPythonLibrary')))
import _myPyFunc

import re, time
from pprint import pprint as p

def phraseNotInArrays(phraseToCheck, phrasesToExclude, partialPhrasesToExclude):

    for phraseFromArray in phrasesToExclude:
        if phraseFromArray.lower() == phraseToCheck.lower():
            return False

    for phraseFromArray in partialPhrasesToExclude:
        if phraseFromArray.lower() in phraseToCheck.lower():
            return False

    return True


startTime = time.time()
strOfTextFilePath = str(Path(pathToThisPythonFile.parents[4], 'organizingFiles', 'google', 'gmail', 'singleTextFile', 'singleTextFile.txt'))

with open(strOfTextFilePath, 'r', encoding='utf8') as fileObj:
    strToSearch = fileObj.read() #.replace('\n', '')

strToSearch = ''.join(strToSearch)
strToSearch = strToSearch[:1000]


phrasesToExclude = ['audio', 'work', 'of', 'on', 'e', 'All', 'reading', 'Kindle', 'in', 'many', 'Note', 'Abe', 'quality', 'memory', 'favorite', 'the', 'five', 'major', 'my', 'bestselling', 'flagship', 'i', 'signed', 'help', 'by', 'more', 'used', 'cook', 'fitness', '400', 'BiggerPockets', 'leather', 'print', 'Audible', 'additional', 'newest', 'new', 'great', 'collectible', 'from', 'selling', 'text', 'rehab', 'browse', 'rare', 'for', 'nook', 'digital', 'free', 'read', 'photo', 'paperback', 'level', 'with', 'our', 'your', 's', 'hand', 'option', 'buying', 'Advantage', 'Owls' \
    'BYU', 'their', 'Dalton']

partialPhrasesToExclude = ['Quick']

# phrasesToExclude = []
# partialPhrasesToExclude = []

# regExPattern = re.compile(r'(?i)(.{,20})(\s*books)(.{,20})')
# regExPattern = re.compile(r'(?i)(\s*)(\S*)(\s*)(books)(\s*)(.{,10})')
# regExPattern = re.compile(r'(?i)\b(?!Quick|audio|work|of|on|e|All|reading|Kindle|in|many|Note|Abe|quality|memory|favorite|the|five|major|my|bestselling|flagship|i|signed|help|by|more|used|cook|fitness|400|BiggerPockets|leather|print|Audible|additional|newest|new|great|collectible|from|selling|text|rehab|browse|rare|for|nook|digital|free|read|photo|paperback|level|with|our|your|s|hand|option|buying|noreplyface)\w+(?=\s?books)')
# findAllResults = re.findall(regExPattern, strToSearch)


# using re.finditer() 
# All occurrences of substring in string  
res = [i.start() for i in re.finditer('books', strToSearch.lower())] 

# printing result  
print("The start indices of the substrings are : " + str(res)) 




# for match in findAllResults:
#     matchList = list(match)

#     try:
#         matchList.append(match[0][match[0].rindex(' ') + 1:])
#     except:
#         matchList.append(match[0])

#     if phraseNotInArrays(matchList[3].lower(), phrasesToExclude, partialPhrasesToExclude):
#         p(matchList)

# p(len(findAllResults))

bookstores = ['Advantage Books', 'Owls Books', 'Abe Books', 'Dalton Books']

_myPyFunc.printElapsedTime(startTime, 'Done')
