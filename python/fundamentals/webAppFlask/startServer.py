from flask import Flask

flaskApp = Flask(__name__)
@flaskApp.route('/')

def jsonReturnFunction():

   jsonToReturn = {
        'cat eyes': 'yellow',
        'collar': 'red'
    }
   
   return str(jsonToReturn)


if __name__ == '__main__':
    flaskApp.run()