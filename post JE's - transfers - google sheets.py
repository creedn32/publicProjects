print("Comment: Importing modules, setting up variables, and grabbing window...")

import gspread, datetime, pywinauto, pyautogui, time
from oauth2client.service_account import ServiceAccountCredentials

pyautogui.PAUSE = 0
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
#credentialsPath = 'C:\\Users\\cnaylor\\Desktop\\testSheets\\creds.json'
credentialsPath = 'C:\\Users\\cnaylor.001\\Desktop\\testSheets\creds.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(credentialsPath, scope)
googleSheetApp = gspread.authorize(credentials)
gsheetJournalEntriesToPost = googleSheetApp.open('Journal Entries To Post').sheet1


gpWinTitleShort = "Bank Transfer Entry"

for win in pywinauto.findwindows.find_elements():
    
    #print(win.name[:len(gpWinTitleShort)])
    
    if win.name[:len(gpWinTitleShort)] == gpWinTitleShort:
        gpWinTitleFull = win.name 

#print(gpWinTitleFull)

pywinauto.win32functions.SetForegroundWindow(pywinauto.findwindows.find_window(title=gpWinTitleFull))

print("Comment: Importing modules, setting up variables, and grabbing window...Done.")


pyautogui.press(['tab', 'tab'])


row = 2

while gsheetJournalEntriesToPost.cell(row, 1).value:


    if row == 2:

        print("Row " + str(row) + " will be entered.")

        for col in range(1, 6):

            numberTabs = 1
            string = gsheetJournalEntriesToPost.cell(row, col).value

            if col == 1:
                dateObj = datetime.datetime.strptime(gsheetJournalEntriesToPost.cell(row, col).value, '%m/%d/%Y')
                #print(dateObj.strftime('%m').lstrip('0'))
                #print(dateObj.strftime('%m'))
                #print(dateObj.strftime('%d').lstrip('0'))
                #print(dateObj.strftime('%d'))
                #print(dateObj.strftime('%Y'))

                string = dateObj.strftime('%m%d%Y')

            elif col == 3:
                numberTabs = 2
                
            elif col == 4:
                string = gsheetJournalEntriesToPost.cell(row, col).value.lstrip('$').replace('.', '').replace(',', '')


            print(string)
            
            for letter in string:
                pyautogui.press(letter)

            for i in range(0, numberTabs):
                pyautogui.press('tab')


    row = row + 1




#prettyPrinter = pprint.PrettyPrinter()
# results = sheet.cell(2, 2).value
# pp.pprint(results)
#
# sheet.update_cell(2, 2, 'Loan Sweep Transaction')
# results = sheet.cell(2, 2).value
# pp.pprint(results)


