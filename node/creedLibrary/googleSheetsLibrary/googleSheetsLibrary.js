const mainLibrary = require('../mainLibrary/mainLibrary');
const c = console.log.bind(console);

const fs = require('fs');
const {google} = require('googleapis');
const readline = require('readline');

module.exports.getGoogleAccountLevelObj = async (pathArrayBelowRepos, googleSheetsUsername) => {

    const pathArrayRepos = mainLibrary.getPathArrayUpFolderTree(pathArrayBelowRepos, 'repos');
    const pathStrOAuthFolder = mainLibrary.pathArrayToStr(pathArrayRepos.concat(['privateData', 'python', 'googleCredentials', 'usingOAuthGspread']));
    const pathStrTokenFile = pathStrOAuthFolder + '/node/' + googleSheetsUsername + '/authorizedUserFile.json';

    const arrayOfScopes = ['https://www.googleapis.com/auth/spreadsheets.readonly'];

    try {

        const jsonCredentialsFileData = await fs.promises.readFile(pathStrOAuthFolder + '/jsonCredentialsFile.json');
        return await authorize(JSON.parse(jsonCredentialsFileData));

    } catch (error) {

        c('Error loading client secret file:', err);

    }


    async function authorize(credentials) {

        const {client_secret, client_id, redirect_uris} = credentials.installed;
        const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);

        // Check if we have previously stored a token.

        try {

            token = await fs.promises.readFile(pathStrTokenFile);

        } catch (error) {

            token = getNewToken(oAuth2Client);

        }

        oAuth2Client.setCredentials(JSON.parse(token));

        return oAuth2Client;

    }

    /**
     * Get and store new token after prompting for user authorization, and then
     * execute the given callback with the authorized OAuth2 client.
     * @param {google.auth.OAuth2} oAuth2Client The OAuth2 client to get token for.
     * @param {getEventsCallback} callback The callback for the authorized client.
     */

    function getNewToken(oAuth2Client) {

        const authUrl = oAuth2Client.generateAuthUrl({

            access_type: 'offline',
            scope: arrayOfScopes,

        });

        console.log('Authorize this app by visiting this url:', authUrl);

        const rl = readline.createInterface({

            input: process.stdin,
            output: process.stdout,

        });

        rl.question('Enter the code from that page here: ', (code) => {

            rl.close();

            oAuth2Client.getToken(code, (err, token) => {

                if (err) return console.error('Error while trying to retrieve access token', err);

                oAuth2Client.setCredentials(token);
                // Store the token to disk for later program executions

                fs.writeFile(pathStrTokenFile, JSON.stringify(token), (err) => {

                    if (err) return console.error(err);
                    console.log('Token stored to', pathStrTokenFile);

                });

                return token;

            });
        });
    }
};

module.exports.getGoogleSheetsValuesLevelObj = (googleAccountLevelObj) => {

    return google.sheets({version: 'v4', auth: googleAccountLevelObj}).spreadsheets.values;
}


module.exports.getGoogleSpreadsheetID = async (googleAccountLevelObj, googleSpreadsheetTitle) => {

    const googleDriveLevelObj = google.drive({version: 'v3', auth: googleAccountLevelObj});

    // let files = [];
    // let pageToken = '';
    // let url = DRIVE_FILES_API_V3_URL;

    q = 'mimeType="application/vnd.google-apps.spreadsheet" and name = "' + googleSpreadsheetTitle + '"';

    let params = {
        'q': q,
        'pageSize': 1000,
        'supportsAllDrives': true,
        'includeItemsFromAllDrives': true,
    };

    // while (pageToken) {

    //     if (pageToken) {

    //         params['pageToken'] = pageToken;

    //     }

    // }


    //     if pageToken:
    //         params['pageToken'] = pageToken

    //     res = self.request('get', url, params=params).json()
    //     files.extend(res['files'])
    //     pageToken = res.get('nextPageToken', None)

    // return files

    const driveList = await googleDriveLevelObj.files.list(params=params);

    return driveList.data.files[0].id;

};


module.exports.getSpreadsheetLevelObj = async (googleAccountLevelObj, googleSpreadsheetTitle) => {

    return {

        googleSpreadsheetID: await module.exports.getGoogleSpreadsheetID(googleAccountLevelObj, googleSpreadsheetTitle)

    };
};


module.exports.getSheetLevelObj = async (pathBelowRepos, googleSheetsUsername, googleSpreadsheetTitle, googleSheetTitle) => {

    const googleAccountLevelObj = await module.exports.getGoogleAccountLevelObj(pathBelowRepos, googleSheetsUsername, googleSpreadsheetTitle);
    const googleSheetsValuesLevelObj = module.exports.getGoogleSheetsValuesLevelObj(googleAccountLevelObj);
    const spreadsheetID = await module.exports.getGoogleSpreadsheetID(googleAccountLevelObj, googleSpreadsheetTitle);

    return {

        googleAccountLevelObj: googleAccountLevelObj,
        googleSheetsValuesLevelObj: googleSheetsValuesLevelObj,
        spreadsheetLevelObj: await module.exports.getSpreadsheetLevelObj(googleAccountLevelObj, googleSpreadsheetTitle),
        spreadsheetID: spreadsheetID,
        getArrayOfValues: async function() {

            try {

                const request = {

                    spreadsheetId: spreadsheetID,
                    range: googleSheetTitle,

                };

                const response = await googleSheetsValuesLevelObj.get(request);
                const sheetArrayOfArrays = response.data.values;

                const maxRowLength = Math.max(...sheetArrayOfArrays.map(row => row.length));
                const rowsWithFill = sheetArrayOfArrays.map(row => row.concat(Array(maxRowLength - row.length).fill('')));
                return rowsWithFill;

            } catch (error) {

                c('The API returned an error: ' + error);

            }

        },
        updateSheet: async function(arrayToUpload) {

            const request = {

                spreadsheetId: spreadsheetID,

                resource: {

                    valueInputOption: 'RAW',

                    data: {

                        range: googleSheetTitle,
                        values: arrayToUpload
                    },

                },

                auth: googleAccountLevelObj,

            };

            try {

                const response = await googleSheetsValuesLevelObj.batchUpdate(request);
                // c(JSON.stringify(response, null, 2));

            } catch (err) {

                c(err);

            }

        }
    };
};
