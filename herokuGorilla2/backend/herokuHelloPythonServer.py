from flask import Flask, request, render_template, Response
import json
from pprint import pprint as p

flaskApp = Flask(__name__, static_folder='../frontend/', template_folder='../frontend/htmlTemplates')
flaskApp.config['TEMPLATES_AUTO_RELOAD'] = True


@flaskApp.route('/datarequests', methods=['GET', 'POST'])
def datarequests():

	if request.method == 'GET':
		dataToSendToFrontend = {
			'cat eyes': 'yellow',
			'collar': 'red'
		}

		return Response(json.dumps(dataToSendToFrontend), mimetype='application/json')


	if request.method == 'POST':
		requestObj = request.json

		if requestObj['spreadsheetType'] == 'public':
			return render_template('reconcilePublic.html')
		else:
			return render_template('reconcilePrivate.html')


@flaskApp.route('/')
def returnMainPage():
	return render_template('index.html')
	# return """	<p>Spreadsheet to reconcile:</p>
	# 			<button onclick="publicClickFunction()">Public</button>
	# 			<button onclick="privateClickFunction()">Private</button>
	# 			<p></p>
	# 			<img src="./frontend/assets/regal-cat.jpeg" alt="regal cat" />"""



if __name__ == '__main__':

    import waitress
    waitress.serve(flaskApp, host='0.0.0.0', port=8000)

    flaskApp.run()
