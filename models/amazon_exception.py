class Error(Exception):
    """Base class for other exception"""
    pass


class UrlNotDefinedAmazonException(Error):
    """Url not defined """
    pass


class MissingParameterAmazonException(Error):
    """At least one of Actor, Artist, Author,
    Brand, BrowseNodeId, Keywords, SearchIndex, Title should be provided."""
    pass


class GenericErrorAmazonException(Error):
    """Generic Error in Amazon API"""
    pass

