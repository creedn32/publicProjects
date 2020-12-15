const mainLibrary = require('../mainLibrary/mainLibrary');
const c = console.log.bind(console);
const fs = require('fs');
const {google} = require('googleapis');

module.exports.getSpreadsheetLevelObj = () => {

    return 1;

};

module.exports.getGoogleSheetsLevelObj = (pathArrayBelowRepos, googleSheetsUsername) => {

    const pathArrayRepos = mainLibrary.getPathArrayUpFolderTree(pathArrayBelowRepos, 'repos');
    const pathStrOAuthFolder = mainLibrary.pathArrayToStr(pathArrayRepos.concat(['privateData', 'python', 'googleCredentials', 'usingOAuthGspread']));
    const pathStrTokenFile = pathStrOAuthFolder + '/' + googleSheetsUsername + '/authorizedUserFile.json';

    const arrayOfScopes = ['https://www.googleapis.com/auth/spreadsheets.readonly'];

    fs.readFile(pathStrOAuthFolder + '/jsonCredentialsFile.json', (err, content) => {
        
        if (err) return c('Error loading client secret file:', err);
        spreadsheetLevelObj = authorize(JSON.parse(content));

    });

    // return spreadsheetLevelObj;

    function authorize(credentials) {

        const {client_secret, client_id, redirect_uris} = credentials.installed;
        const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);

        // Check if we have previously stored a token.

        fs.readFile(pathStrTokenFile, (err, token) => {

            if (err) return c('Token failed.'); // getNewToken(oAuth2Client, callback);
            return oAuth2Client.setCredentials(JSON.parse(token));

        });
    }

    /**
     * Get and store new token after prompting for user authorization, and then
     * execute the given callback with the authorized OAuth2 client.
     * @param {google.auth.OAuth2} oAuth2Client The OAuth2 client to get token for.
     * @param {getEventsCallback} callback The callback for the authorized client.
     */

    function getNewToken(oAuth2Client, callback) {
        
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
                callback(oAuth2Client);
            
            });
        });
    }
};
