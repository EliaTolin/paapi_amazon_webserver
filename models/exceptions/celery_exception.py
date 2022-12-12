from models.exceptions.base_exception import Error
import constant.exception.celery_error_code as error_message


class FailureCeleryException(Error):
    """except amazon_paapi.errors.exceptions.ItemsNotFound"""
    code_message = error_message.failure
