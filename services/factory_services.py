from flask import Flask
from routes.routes import base_api
from services.celery_services import make_celery
import config


def init_services():
    app = Flask(__name__)
    app.register_blueprint(base_api)
    app.config.update(CELERY_CONFIG={
        'broker_url': config.CELERY_BROKER_URL,
        'result_backend': config.CELERY_BROKER_URL,
    })
    make_celery(app)
    return app
