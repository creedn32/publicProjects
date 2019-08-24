import win32gui, win32process, psutil
import time



import sys
sys.path.append("..")
from creed_modules import creedFunctions


i = 0

while i <= 1:

    win32guiObj = win32gui
    win32guiObj.GetWindowText(win32guiObj.GetForegroundWindow())
    processID = win32process.GetWindowThreadProcessId(win32guiObj.GetForegroundWindow())
    if psutil.Process(processID[-1]).name() == "Executor.exe":
        print(psutil.Process(processID[-1]))

    # creedFunctions.printPythonInfo(win32gui)
    # creedFunctions.printPythonInfo(win32guiObj)
    # creedFunctions.printPythonInfo(win32guiObj.GetForegroundWindow())
    # creedFunctions.printPythonInfo(processID)
    # creedFunctions.printPythonInfo(processID[-1])
    # creedFunctions.printPythonInfo(psutil)



    time.sleep(3)

