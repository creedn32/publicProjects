print("Comment: Importing modules and setting up variables...")

#Things to do:
#
##Check if modules are already imported
##Listen for mouse click release


import sys
sys.path.append("..")

import gspread, pyautogui, datetime, creed_modules.creed_toolpack, pynput.mouse, win32api, win32con
from oauth2client.service_account import ServiceAccountCredentials

numLockChanged = False
pyautogui.PAUSE = 0
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
credentialsPath = "C:\\Users\\cnaylor\\Desktop\\Portable Procedures\\repos\\private_data\\post_journal_entries\\creds.json"


credentials = ServiceAccountCredentials.from_json_keyfile_name(credentialsPath, scope)
googleSheetApp = gspread.authorize(credentials)
googleSheetBankTransactions = googleSheetApp.open("Journal Entries To Post").worksheet("Bank Transactions")


def functionOnClick(x, y, button, pressed):
    print("Mouse clicked at {0}, {1} with {2} and pressed is {3}".format(x, y, button, pressed))
    listenerObj.stop()

if win32api.GetKeyState(win32con.VK_NUMLOCK) == 1:
    pyautogui.press("numlock")
    numLockChanged = True


print("Comment: Importing modules and setting up variables...Done.")


# with pynput.mouse.Listener(on_click=functionOnClick) as listenerObj:
#     print("Click on 'Maximize' to prepare window for posting...")
#     listenerObj.join()
#
# time.sleep(1)



with pynput.mouse.Listener(on_click=functionOnClick) as listenerObj:
    print("Click on 'Clear' to begin posting...")
    listenerObj.join()


row = 3

while googleSheetBankTransactions.cell(row, 1).value:

    print("Row " + str(row) + " will be populated into the Great Plains entry window.")

    for col in range(1, 10):

        numberTabs = 1
        string = googleSheetBankTransactions.cell(row, col).value


        if col == 1:
            if googleSheetBankTransactions.cell(row, col).value == "Enter Transaction":
                pyautogui.press(["down", "up", "up", "up"])
            elif googleSheetBankTransactions.cell(row, col).value == "Enter Receipt":
                pyautogui.press(["down", "up", "up", "up", "down"])

        elif col == 2:
            if googleSheetBankTransactions.cell(row, col).value == "Check":
                pyautogui.press(["down", "up", "up", "up"])
            if googleSheetBankTransactions.cell(row, col).value == "Cash":
                pyautogui.press(["down", "up", "up", "up", "down"])
            if googleSheetBankTransactions.cell(row, col).value == "Increase Adjustment":
                pyautogui.press(["down", "up", "up", "up", "down", "down"])
            if googleSheetBankTransactions.cell(row, col).value == "Decrease Adjustment":
                pyautogui.press(["down", "up", "up", "up", "down", "down", "down"])


        elif col == 3:
            dateObj = datetime.datetime.strptime(googleSheetBankTransactions.cell(row, col).value, "%m/%d/%Y")
            string = dateObj.strftime("%m%d%Y")

        elif col == 4:
            numberTabs = 2

        elif col == 7:
            numberTabs = 6


        elif col == 8:
            string = googleSheetBankTransactions.cell(row, col).value.replace("-", "")

            if googleSheetBankTransactions.cell(row, 1).value != "Enter Transaction" or (googleSheetBankTransactions.cell(row, 1).value == "Enter Transaction" and googleSheetBankTransactions.cell(row, 2).value != "Enter Transaction" not in ["Check", "Decrease Adjustment"]):
                numberTabs = 2



        if col in [7, 9]:
            string = googleSheetBankTransactions.cell(row, col).value.lstrip("$").replace(".", "").replace(",", "")


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


    row = row + 1


if numLockChanged:
    pyautogui.press("numlock")
