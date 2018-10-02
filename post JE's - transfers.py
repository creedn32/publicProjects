print("Cmt: Importing modules...")

import sys, time, xlwings, pywinauto, pyautogui, win32api    

print("Cmt: Importing modules...Done.")


print("Cmt: Open and connect to file...")

pyautogui.PAUSE = .0
row = 583
filePath = ""
jeWb = xlwings.Book(filePath)
sheetBankTransfers = jeWb.sheets["Bank Transfers"]

for win in pywinauto.findwindows.find_elements():
    gpWinTitleShort = "Bank Transfer Entry"
    if win.name[:len(gpWinTitleShort)] == gpWinTitleShort:
        gpWinTitleFull = win.name                          

pywinauto.win32functions.SetForegroundWindow(pywinauto.findwindows.find_window(title=gpWinTitleFull))

print("Cmt: Open and connect to file...Done.")


while not (sheetBankTransfers.range(row, 1).value == None):

    if sheetBankTransfers.range(row, 1).color == None:

        print("Row " + str(row) + " will be entered.")

        pyautogui.press(["tab", "tab"])

        for x in range(1, 6):
            print("x is " + str(x))
            print(sheetBankTransfers.range(row, x).value)

            if x == 4:
                pyautogui.press("tab")

            if x == 1:
                string = ('%02d' % sheetBankTransfers.range(row, x).value.month) + ('%02d' % sheetBankTransfers.range(row, x).value.day) + str(sheetBankTransfers.range(row, x).value.year)
            else:
                string= str(sheetBankTransfers.range(row, x).value)

            for letter in string:
                pyautogui.press(letter)

            if x == 5:
                pyautogui.press("tab")
                
            pyautogui.press("tab")



        while True:
            if win32api.GetKeyState(0x01) == -127:
                print("left button clicked")
                time.sleep(1)
                break

    row = row + 1


