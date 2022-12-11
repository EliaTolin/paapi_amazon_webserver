import redis
import config
from datetime import datetime

from helper.debug_message import show_message_debug


class RedisManager:
    def __init__(self):
        show_message_debug(message="REDIS_DATABASE_HOST = "+config.REDIS_DATABASE_HOST)
        self.redis_db = redis.Redis(host=config.REDIS_DATABASE_HOST, port=config.REDIS_DATABASE_PORT,
                                    username=config.REDIS_DATABASE_USERNAME,
                                    password=config.REDIS_DATABASE_PASSWORD,
                                    decode_responses=True)
        self.time_created = datetime.now().time()

    def is_redis_available(self):
        try:
            self.redis_db.ping()
        except (redis.exceptions.ConnectionError, ConnectionRefusedError):
            return False
        return True
    
    def delete_all_keys(self):
        keys = self.redis_db.keys('*')
        for key in keys:
            self.redis_db.delete(key)


redis_manager = RedisManager()
