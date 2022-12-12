import time

from singleton.redis_manager import redis_manager
import helper.debug_message as debug_message
from models.amazon_category import AmazonCategory
import constant.database.database_constants as db_constant
import config


def init_server() -> bool:
    debug_message.show_message_debug("START INIT SERVER!", debug_message.TypeMessage.INFO)
    # Check if redis is available
    if not redis_manager.is_redis_available():
        debug_message.show_message_debug("REDIS NOT CONNECTED! " + config.REDIS_DATABASE_HOST,
                                         debug_message.TypeMessage.ERROR)
        return False
    # Start init the categories preferences
    debug_message.show_message_debug("INIT REDIS!", debug_message.TypeMessage.INFO)
    category_counter = 0

    for category in AmazonCategory.ITCategory:
        key = category + db_constant.key_suffix_preference
        if redis_manager.redis_db.get(key) is None:
            redis_manager.redis_db.set(key, 1)
            category_counter += 1
    debug_message.show_message_debug("ADD {0} CATEGORY PREFERENCES KEY!".format(category_counter),
                                     debug_message.TypeMessage.INFO)

    # Finish the init the server

    # Check celery worker
    try:
        from services.celery_services import celery_app
        worker_is_up = False
        # Retry for 10 Seconds to connecting to Celery
        for i in range(10):
            if celery_app.control.inspect().ping():
                worker_is_up = True
                break
            debug_message.show_message_debug("RETRY TO CONNECT TO CELERY, RETRY N:" + str(i),
                                             debug_message.TypeMessage.WARNING)
            time.sleep(1)
        if not worker_is_up:
            debug_message.show_message_debug("CELERY WORKER NOT FOUND! ",
                                             debug_message.TypeMessage.ERROR)
            return False
    except IOError:
        from errno import errorcode
        debug_message.show_message_debug("CELERY CONNECTION ERROR! ",
                                         debug_message.TypeMessage.ERROR)
        return False

    debug_message.show_message_debug("CELERY SERVER OK!", debug_message.TypeMessage.SUCCESS)
    debug_message.show_message_debug("FINISH INIT SERVER!", debug_message.TypeMessage.SUCCESS)
    return True
