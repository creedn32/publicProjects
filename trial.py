from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
    creds = tools.run_flow(flow, store)
SHEETS = discovery.build('sheets', 'v4', http=creds.authorize(Http()))

SHEET_ID = ... # add your Sheet ID here
reqs = {'requests': [
    # frozen row 1
    {'updateSheetProperties': {
        'properties': {'gridProperties': {'frozenRowCount': 1}},
        'fields': 'gridProperties.frozenRowCount',
    }},
    # embolden row 1
    {'repeatCell': {
        'range': {'endRowIndex': 1},
        'cell': {'userEnteredFormat': {'textFormat': {'bold': True}}},
        'fields': 'userEnteredFormat.textFormat.bold',
    }},
    # currency format for column E (E2:E7)
    {'repeatCell': {
        'range': {
            'startRowIndex': 1,
            'endRowIndex': 6,
            'startColumnIndex': 4,
            'endColumnIndex': 5,
        },
        'cell': {
            'userEnteredFormat': {
                'numberFormat': {
                    'type': 'CURRENCY',
                    'pattern': '"$"#,##0.00',
                },
            },
        },
        'fields': 'userEnteredFormat.numberFormat',
    }},
    # validation for column F (F2:F7)
    {'setDataValidation': {
        'range': {
            'startRowIndex': 1,
            'endRowIndex': 6,
            'startColumnIndex': 5,
            'endColumnIndex': 6,
        },
        'rule': {
            'condition': {
                'type': 'ONE_OF_LIST',
                'values': [
                    {'userEnteredValue': 'PENDING'},
                    {'userEnteredValue': 'SHIPPED'},
                    {'userEnteredValue': 'DELIVERED'},
                ]
            },
            #'inputMessage': 'Select PENDING, SHIPPED, or DELIVERED',
            #'strict': True,
            'showCustomUi': True,
        },
    }},
]}

res = SHEETS.spreadsheets().batchUpdate(
        spreadsheetId=SHEET_ID, body=reqs).execute()