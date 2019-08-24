import win32gui
import time
import psutil
import win32process
from pprint import pprint


i = 0

while i <= 1:
    time.sleep(3)
    pprint(win32gui)
    pprint(help(win32gui))
    pprint(dir(win32gui))

    win32guiObj = win32gui
    win32guiObj.GetWindowText(win32guiObj.GetForegroundWindow())
    processID = win32process.GetWindowThreadProcessId(win32guiObj.GetForegroundWindow())
    print(psutil.Process(processID[-1]).name())