print("Comment: Importing modules and setting up variables...")

import gspread, pyautogui, datetime, win32api, time
from oauth2client.service_account import ServiceAccountCredentials


pyautogui.PAUSE = 0
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
credentialsPath = 'C:\\Users\\cnaylor\\Desktop\\creds.json'


credentials = ServiceAccountCredentials.from_json_keyfile_name(credentialsPath, scope)
googleSheetApp = gspread.authorize(credentials)
googleSheetJournalEntries = googleSheetApp.open('Journal Entries To Post').worksheet('Transfer Entries')

def repetitiveKeyPress(numberOfTabs, keyToPress):
    for i in range(0, numberOfTabs):
        pyautogui.press(keyToPress)

print("Comment: Importing modules and setting up variables...Done.")


row = 2

while googleSheetJournalEntries.cell(row, 1).value:

    print("Row " + str(row) + " will be entered.")

    repetitiveKeyPress(2, 'tab')

    for col in range(1, 6):

        numberTabs = 1
        string = googleSheetJournalEntries.cell(row, col).value

        if col == 1:
            dateObj = datetime.datetime.strptime(googleSheetJournalEntries.cell(row, col).value, '%m/%d/%Y')
            #print(dateObj.strftime('%m').lstrip('0'))
            #print(dateObj.strftime('%m'))
            #print(dateObj.strftime('%d').lstrip('0'))
            #print(dateObj.strftime('%d'))
            #print(dateObj.strftime('%Y'))

            string = dateObj.strftime('%m%d%Y')

        elif col == 3:
            numberTabs = 2

        elif col == 4:
            string = googleSheetJournalEntries.cell(row, col).value.lstrip('$').replace('.', '').replace(',', '')


        # print(string)


        for letter in string:

            if ord(letter) in (list(range(123, 127)) + list(range(94, 96)) + list(range(62, 91)) + [60, 58] + list(range(40, 44)) + list(range(33, 39))):

                pyautogui.PAUSE = .0000000000001
                pyautogui.keyDown("shift")
                pyautogui.press(letter)
                pyautogui.keyUp("shift")
                pyautogui.PAUSE = 0

            else:
                pyautogui.press(letter)


        repetitiveKeyPress(numberTabs, 'tab')


    while True:

        keyPressed = win32api.GetKeyState(0x01)

        if keyPressed in [-127, -128]:
            print("left button clicked: " + str(keyPressed))
            time.sleep(.25)
            break





# from apiclient import discovery
# from httplib2 import Http
# from oauth2client import file, client, tools
#
# SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
# store = file.Storage('storage.json')
# creds = store.get()
# if not creds or creds.invalid:
#     flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
#     creds = tools.run_flow(flow, store)
# SHEETS = discovery.build('sheets', 'v4', http=creds.authorize(Http()))
#
# SHEET_ID = ... # add your Sheet ID here
# reqs = {'requests': [
#     # frozen row 1
#     {'updateSheetProperties': {
#         'properties': {'gridProperties': {'frozenRowCount': 1}},
#         'fields': 'gridProperties.frozenRowCount',
#     }},
#     # embolden row 1
#     {'repeatCell': {
#         'range': {'endRowIndex': 1},
#         'cell': {'userEnteredFormat': {'textFormat': {'bold': True}}},
#         'fields': 'userEnteredFormat.textFormat.bold',
#     }},
#     # currency format for column E (E2:E7)
#     {'repeatCell': {
#         'range': {
#             'startRowIndex': 1,
#             'endRowIndex': 6,
#             'startColumnIndex': 4,
#             'endColumnIndex': 5,
#         },
#         'cell': {
#             'userEnteredFormat': {
#                 'numberFormat': {
#                     'type': 'CURRENCY',
#                     'pattern': '"$"#,##0.00',
#                 },
#             },
#         },
#         'fields': 'userEnteredFormat.numberFormat',
#     }},
#     # validation for column F (F2:F7)
#     {'setDataValidation': {
#         'range': {
#             'startRowIndex': 1,
#             'endRowIndex': 6,
#             'startColumnIndex': 5,
#             'endColumnIndex': 6,
#         },
#         'rule': {
#             'condition': {
#                 'type': 'ONE_OF_LIST',
#                 'values': [
#                     {'userEnteredValue': 'PENDING'},
#                     {'userEnteredValue': 'SHIPPED'},
#                     {'userEnteredValue': 'DELIVERED'},
#                 ]
#             },
#             #'inputMessage': 'Select PENDING, SHIPPED, or DELIVERED',
#             #'strict': True,
#             'showCustomUi': True,
#         },
#     }},
# ]}
#
# res = SHEETS.spreadsheets().batchUpdate(
#         spreadsheetId=SHEET_ID, body=reqs).execute()
