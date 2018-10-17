#add tkinter button to stop program
#change from xlwings to VBA


print("Cmt: Importing modules...")

import time, xlwings, pywinauto, pyautogui, win32api, os, win32com.client
#import inspect    
#print("execfile(\"" + inspect.getfile(inspect.currentframe()).encode('string-escape') + "\")")

print("Cmt: Importing modules...Done.")

excelApp = win32com.client.gencache.EnsureDispatch('Excel.Application')
excelApp.DisplayAlerts = False
filePath = os.path.abspath(os.curdir)
fileName = "JE's To Post"
fileExtension = ".xlsx"

excelApp.Workbooks.Open(filePath + "\\" + fileName + fileExtension)
excelApp.Calculation = win32com.client.constants.xlCalculationManual

excelWb = excelApp.Workbooks(fileName + fileExtension)
excelBankTransactionsSheet = excelWb.Worksheets("Bank Transactions")

pyautogui.PAUSE = 0
# pyautogui.FAILSAFE = True

excelApp.Visible = True

print("Cmt: Open and connect to file...")

bankTransactionsRow = 2
bankTransactionsRow = 982




for win in pywinauto.findwindows.find_elements():
    gpWinTitleShort = "Bank Transaction Entry"
    if win.name[:len(gpWinTitleShort)] == gpWinTitleShort:
        gpWinTitleFull = win.name                          

pywinauto.win32functions.SetForegroundWindow(pywinauto.findwindows.find_window(title=gpWinTitleFull))

print("Cmt: Open and connect to file...Done.")





while excelBankTransactionsSheet.Cells(bankTransactionsRow, 1).Value:

    if excelBankTransactionsSheet.Cells(bankTransactionsRow, 1).Interior.Color == 16777215 and excelBankTransactionsSheet.Cells(bankTransactionsRow, 8).Value:
    
        print("Row " + str(bankTransactionsRow) + " will be entered.")
        

        for x in range(1, 10):
            print(excelBankTransactionsSheet.Cells(bankTransactionsRow, x).Value)
            if x == 3:
                string = ('%02d' % excelBankTransactionsSheet.Cells(bankTransactionsRow, x).Value.month) + ('%02d' % excelBankTransactionsSheet.Cells(bankTransactionsRow, x).Value.day) + str(excelBankTransactionsSheet.Cells(bankTransactionsRow, x).Value.year)
            else:
                string = str(excelBankTransactionsSheet.Cells(bankTransactionsRow, x).Value)

            
            if x == 1:
                if excelBankTransactionsSheet.Cells(bankTransactionsRow, x).Value == "Enter Transaction":
                    pyautogui.press(["down", "up", "up", "up"])
                elif excelBankTransactionsSheet.Cells(bankTransactionsRow, x).Value == "Enter Receipt":
                    pyautogui.press(["down", "up", "up", "up", "down"])
            elif x == 2:
                if excelBankTransactionsSheet.Cells(bankTransactionsRow, x).Value == "Check":
                    pyautogui.press(["down", "up", "up"])
                if excelBankTransactionsSheet.Cells(bankTransactionsRow, x).Value == "Cash":
                    pyautogui.press(["down", "up", "up", "down"])              
            else:
                for letter in string:
                    pyautogui.press(letter)



            if x == 4 or x == 8:
                pyautogui.press("tab")
                
            if x == 7:
                for x in range(1, 5):
                    pyautogui.press("tab")

                for letter in string:
                    pyautogui.press(letter)
                pyautogui.press("tab")

            pyautogui.press("tab")



        while True:
            if win32api.GetKeyState(0x01) == -127 or win32api.GetKeyState(0x01) == -128:
                print("left button clicked")
                time.sleep(1.5)
                break

    
    bankTransactionsRow = bankTransactionsRow + 1







##
##        for currentColumn in range(1, 10):
##        
##            if currentColumn == 5:
##                pyautogui.press("tab")
##
##
##            if excelSheet.range(row, 2).value == "Increase Adjustment" or excelSheet.range(row, 2).value == "Check":
##                if currentColumn == 8:
##                    for tabCount in range(0, 5):
##                        pyautogui.press("tab")
##
##                if currentColumn == 9:
##                    for tabCount in range(0, 1):
##                        pyautogui.press("tab")
##                                                   
##            elif excelSheet.range(row, 2).value == "Decrease Adjustment":
##                if currentColumn == 8:
##                    for tabCount in range(0, 5):
##                        pyautogui.press("tab")
##
##                        
##
##            for letter in str(excelSheet.range(row, currentColumn).value):
##                if currentColumn == 1:
##                    pyautogui.press(["down", "up", "up", "up"])
##                    
##                    if excelSheet.range(row, 1).value == "Enter Transaction":
##                        break
##                    elif excelSheet.range(row, 1).value == "Enter Receipt":
##                        pyautogui.press(letter)
##                        break
##
##                if currentColumn == 2 and excelSheet.range(row, 1).value == "Enter Transaction":
##                    pyautogui.press(letter)
##                    break
##                elif currentColumn == 2 and excelSheet.range(row, 1).value == "Enter Receipt":
##                    break
##
##                if currentColumn == 3 and letter == ".":
##                    break
##                
##                pyautogui.press(letter)




excelApp.DisplayAlerts = True
excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelWb.Save()
