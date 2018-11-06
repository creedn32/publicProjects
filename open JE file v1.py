print("Comment: Importing modules...")

import sys, time, xlwings, pywinauto, pyautogui

print("Cmt: Importing modules...Done.")



print("Cmt: Open and connect to file...")

pyautogui.PAUSE = 0

filePath = ""
jeWb = xlwings.Book(filePath)
sheetBankTransactions = jeWb.sheets["Bank Transactions"]

for win in pywinauto.findwindows.find_elements():
    if win.name[:4] == "JE's":
        excelTitle = win.name
        print(excelTitle)


if not any(win.name[:4] == "Book" for win in pywinauto.findwindows.find_elements()):
    blankWb = xlwings.Book()


for win in pywinauto.findwindows.find_elements():
    if win.name[:4] == "Book":
        blankExcelTitle = win.name
        print(blankExcelTitle)


# pywinauto.win32functions.SetForegroundWindow(pywinauto.findwindows.find_window(title=excelTitle))
pywinauto.win32functions.SetForegroundWindow(pywinauto.findwindows.find_window(title=blankExcelTitle))

print("Cmt: Open and connect to file...Done.")




row = 733

while not (sheetBankTransactions.range(row, 1).value == None and sheetBankTransactions.range(row, 8).value == None):

    if sheetBankTransactions.range(row, 1).color == None:

        print("Row " + str(row) + " is white")

        time.sleep(1)

        for x in range(1, 9):

            for letter in str(sheetBankTransactions.range(row, x).value):
                pyautogui.press(letter)

            pyautogui.press('tab')

    row = row + 1



























#
#
# if 'pathlib' not in sys.modules:
#     import pathlib
#     print("Cmt: Opened pathlib.")
#
# pathlib = sys.modules["pathlib"]


# jeFile = sys.modules["pathlib"].Path(filePath)

# pywinauto.Application().connect(title=blankExcelTitle).window(title=blankExcelTitle).SetFocus()
# pywinauto.Application().connect(title=excelTitle).window(title=excelTitle).SetFocus()

# pyautogui.press(['u'])
        
# excelWindow = excelApp.window(title=excelTitle)
# excelWindow.SetFocus()
# import os

# if 'os' not in sys.modules:
#     import os
#     print("Cmt: Opened os.")


# if 'pyautogui' not in sys.modules:
#     import pyautogui

# import subprocess
# startProcessPath = "C:\\Windows\\System32\\calc.exe"
# startProcessPathFile = sys.modules["pathlib"].Path(startProcessPath)
#
# if startProcessPathFile.is_file():
#     print("The following file exists! " + startProcessPath)
#     subprocess.Popen(startProcessPath)

#
# if 'xlwings' not in sys.modules:
#     import xlwings
#
#     print("Cmt: Opened xlwings.")
#
# if 'pywinauto' not in sys.modules:
#     import pywinauto
#
#     print("Cmt: Opened pywinauto.")
#
# if 'pyautogui' not in sys.modules:
#     import pyautogui
#
#     print("Cmt: Opened pyautogui.")
