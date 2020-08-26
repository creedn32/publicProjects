from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
import _myPyFunc, subprocess, os, time
from runpy import run_path


pathToPowerShellScript = Path(_myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'publicProjects'), 'commandLineInterfaces', 'powershell', 'turnOffMonitor.ps1')
subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe', str(pathToPowerShellScript)], cwd=os.getcwd())


# time.sleep(5)
# run_path(str(Path(pathToThisPythonFile.parents[1], 'wakeUpForMorning', 'wakeUpForMorning.py')))


