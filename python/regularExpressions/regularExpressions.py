from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'herokuGorilla', 'backend', 'python', 'myPythonLibrary')))
import _myPyFunc

import re, time
from pprint import pprint as p


startTime = time.time()


strOfTextFilePath = str(Path(pathToThisPythonFile.parents[4], 'organizingFiles', 'google', 'gmail', 'singleTextFile', 'singleTextFile.txt'))

with open(strOfTextFilePath, 'r', encoding='utf8') as fileObj:
    strToSearch = fileObj.read() #.replace('\n', '')

strToSearch = ''.join(strToSearch)
# strToSearch = strToSearch[:1000000]


regExPattern = re.compile(r'(?i)(.{,20})(\s*books)(.{,20})')
# regExPattern = re.compile(r'(?i)(\s*)(\S*)(\s*)(books)(\s*)(.{,10})')
# regExPattern = re.compile(r'(?i)\b(?!Quick|audio|work|of|on|e|All|reading|Kindle|in|many|Note|Abe|quality|memory|favorite|the|five|major|my|bestselling|flagship|i|signed|help|by|more|used|cook|fitness|400|BiggerPockets|leather|print|Audible|additional|newest|new|great|collectible|from|selling|text|rehab|browse|rare|for|nook|digital|free|read|photo|paperback|level|with|our|your|s|hand|option|buying|noreplyface)\w+(?=\s?books)')


phrasesToExclude = ['Quick', 'audio', 'work', 'of', 'on', 'e', 'All', 'reading', 'Kindle', 'in', 'many', 'Note', 'Abe', 'quality', 'memory', 'favorite', 'the', 'five', 'major', 'my', 'bestselling', 'flagship', 'i', 'signed', 'help', 'by', 'more', 'used', 'cook', 'fitness', '400', 'BiggerPockets', 'leather', 'print', 'Audible', 'additional', 'newest', 'new', 'great', 'collectible', 'from', 'selling', 'text', 'rehab', 'browse', 'rare', 'for', 'nook', 'digital', 'free', 'read', 'photo', 'paperback', 'level', 'with', 'our', 'your', 's', 'hand', 'option', 'buying', 'Advantage', 'Owls']
phrasesToExcludeLowerCase = [x.lower() for x in phrasesToExclude]



for match in re.findall(regExPattern, strToSearch):
    matchList = list(match)

    try:
        matchList.append(match[0][match[0].rindex(' ') + 1:])
    except:
        matchList.append(match[0])

    if matchList[3].lower() not in phrasesToExcludeLowerCase:
        p(matchList)


bookstores = ['Advantage Books', 'Owls Books', 'Abe Books']

_myPyFunc.printElapsedTime(startTime, 'Done')
