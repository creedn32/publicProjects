import time
from flask import Flask
from pprint import pprint as p
# import waitress

flaskAppObj = Flask(__name__, static_folder='../reactBuild', static_url_path='/')

@flaskAppObj.route('/api/time')
def returnCurrentTime():
    print('Python is returning a object with the current time to the front end...')
    return {'time': time.time()}

@flaskAppObj.route('/')
def returnIndexHTML():
    return flaskAppObj.send_static_file('index.html')



# if __name__ == '__main__':

#     def mainFunction(arrayOfArguments):
#         if arrayOfArguments[1] == 'development':
#             p('Running with Flask, not waitress...')
#             flaskAppObj.run()
#         else:
#             p('Running with waitress, not Flask...')
#             waitress.serve(flaskAppObj, host='0.0.0.0', port=8000)

#     p('flaskReactServer.py is not being imported. It is being run directly...')
#     mainFunction(sys.argv)

# else:
# 	p('flaskReactServer.py is being imported. It is not being run directly...')




# import time
# from flask import Flask

# app = Flask(__name__)

# @app.route('/time')
# def get_current_time():
#     return {'time': time.time()}
