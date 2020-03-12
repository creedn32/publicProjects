print("Comment: Importing modules and setting up variables...")
import time
startTime = time.time()


import pathlib, pickle, os.path, googleapiclient.discovery, google_auth_oauthlib.flow, google.auth.transport.requests
from pprint import pprint as pp

credentialsPath = pathlib.Path(pathlib.Path.cwd().parents[3], "privateData", "python", "googleCredentials", "googleCredentials.json")
pp(credentialsPath)
# credentialsPath = str(pathlib.Path.cwd().parents[3]) + "/privateData/python/googleCredentials/googleCredentials.json"
tokenPath = str(pathlib.Path.cwd().parents[3]) + "/privateData/python/googleCredentials/googleToken.pickle"
googleScopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentialsObj = None

if os.path.exists(tokenPath):
    with open(tokenPath, "rb") as tokenObj:
        credentialsObj = pickle.load(tokenObj)

# If there are no (valid) credentials available, let the user log in.


if not credentialsObj or not credentialsObj.valid:
    if credentialsObj and credentialsObj.expired and credentialsObj.refresh_token:
        credentialsObj.refresh(google.auth.transport.requests.Request())
    else:
        flowObj = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(credentialsPath, googleScopes)
        credentialsObj = flowObj.run_local_server(port=0)
    # Save the credentials for the next run
    with open(tokenPath, "wb") as tokenObj:
        pickle.dump(credentialsObj, tokenObj)



googleSheetsObj = googleapiclient.discovery.build("sheets", "v4", credentials=credentialsObj).spreadsheets()

