from flask import Flask
from routes.routes import base_api
import config

def __init_celery(celery, app):
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

def init_services(**kwargs):
    app = Flask(__name__)
    if kwargs.get("celery"):
        __init_celery(kwargs.get("celery"), app)
    app.register_blueprint(base_api)
    app.config.update(CELERY_CONFIG={
        'broker_url': config.CELERY_BROKER_URL,
        'result_backend': config.CELERY_BROKER_URL,
    })
    return app