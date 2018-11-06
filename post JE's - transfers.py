#make entering data more uniform by using elif's and tabbing all after entering


print("Cmt: Importing modules...")

import os, pywinauto, pyautogui, win32com.client, time, win32api # sys   

print("Cmt: Importing modules...Done.")

excelApp = win32com.client.gencache.EnsureDispatch('Excel.Application')
excelApp.DisplayAlerts = False
filePath = os.path.abspath(os.curdir)
fileName = "JE's To Post"
fileExtension = ".xlsx"

excelApp.Workbooks.Open(filePath + "\\" + fileName + fileExtension)
excelApp.Calculation = win32com.client.constants.xlCalculationManual

excelWb = excelApp.Workbooks(fileName + fileExtension)
excelBankTransfersSheet = excelWb.Worksheets("Bank Transfers")

pyautogui.PAUSE = 0

print("Cmt: Open and connect to file...")

bankTransfersRow = 3
bankTransfersRow = 750


for win in pywinauto.findwindows.find_elements():
    gpWinTitleShort = "Bank Transfer Entry"
    if win.name[:len(gpWinTitleShort)] == gpWinTitleShort:
        gpWinTitleFull = win.name                          

pywinauto.win32functions.SetForegroundWindow(pywinauto.findwindows.find_window(title=gpWinTitleFull))

excelApp.Visible = True
print("Cmt: Open and connect to file...Done.")



while excelBankTransfersSheet.Cells(bankTransfersRow, 1).Value:

    #print(excelBankTransfersSheet.Cells(bankTransfersRow, 1).Interior.Color)

    if excelBankTransfersSheet.Cells(bankTransfersRow, 1).Interior.Color == 16777215:
    
        print("Row " + str(bankTransfersRow) + " will be entered.")
        
        pyautogui.press(["tab", "tab"])

        for x in range(1, 6):
            #print("x is " + str(x))
            print(excelBankTransfersSheet.Cells(bankTransfersRow, x).Value)


            if x == 1:
                #string = "090718"
                #string = ('%02d' % excelBankTransfersSheet.Cells(bankTransfersRow, x).Value.month) + ('%02d' % excelBankTransfersSheet.Cells(bankTransfersRow, x).Value.day) + str(excelBankTransfersSheet.Cells(bankTransfersRow, x).Value.year)
                string = ('%02d' % excelBankTransfersSheet.Cells(bankTransfersRow, x).Value.month) + ('%02d' % excelBankTransfersSheet.Cells(bankTransfersRow, x).Value.day) + str(excelBankTransfersSheet.Cells(bankTransfersRow, x).Value.year)
            else:
                string = str(excelBankTransfersSheet.Cells(bankTransfersRow, x).Value)


            if x == 4:
                pyautogui.press("tab")
                
            for letter in string:
                pyautogui.press(letter)

            #if x == 3:
                #pyautogui.press("tab")
            if x == 5:
                 pyautogui.press("tab")
                 pyautogui.press("tab")
                
            pyautogui.press("tab")


        print(1)
        excelBankTransfersSheet.Cells(bankTransfersRow, 1).EntireRow.Interior.Color = 5296274
        excelWb.Save()

        while True:
            if win32api.GetKeyState(0x01) == -127 or win32api.GetKeyState(0x01) == -128:
                print("left button clicked " + win32api.GetKeyState(0x01))
                time.sleep(1.5)
                break

    
    bankTransfersRow = bankTransfersRow + 1



excelApp.DisplayAlerts = True
excelApp.Calculation = win32com.client.constants.xlCalculationAutomatic
excelWb.Save()

