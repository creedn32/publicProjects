import flask

flaskApp = flask.Flask(__name__, static_url_path='')

@flaskApp.route('/cat')
def returnCatDetails():

   jsonToReturn = {
        'cat eyes': 'yellow',
        'collar': 'red'
    }
   
   return str(jsonToReturn)



# @flaskApp.route('/') #<path:filename>')
# def returnMainPage():

#    return flask.send_from_directory('../frontend', filename)
   


@flaskApp.route('/') #<path:filename>')
def returnMainPage():

   return flask.render_template('../frontend', filename)




if __name__ == '__main__':
    
    from waitress import serve
    serve(flaskApp, host='0.0.0.0', port=8000)

    flaskApp.run()