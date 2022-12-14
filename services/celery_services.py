from celery import Celery
import config
from helper.debug_message import show_message_debug
celery_app = Celery(
    __name__,
    backend=config.CELERY_RESULT_BACKEND,
    broker=config.CELERY_BROKER_URL,
    include=['core.tasks.amazon_task']
)


def make_celery(app):
    show_message_debug(message="CELERY_RESULT_BACKEND = " + config.CELERY_RESULT_BACKEND)
    show_message_debug(message="CELERY_BROKER_URL = " + config.CELERY_BROKER_URL)
    show_message_debug(message="REDIS_DATABASE_HOST = " + config.REDIS_DATABASE_HOST)
    celery_app.conf.update(app.config)

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    show_message_debug("INIT CELERY DONE")