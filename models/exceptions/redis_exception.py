from models.exceptions.base_exception import Error
import constant.exception.database_error_code_message as db_error_code_message

class RedisConnectionException(Error):
    """Error to connection to RedisDB"""
    code_message = db_error_code_message.redis_connection_error
    pass
