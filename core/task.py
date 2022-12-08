from time import sleep
import celery


@celery.task
def delay_hello_world(delay_seconds: int) -> str:
    sleep(delay_seconds)
    return 'hello world'
