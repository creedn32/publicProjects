from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
import _myPyFunc, subprocess, os


pathToPowerShellScript = Path(_myPyFunc.getParentalDirectory(pathToThisPythonFile, 'publicProjects'), 'shell', 'powershell', 'turnOffMonitor.ps1')
subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe', pathToPowerShellScript], cwd=os.getcwd())