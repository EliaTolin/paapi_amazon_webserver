from models.exceptions.base_exception import Error
import constant.exception.amazon_error_code_message as error_message


class InvalidArgumentAmazonException(Error):
    """The value provided in the request for atleast one parameter is invalid."""
    code_message = error_message.invalid_arguments
    pass


class CategoryNotExistException(Error):
    """Category not exists"""
    code_message = error_message.category_not_exist

    def __dict__(self):
        return {"code_message": self.code_message}

    pass


class UrlNotDefinedAmazonException(Error):
    """Url not defined """
    code_message = error_message.url_not_defined
    pass


class MissingParameterAmazonException(Error):
    """At least one of Actor, Artist, Author,
    Brand, BrowseNodeId, Keywords, SearchIndex, Title should be provided."""
    code_message = error_message.missing_parameter
    pass


class GenericErrorAmazonException(Error):
    """Generic Error in Amazon API"""
    code_message = error_message.generic_error_amazon
    pass


class TooManyRequestAmazonException(Error):
    """except amazon_paapi.errors.exceptions.TooManyRequests:
        https://github.com/sergioteula/python-amazon-paapi/discussions/59"""
    code_message = error_message.too_many_request
    pass


class ItemsNotFoundAmazonException(Error):
    """except amazon_paapi.errors.exceptions.ItemsNotFound"""
    code_message = error_message.items_not_found


class AsinNotFoundException(Error):
    """except amazon_paapi.errors.exceptions.AsinNotFound"""
    code_message = error_message.asin_not_found
