#add tkinter button to stop program
#change from xlwings to VBA


print("Cmt: Importing modules...")

import time, xlwings, pywinauto, pyautogui, win32api, os, win32com.client
#import inspect    
#print("execfile(\"" + inspect.getfile(inspect.currentframe()).encode('string-escape') + "\")")

print("Cmt: Importing modules...Done.")
print("Cmt: Open and connect to file...")

excelApp = win32com.client.gencache.EnsureDispatch('Excel.Application')
excelApp.Visible = True
excelApp.DisplayAlerts = False

filePath = os.path.abspath(os.curdir)
fileName = "JE's To Post"
fileExtension = ".xlsx"
excelApp.Workbooks.Open(filePath + "\\" + fileName + fileExtension)

pyautogui.PAUSE = 0
# pyautogui.FAILSAFE = True
bankTransactionsRow = 2

excelApp.Calculation = win32com.client.constants.xlCalculationManual
excelWb = excelApp.Workbooks(fileName + fileExtension)
excelBankTransactionsSheet = excelWb.Worksheets("Bank Transactions")
#excelBankTransactionsSheet = excelWb.Worksheets("Bank Transactions - Recurring")
bankTransactionsRow = 1314
#bankTransactionsRow = 514

for win in pywinauto.findwindows.find_elements():
    gpWinTitleShort = "Bank Transaction Entry"
    if win.name[:len(gpWinTitleShort)] == gpWinTitleShort:
        gpWinTitleFull = win.name                          

pywinauto.win32functions.SetForegroundWindow(pywinauto.findwindows.find_window(title=gpWinTitleFull))


print("Cmt: Open and connect to file...Done.")


while excelBankTransactionsSheet.Cells(bankTransactionsRow, 1).Value or excelBankTransactionsSheet.Cells(bankTransactionsRow, 7).Value:

    if excelBankTransactionsSheet.Cells(bankTransactionsRow, 1).Interior.Color == 16777215 and excelBankTransactionsSheet.Cells(bankTransactionsRow, 8).Value:
    
        print("Row " + str(bankTransactionsRow) + " will be entered.")
        debitFirst = True
        

        for x in range(1, 10):

            string = str(excelBankTransactionsSheet.Cells(bankTransactionsRow, x).Value)

            if x == 3:
                string = ('%02d' % excelBankTransactionsSheet.Cells(bankTransactionsRow, x).Value.month) + ('%02d' % excelBankTransactionsSheet.Cells(bankTransactionsRow, x).Value.day) + str(excelBankTransactionsSheet.Cells(bankTransactionsRow, x).Value.year)
            elif str(excelBankTransactionsSheet.Cells(bankTransactionsRow, x).Value) == "None":
                string = ""

            
            if x == 1:
                if excelBankTransactionsSheet.Cells(bankTransactionsRow, x).Value == "Enter Transaction":
                    pyautogui.press(["down", "up", "up", "up"])
                elif excelBankTransactionsSheet.Cells(bankTransactionsRow, x).Value == "Enter Receipt":
                    pyautogui.press(["down", "up", "up", "up", "down"])
            elif x == 2:
                if excelBankTransactionsSheet.Cells(bankTransactionsRow, x).Value == "Check":
                    pyautogui.press(["down", "up", "up", "up"])
                if excelBankTransactionsSheet.Cells(bankTransactionsRow, x).Value == "Cash":
                    pyautogui.press(["down", "up", "up", "up", "down"])
                if excelBankTransactionsSheet.Cells(bankTransactionsRow, x).Value == "Increase Adjustment":
                    pyautogui.press(["down", "up", "up", "up", "down", "down"])
                if excelBankTransactionsSheet.Cells(bankTransactionsRow, x).Value == "Decrease Adjustment":
                    debitFirst = False
                    pyautogui.press(["down", "up", "up", "up", "down", "down", "down"])
            else:
                for letter in string:
                    pyautogui.press(letter)


            extraTabs = 1
            
            if x == 4:
                extraTabs = 2 #extra tabs after entering Checkbook ID
            elif x == 7:
                extraTabs = 6 #extra tabs after entering amount
            elif x == 8 and debitFirst:
                extraTabs = 2 #extra tabs after entering GL Account       

            for i in range(1, extraTabs + 1):
                pyautogui.press("tab")

 
        while True:
            if win32api.GetKeyState(0x01) == -127 or win32api.GetKeyState(0x01) == -128:
                print("left button clicked")
                time.sleep(4)
                break

    
    bankTransactionsRow = bankTransactionsRow + 1


excelApp.DisplayAlerts = True
excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelWb.Save()
