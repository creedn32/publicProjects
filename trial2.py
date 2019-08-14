import sys
sys.path.append("..")

# from __future__ import print_function
import pickle
import os.path
import pprint, creed_modules.creed_toolpack
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
googleScopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of the spreadsheet.
spreadsheetID = "1uQezYVWkLZEvXzbprJPLRyDdyn04MdO-k6yaiyZPOx8"
rangeName = "Transfers"
credentialsPath = os.path.abspath(os.path.join(os.curdir, "..\\private_data\\post_journal_entries\\googleCredentials.json"))
tokenPath = os.path.abspath(os.path.join(os.curdir, "..\\private_data\\post_journal_entries\\googleToken.pickle"))

def main():

    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """

    credentialsObj = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.


    if os.path.exists(tokenPath):
        with open(tokenPath, "rb") as tokenObj:
            credentialsObj = pickle.load(tokenObj)

    # If there are no (valid) credentials available, let the user log in.

    if not credentialsObj or not credentialsObj.valid:
        if credentialsObj and credentialsObj.expired and credentialsObj.refresh_token:
            credentialsObj.refresh(Request())
        else:
            flowObj = InstalledAppFlow.from_client_secrets_file(credentialsPath, googleScopes)
            credentialsObj = flowObj.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tokenPath, "wb") as tokenObj:
            pickle.dump(credentialsObj, tokenObj)

    serviceObj = build("sheets", "v4", credentials=credentialsObj)

    # Call the Sheets API
    googleSheet = serviceObj.spreadsheets()
    result = googleSheet.values().get(spreadsheetId=spreadsheetID, range=rangeName).execute()
    googleSheetCells = result.get("values", [])


    for row in range(1, len(googleSheetCells)):

        print("Row " + str(row) + " will be populated into the Great Plains entry window.")

        # creed_modules.creed_toolpack.repetitiveKeyPress(2, "tab")

        for col in range(0, 5):
            numberTabs = 1
            string = googleSheetCells[row][col]
            print(string)






    # if not values:
    #     print("No data found.")
    # else:
    #     print("Name, Major:")
    #     for row in values:
    #         # Print columns A and E, which correspond to indices 0 and 4.
    #         print("%s, %s" % (row[0], row[4]))


if __name__ == "__main__":
    main()