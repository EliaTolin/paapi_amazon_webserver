from celery import Celery
import config

celery_app = Celery(
    __name__,
    backend=config.CELERY_RESULT_BACKEND,
    broker=config.CELERY_BROKER_URL,
    include=['core.tasks.amazon_task']
)


def make_celery(app):
    celery_app.conf.update(app.config)

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
