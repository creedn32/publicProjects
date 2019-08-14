print("Comment: Importing modules and setting up variables...")

#Things to do:
#
##Check if modules are already imported
##Listen for mouse click release


import sys
sys.path.append("..")

import gspread, pyautogui, datetime, creed_modules.creed_toolpack, pynput.mouse, win32api, win32con, os, time
from oauth2client.service_account import ServiceAccountCredentials


numLockChanged = False
pyautogui.PAUSE = 0
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
credentialsPath = os.path.abspath(os.path.join(os.curdir, "..\\private_data\\post_journal_entries\\myCredentials.json"))


credentialsObj = ServiceAccountCredentials.from_json_keyfile_name(credentialsPath, scope)
googleSheetApp = gspread.authorize(credentialsObj)
# googleSheetBankTransactions = googleSheetApp.open("Journal Entries To Post").worksheet("Bank Transactions")
googleSheetBankTransactions = googleSheetApp.open("Journal Entries To Post").worksheet("Bank Transactions - Recurring")
# googleSheetBankTransactions = googleSheetApp.open("Journal Entries To Post - Public").worksheet("Transactions")


def functionOnClick(x, y, button, pressed):
    print("Mouse clicked at {0}, {1} with {2} and pressed is {3}".format(x, y, button, pressed))
    listenerObj.stop()


if win32api.GetKeyState(win32con.VK_NUMLOCK) == 1:
    pyautogui.press("numlock")
    numLockChanged = True


print("Comment: Importing modules and setting up variables...Done.")


with pynput.mouse.Listener(on_click=functionOnClick) as listenerObj:
    print("Click on 'Clear' to begin posting...")
    listenerObj.join()


row = 9

while googleSheetBankTransactions.cell(row, 1).value:

    print("Row " + str(row) + " will be populated into the Great Plains entry window.")
    optionVar = googleSheetBankTransactions.cell(row, 1).value
    typeVar = googleSheetBankTransactions.cell(row, 2).value

    for col in range(1, 10):

        numberTabs = 1
        string = googleSheetBankTransactions.cell(row, col).value


        if col == 1:

            pyautogui.press(["down", "up", "up", "up"])

            if optionVar == "Enter Receipt":
                pyautogui.press("down")

        elif col == 2:

            pyautogui.press(["down", "up", "up", "up"])

            if typeVar == "Cash":
                pyautogui.press("down")
            elif typeVar == "Increase Adjustment":
                creed_modules.creed_toolpack.repetitiveKeyPress(2, "down")
            elif typeVar == "Decrease Adjustment":
                creed_modules.creed_toolpack.repetitiveKeyPress(3, "down")


        elif col == 3:
            dateObj = datetime.datetime.strptime(string, "%m/%d/%Y")
            string = dateObj.strftime("%m%d%Y")

        elif col == 4:
            numberTabs = 2

        elif col == 7:
            numberTabs = 6


        elif col == 8:
            string = string.replace("-", "")

            if optionVar != "Enter Transaction" or (optionVar == "Enter Transaction" and typeVar not in ["Check", "Decrease Adjustment"]):
                numberTabs = 2



        if col in [7, 9]:

            if len(string.split(".")) == 1:
                string = string + "00"

            string = string.lstrip("$").replace(".", "").replace(",", "")


        if col not in [1, 2]:

            for letter in string:

                if ord(letter) in (list(range(123, 127)) + list(range(94, 96)) + list(range(62, 91)) + [60, 58] + list(
                        range(40, 44)) + list(range(33, 39))):

                    pyautogui.PAUSE = .0000000000001
                    pyautogui.keyDown("shift")
                    pyautogui.press(letter)
                    pyautogui.keyUp("shift")
                    pyautogui.PAUSE = 0

                else:
                    pyautogui.press(letter)


        creed_modules.creed_toolpack.repetitiveKeyPress(numberTabs, "tab")


    with pynput.mouse.Listener(on_click=functionOnClick) as listenerObj:
        print("'Post' or 'Clear' this entry to continue...")
        listenerObj.join()

    time.sleep(1)
    row = row + 1


if numLockChanged:
    pyautogui.press("numlock")
