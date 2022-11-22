from models.exceptions.base_exception import Error


class RedisConnectionException(Error):
    """Error to connection to RedisDB"""
    code_message = "redis_connection_error"
    pass
