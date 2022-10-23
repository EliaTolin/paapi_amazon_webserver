import redis
import config
from datetime import datetime


class RedisManager:
    def __init__(self):
        self.redis_db = redis.Redis(host=config.DATABASE_HOST, port=config.DATABASE_PORT, decode_responses=True)
        self.time_created = datetime.now().time()


redis_manager = RedisManager()
