#add tkinter button to stop program
#insert bank transfer code from other file
#change from xlwings to VBA



print("Cmt: Importing modules...")

import time, xlwings, pywinauto, pyautogui, win32api, os, inspect    

print("execfile(\"" + inspect.getfile(inspect.currentframe()).encode('string-escape') + "\")")
print("Cmt: Importing modules...Done.")
print("Cmt: Open and connect to file...")

pyautogui.PAUSE = .005
# pyautogui.FAILSAFE = True
excelFilePath = "Y:\\Accounting\\12_Creed\\Controlling - Accounting\\Journal Entries\\JE\'s To Post.xlsx"
# excelFilePath = "C:\\Users\\cnaylor\\Desktop\\FileShare\\Accounting\\12_Creed\\Controlling - Accounting\\Journal Entries\\JE\'s To Post.xlsx"
excelWb = xlwings.Book(excelFilePath)
#excelSheetName = "Bank Transactions"
excelSheetName = "Bank Transactions - Recurring"
winTitleShort = "Bank Transaction Entry"
excelSheet = excelWb.sheets[excelSheetName]
row = 319
#row = 2


for win in pywinauto.findwindows.find_elements():
    
    if win.name[:len(winTitleShort)] == winTitleShort:
        winTitleFull = win.name                          

pywinauto.win32functions.SetForegroundWindow(pywinauto.findwindows.find_window(title=winTitleFull))

print("Cmt: Open and connect to file...Done.")


while not (excelSheet.range(row, 1).value == None and excelSheet.range(row, 8).value == None):

    if excelSheet.range(row, 1).color == None and (excelSheet.range(row, 1).value == "Enter Transaction" or excelSheet.range(row, 1).value == "Enter Receipt"):

        print("Row " + str(row) + " will be entered.")

        for currentColumn in range(1, 10):
        
            if currentColumn == 5:
                pyautogui.press("tab")


            if excelSheet.range(row, 2).value == "Increase Adjustment" or excelSheet.range(row, 2).value == "Check":
                if currentColumn == 8:
                    for tabCount in range(0, 5):
                        pyautogui.press("tab")

                if currentColumn == 9:
                    for tabCount in range(0, 1):
                        pyautogui.press("tab")
                                                   
            elif excelSheet.range(row, 2).value == "Decrease Adjustment":
                if currentColumn == 8:
                    for tabCount in range(0, 5):
                        pyautogui.press("tab")

                        

            for letter in str(excelSheet.range(row, currentColumn).value):
                if currentColumn == 1:
                    pyautogui.press(["down", "up", "up", "up"])
                    
                    if excelSheet.range(row, 1).value == "Enter Transaction":
                        break
                    elif excelSheet.range(row, 1).value == "Enter Receipt":
                        pyautogui.press(letter)
                        break

                if currentColumn == 2 and excelSheet.range(row, 1).value == "Enter Transaction":
                    pyautogui.press(letter)
                    break
                elif currentColumn == 2 and excelSheet.range(row, 1).value == "Enter Receipt":
                    break

                if currentColumn == 3 and letter == ".":
                    break
                
                pyautogui.press(letter)
    
            pyautogui.press("tab")


        while True:
            if win32api.GetKeyState(0x01) == -127 or win32api.GetKeyState(0x01) == -128:
                print("left button clicked")
                time.sleep(1.5)
                break

    row = row + 1









 #if currentColumn == 3 and len(str(int(excelSheet.range(row, currentColumn).value))) == 5:
             #   pyautogui.press("0")


#if not any(win.name[:4] == "Book" for win in pywinauto.findwindows.find_elements()):
#    blankWb = xlwings.Book()


#
# if 'pathlib' not in sys.modules:
#     import pathlib
#     print("Cmt: Opened pathlib.")
#
# pathlib = sys.modules["pathlib"]


# jeFile = sys.modules["pathlib"].Path(excelFilePath)

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
