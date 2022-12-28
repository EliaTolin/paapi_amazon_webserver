from models.exceptions.amazon_exception import *
from celery.exceptions import MaxRetriesExceededError

from models.exceptions.redis_exception import RedisConnectionException


def handle_error(exc, task_id):
    # Handle the exception
    if isinstance(exc, ValueError):
        print('Task {} failed because y cannot be 0'.format(task_id))
    elif isinstance(exc, TypeError):
        print('Task {} failed because x and y must be integers'.format(task_id))
        raise GenericErrorAmazonException

    elif isinstance(exc, MaxRetriesExceededError):
        raise TooManyRequestAmazonException

    elif isinstance(exc, InvalidArgumentAmazonException):
        raise InvalidArgumentAmazonException

    elif isinstance(exc, MissingParameterAmazonException):
        raise MissingParameterAmazonException

    elif isinstance(exc, TooManyRequestAmazonException):
        raise TooManyRequestAmazonException

    elif isinstance(exc, RedisConnectionException):
        raise RedisConnectionException

    elif isinstance(exc, CategoryNotExistException):
        raise CategoryNotExistException

    elif isinstance(exc, ItemsNotFoundAmazonException):
        raise ItemsNotFoundAmazonException
