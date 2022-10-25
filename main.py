from flask import Flask
from routes.routes import base_api
from core.redis_manager import redis_manager
app = Flask(__name__)
app.register_blueprint(base_api)


@app.route('/')
def hello_world():
    return 'Hello, World!\n'


if __name__ == '__main__':
    if not redis_manager.is_redis_available():
        exit(-1,"REDIS NOT CONNECTED")

    app.run(host='0.0.0.0', debug=True)
