from flask import Flask
from routes.routes import base_api

app = Flask(__name__)
app.register_blueprint(base_api)


@app.route('/')
def hello_world():
    return 'Hello, World!\n'


if __name__ == '__main__':
    app.run(debug=True)
