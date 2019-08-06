print("Comment: Importing modules, setting up variables, and grabbing window...")

import gspread, datetime, pyautogui, time, win32api
from oauth2client.service_account import ServiceAccountCredentials

pyautogui.PAUSE = 0
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
#credentialsPath = 'C:\\Users\\cnaylor\\Desktop\\testSheets\\creds.json'
credentialsPath = 'C:\\Users\\cnaylor.001\\Desktop\     \testSheets\creds.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(credentialsPath, scope)
googleSheetApp = gspread.authorize(credentials)
gsheetJournalEntriesToPost = googleSheetApp.open('Journal Entries To Post').sheet1


print("Comment: Importing modules, setting up variables, and grabbing window...Done.")


pyautogui.press(['tab', 'tab'])


# row = 2
#
# while gsheetJournalEntriesToPost.cell(row, 1).value:
#
#     print("Row " + str(row) + " will be entered.")
#
#     for col in range(1, 6):
#
#         numberTabs = 1
#         string = gsheetJournalEntriesToPost.cell(row, col).value
#
#         if col == 1:
#             dateObj = datetime.datetime.strptime(gsheetJournalEntriesToPost.cell(row, col).value, '%m/%d/%Y')
#             #print(dateObj.strftime('%m').lstrip('0'))
#             #print(dateObj.strftime('%m'))
#             #print(dateObj.strftime('%d').lstrip('0'))
#             #print(dateObj.strftime('%d'))
#             #print(dateObj.strftime('%Y'))
#
#             string = dateObj.strftime('%m%d%Y')
#
#         elif col == 3:
#             numberTabs = 2
#
#         elif col == 4:
#             string = gsheetJournalEntriesToPost.cell(row, col).value.lstrip('$').replace('.', '').replace(',', '')
#
#
#         print(string)
#
#         for letter in string:
#             pyautogui.press(letter)
#
#         for i in range(0, numberTabs):
#             pyautogui.press('tab')
#
#
#     while True:
#         if win32api.GetKeyState(0x01) == -127 or win32api.GetKeyState(0x01) == -128:
#             print("left button clicked")
#             time.sleep(4)
#             break
#
#
#     row = row + 1
#
#
#
#
#
