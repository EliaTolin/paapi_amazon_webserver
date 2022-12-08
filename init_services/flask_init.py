from routes.routes import base_api
from flask import Flask


def make_flask():
    app = Flask(__name__)
    app.register_blueprint(base_api)
    app.config.update(CELERY_CONFIG={
        'broker_url': 'redis://localhost:6379',
        'result_backend': 'redis://localhost:6379',
    })
    return app
