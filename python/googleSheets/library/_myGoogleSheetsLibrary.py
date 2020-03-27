def getGoogleSheetsAPIObj():

    from pathlib import Path
    pathToThisPythonFile = Path(__file__).resolve()
    import sys
    sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'library')))
    import _myPyFunc
    
    import pickle, googleapiclient.discovery, google_auth_oauthlib.flow, google.auth.transport.requests


    pathToJSONForCredentialsRetrieval = Path(pathToThisPythonFile.parents[4], 'privateData', 'python', 'googleCredentials', 'jsonForCredentialsRetrieval.json')
    pathToPickleFileWithCredentials = Path(pathToThisPythonFile.parents[4], 'privateData', 'python', 'googleCredentials', 'pickleFileWithCredentials.pickle')

    googleSheetsAPIScopes = ["https://www.googleapis.com/auth/spreadsheets"]
    credentialsObj = None

    #if the pickle is file is available from persistent memory, then get the credentials object from it
    #otherwise, check if the credentials object can be refreshed and do that
    #if the credentials object can't be refreshed, then get them

    if Path.exists(pathToPickleFileWithCredentials):
        
        with open(pathToPickleFileWithCredentials, "rb") as pickleFileObj:
            credentialsObj = pickle.load(pickleFileObj)
    else:

        if not credentialsObj or not credentialsObj.valid:
            if credentialsObj and credentialsObj.expired and credentialsObj.refresh_token:
                credentialsObj.refresh(google.auth.transport.requests.Request())
            else:
                flowObj = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(pathToJSONForCredentialsRetrieval, googleSheetsAPIScopes)
                credentialsObj = flowObj.run_local_server(port=0)
            
            #save the credentials in persistent memeory
            
            with open(pathToPickleFileWithCredentials, "wb") as pickleFileObj:
                pickle.dump(credentialsObj, pickleFileObj)

    return googleapiclient.discovery.build("sheets", "v4", credentials=credentialsObj).spreadsheets()