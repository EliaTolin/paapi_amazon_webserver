from flask import Flask

import init_server as init
from routes.routes import base_api

import config

app = Flask(__name__)
app.register_blueprint(base_api)


@app.route('/')
def hello_world():
    return 'Hello, PA API Amazon Server!\n'


if __name__ == '__main__':
    if init.init_server():
        app.run(host='0.0.0.0', debug=config.DEBUG)
    else:
        print("###### THERE WAS AN ERROR, CHECK THE LOGS ######")
        exit(-1)
