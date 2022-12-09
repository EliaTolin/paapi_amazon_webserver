from celery import Celery
import config

def make_celery(app_name=__name__):
    return Celery(
         app_name,
         backend=config.CELERY_RESULT_BACKEND,
         broker=config.CELERY_BROKER_URL
    )

celery_app = make_celery()