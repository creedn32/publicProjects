print("Comment: Importing modules and setting up variables...")

#Things to do:
#
##Check if modules are already imported


import sys
sys.path.append("..")

import gspread, pyautogui, datetime, creed_modules.creed_toolpack, pynput.mouse
from oauth2client.service_account import ServiceAccountCredentials


pyautogui.PAUSE = 0
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
credentialsPath = "C:\\Users\\creed\\Box Sync\\Developer\\PortableGit\\repos\\private_data\\post_journal_entries2\\creds.json"



credentials = ServiceAccountCredentials.from_json_keyfile_name(credentialsPath, scope)
googleSheetApp = gspread.authorize(credentials)
# googleSheetBankTransfers = googleSheetApp.open("Journal Entries To Post").worksheet("Bank Transfers")
googleSheetBankTransfers = googleSheetApp.open("Journal Entries To Post").sheet1



def functionOnClick(x, y, button, pressed):
    print("Mouse clicked at {0}, {1} with {2} and pressed is {3}".format(x, y, button, pressed))
    listenerObj.stop()


print("Comment: Importing modules and setting up variables...Done.")


with pynput.mouse.Listener(on_click=functionOnClick) as listenerObj:
    print("Click on 'Clear' to begin posting...")
    listenerObj.join()



row = 2

while googleSheetBankTransfers.cell(row, 1).value:

    print("Row " + str(row) + " will be populated into the Great Plains entry window.")

    creed_modules.creed_toolpack.repetitiveKeyPress(2, "tab")

    for col in range(1, 6):

        numberTabs = 1
        string = googleSheetBankTransfers.cell(row, col).value

        if col == 1:
            dateObj = datetime.datetime.strptime(string, "%m/%d/%Y")
            #print(dateObj.strftime('%m').lstrip('0'))
            #print(dateObj.strftime('%m'))
            #print(dateObj.strftime('%d').lstrip('0'))
            #print(dateObj.strftime('%d'))
            #print(dateObj.strftime('%Y'))

            string = dateObj.strftime("%m%d%Y")

        elif col == 3:
            numberTabs = 2

        elif col == 4:
            string = string.lstrip("$").replace(".", "").replace(",", "")


        for letter in string:

            if ord(letter) in (list(range(123, 127)) + list(range(94, 96)) + list(range(62, 91)) + [60, 58] + list(range(40, 44)) + list(range(33, 39))):

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


