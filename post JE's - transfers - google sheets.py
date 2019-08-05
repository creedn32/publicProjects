print("Comment: Importing modules and setting up variables...")

import gspread, datetime
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
#credentialsPath = 'C:\\Users\\cnaylor\\Desktop\\testSheets\\creds.json'
credentialsPath = 'C:\\Users\\cnaylor.001\\Desktop\\testSheets\creds.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(credentialsPath, scope)
googleSheetApp = gspread.authorize(credentials)
gsheetJournalEntriesToPost = googleSheetApp.open('Journal Entries To Post').sheet1

print("Comment: Importing modules and setting up variables...Done.")

#prettyPrinter = pprint.PrettyPrinter()
# results = sheet.cell(2, 2).value
# pp.pprint(results)
#
# sheet.update_cell(2, 2, 'Loan Sweep Transaction')
# results = sheet.cell(2, 2).value
# pp.pprint(results)


row = 2

while gsheetJournalEntriesToPost.cell(row, 1).value:


    if row == 2:

        print("Row " + str(row) + " will be entered.")

        for col in range(1, 6):

            if col == 1:
                dateObj = datetime.datetime.strptime(gsheetJournalEntriesToPost.cell(row, col).value, '%m/%d/%Y')
                #print(dateObj.strftime('%m').lstrip('0'))
                #print(dateObj.strftime('%m'))
                #print(dateObj.strftime('%d').lstrip('0'))
                #print(dateObj.strftime('%d'))
                #print(dateObj.strftime('%Y'))
                print(dateObj.strftime('%m%d%Y'))

            elif col == 4:
                print(gsheetJournalEntriesToPost.cell(row, col).value.lstrip('$').replace('.', '').replace(',', ''))
            else:
                print(gsheetJournalEntriesToPost.cell(row, col).value)

    row = row + 1

