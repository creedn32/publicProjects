# import win32gui, win32con
#
# import time
# import psutil


import pywinauto, sys
sys.path.append("..")
from creed_modules import creedFunctions


windowsExplorerApp = pywinauto.Application(backend="uia").connect(path="explorer.exe")
systemTrayObj = windowsExplorerApp.window(class_name="Shell_TrayWnd")
systemTrayObj.child_window(title="Executor").click()

creedFunctions.printPythonInfo(systemTrayObj.child_window(title="Executor"))




#
# executorApp = pywinauto.Application().connect(path = r"C:\Users\cnaylor\Desktop\Portable Applications\Other\Executor64bit\Executor64bit\Executor.exe")
#
#
# # for i in executorApp.windows():
# #     print(i)
#
# executorWindow = executorApp["hwndwrapper.DialogWrapper - 'Executor', TApplication"]
# executorWindow.Minimize()



# for i in pywinauto.findwindows.find_windows():
#     print(i)



# , win32process, psutil
# import time



# import sys
# sys.path.append("..")
# from creed_modules import creedFunctions


#
# for processObj in psutil.process_iter():
#     print(processObj.name())





# def enumHandler(hwnd, lParam):
#     if win32gui.GetWindowText(hwnd) == "Executor":
#         infoObj.windowToMaximize = hwnd
#         print(win32gui.GetWindowText(hwnd))
#         print(hwnd)
#         print(win32gui.IsWindowVisible(hwnd))
#
#
#
#
# class info():
#     def __init__(self, windowToMaximize):
#         self.windowToMaximize = windowToMaximize
#
# infoObj = info(None)
# win32gui.EnumWindows(enumHandler, None)



# win32gui.ShowWindow(198822, win32con.SW_MAXIMIZE)
# win32gui.ShowWindow(1246954, win32con.SW_MAXIMIZE)
# win32gui.SetForegroundWindow(1442984)









#
# i = 0
#
# while i <= 1:
#
#     win32guiObj = win32gui
#     win32guiObj.GetWindowText(win32guiObj.GetForegroundWindow())
#     processID = win32process.GetWindowThreadProcessId(win32guiObj.GetForegroundWindow())
#     if psutil.Process(processID[-1]).name() == "Executor.exe":
#         print(psutil.Process(processID[-1]))
#
#     # creedFunctions.printPythonInfo(win32gui)
#     # creedFunctions.printPythonInfo(win32guiObj)
#     # creedFunctions.printPythonInfo(win32guiObj.GetForegroundWindow())
#     # creedFunctions.printPythonInfo(processID)
#     # creedFunctions.printPythonInfo(processID[-1])
#     # creedFunctions.printPythonInfo(psutil)
#
#
#
#     time.sleep(3)

