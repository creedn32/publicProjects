from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
import _myPyFunc, subprocess, os, time, webbrowser


pathToPowerShellScript = Path(_myPyFunc.getParentalDirectory(pathToThisPythonFile, 'publicProjects'), 'shell', 'powershell', 'turnOffMonitor.ps1')
subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe', str(pathToPowerShellScript)], cwd=os.getcwd())


# time.sleep(5)
# webbrowser.open('https://www.youtube.com/embed/Xf5QTs2NLRc?start=1&fs=1&autoplay=1')
