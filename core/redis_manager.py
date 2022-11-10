import redis
import config
from datetime import datetime


class RedisManager:
    def __init__(self):
        self.redis_db = redis.Redis(host=config.REDIS_DATABASE_HOST, port=config.REDIS_DATABASE_PORT,
                                    username=config.REDIS_DATABASE_USERNAME,
                                    password=config.REDIS_DATABASE_PASSWORD,
                                    decode_responses=True)
        self.time_created = datetime.now().time()

    def is_redis_available(self):
        try:
            self.redis_db.ping()
            print("Successfully connected to redis")
        except (redis.exceptions.ConnectionError, ConnectionRefusedError):
            print("Redis connection error!")
            return False
        return True
    
    def delete_all_keys(self):
        keys = self.redis_db.keys('*')
        for key in keys:
            self.redis_db.delete(key)


redis_manager = RedisManager()
