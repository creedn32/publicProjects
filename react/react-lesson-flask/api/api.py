import time
from flask import Flask

# app = Flask(__name__)
app = Flask(__name__, static_folder='../build', static_url_path='/')

@app.route('/api/time')
def get_current_time():
    print('Python is returning a object with the current time to the front end...')
    return {'time': time.time()}

@app.route('/')
def index():
    return app.send_static_file('index.html')