from core.redis_manager import redis_manager
import helper.debug_message as debug_message
from models.amazon_category import AmazonCategory
import constant.database.database_constants as db_constant


def init_server() -> bool:
    debug_message.show_message_debug("START INIT SERVER!", debug_message.TypeMessage.INFO)
    # Check if redis is available
    if not redis_manager.is_redis_available():
        debug_message.show_message_debug("REDIS NOT CONNECTED!", debug_message.TypeMessage.ERROR)
        return False
    # Start init the categories preferences
    debug_message.show_message_debug("INIT REDIS!", debug_message.TypeMessage.INFO)
    category_counter = 0

    for category in AmazonCategory.ITCategory:
        key = category+db_constant.key_suffix_preference
        if redis_manager.redis_db.get(key) is None:
            redis_manager.redis_db.set(key, 1)
            category_counter += 1
    debug_message.show_message_debug("ADD {0} CATEGORY PREFERENCES KEY!".format(category_counter),
                                     debug_message.TypeMessage.INFO)

    # Finish the init the server
    debug_message.show_message_debug("FINISH INIT SERVER!", debug_message.TypeMessage.SUCCESS)
    return True
