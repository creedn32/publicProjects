from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
import _myPyFunc

sys.path.append(str(Path(_myPyFunc.replacePartOfPath(pathToThisPythonFile.parents[0], 'publicProjects', 'privateData'))))
import phrase

import subprocess

subprocessObj = subprocess.Popen(['runas', '/noprofile', '/user:Administrator', 'NeedsAdminPrivilege.exe'], stdin=subprocess.PIPE)
subprocessObj.stdin.write(phrase.phrase)
subprocessObj.communicate()


# subprocess.Popen('cmder')