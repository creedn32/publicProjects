function c(textToLogToConsole) {
	console.log(textToLogToConsole)
}

async function receiveGetResponseFromServer() {
	async function sendGetRequestFromBrowser() {
		try {
			return (await axios.get('/datarequests')).data
		} catch (e) {
			return null;
		}
	}

	var dataReceivedFromServer = await sendGetRequestFromBrowser();
	var jsonReceivedFromServer = JSON.stringify(dataReceivedFromServer)

	c(`Received data from server from GET request: ${jsonReceivedFromServer}`)
};


function sendPostRequestFromBrowser(spreadsheetType) {

	// Creating a XHR object
	let xhr = new XMLHttpRequest();
	let url = '/datarequests';

	// open a connection
	xhr.open('POST', url, true);

	// Set the request header i.e. which type of content you are sending
	xhr.setRequestHeader('Content-Type', 'application/json');

	// Create a state change callback
	xhr.onreadystatechange = function () {

		if (xhr.readyState === 4 && xhr.status === 200) {
			// Print received data from server
			c(`Received response from server on POST request: ${this.responseText}`)

			if (xhr.getResponseHeader('content-type').indexOf('text/html') >= 0) { 
				var parserObj = new DOMParser();
				var responseDocumentObj = parserObj.parseFromString(this.responseText, 'text/html');
				document.body.innerHTML = responseDocumentObj.body.innerHTML
			}
		}
	};

	// Converting JSON data to string
	var spreadSheetTypePostData = JSON.stringify({"spreadsheetType": spreadsheetType});

	// Sending data with the request
	xhr.send(spreadSheetTypePostData);
}





function publicClickFunction() {
	sendPostRequestFromBrowser('public');
}


function privateClickFunction() {
	receiveGetResponseFromServer()
	sendPostRequestFromBrowser('private');
}

function reconcileClickFunction() {
	window.location = '/';
}




