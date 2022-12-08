from config import *
from datetime import datetime
from amazon_paapi import AmazonApi
from celery import Celery

CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

class CeleryManager:
    
    def __init__(self,app):
        self.celery_app = Celery(
        app.import_name,
        backend=CELERY_RESULT_BACKEND,
        broker=CELERY_BROKER_URL
        )
        self.celery_app.conf.update(app.config)
        self.time_created = datetime.now().time()


celery_manager = CeleryManager()
