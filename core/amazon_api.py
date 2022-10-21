from amazon_paapi import AmazonApi
from amazon_paapi.sdk.models.sort_by import SortBy
from config import *
from models.amazon_exception import *
from models.amazon_model import AmazonItem
from core.redis_manager import redis_manager

amazon = AmazonApi(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_PARTNER_ID, AMAZON_COUNTRY)


def _get_sort_type(sort) -> SortBy:
    if sort is None:
        return SortBy.RELEVANCE

    sort_type = {
        "RELEVANCE": SortBy.RELEVANCE,
        "PRICE_HIGHTOLOW": SortBy.PRICE_HIGHTOLOW,
        "PRICE_LOWTOHIGH": SortBy.PRICE_LOWTOHIGH,
        "FEATURED": SortBy.FEATURED,
        "NEWESTARRIVALS": SortBy.NEWESTARRIVALS,
        "AVGCUSTOMERREVIEWS": SortBy.AVGCUSTOMERREVIEWS,
    }
    return sort_type.get(sort, SortBy.RELEVANCE)


def search_products(keywords: str = None, actor: str = None, artist: str = None, author: str = None, brand: str = None,
                    title: str = None,
                    max_price: int = None, min_price: int = None, min_saving_percent: int = None,
                    min_reviews_rating: int = None, search_index: str = None, sort: str = None,
                    item_page: int = None, item_count: int = None) -> list:

    is_none = keywords or actor or artist or author or brand or search_index or title

    # Limit the item count
    item_count = 100 if item_count > 100 else item_count

    if is_none is None:
        raise MissingParameterAmazonException

    sort_type = _get_sort_type(sort)

    search_results = amazon.search_items(keywords=keywords,
                                         actor=actor, artist=artist, author=author, brand=brand, title=title,
                                         max_price=max_price, min_price=min_price,
                                         min_saving_percent=min_saving_percent,
                                         min_reviews_rating=min_reviews_rating, search_index=search_index,
                                         sort_by=sort_type, item_page=item_page, item_count=item_count)

    list_item = []
    for item in search_results.items:
        try:
            amazon_item = AmazonItem(item)
            list_item.append(amazon_item)

        except UrlNotDefinedAmazonException:
            continue

        except Exception:
            raise Exception("error")
    return list_item


def get_category_offers(category, item_count: int = None, item_page: int = None,
                        min_saving_percent: int = None):
    item_count = 100 if item_count > 100 else item_count

    if redis_manager.redis_db.exists(category):
        num_element_in_db = redis_manager.redis_db.hget(category, "items").count()

        if (item_count*item_page) < num_element_in_db:

            try:
                products = search_products(search_index=category, item_count=item_count, item_page=item_page,
                                           min_saving_percent=min_saving_percent)
            except MissingParameterAmazonException:
                raise MissingParameterAmazonException
            if len(products) == 0:
                raise GenericErrorAmazonException

        return redis_manager.redis_db.hget(category, "items")

    try:
        products = search_products(search_index=category, item_count=item_count, item_page=item_page,
                                   min_saving_percent=min_saving_percent)

    except MissingParameterAmazonException:
        raise MissingParameterAmazonException

    if len(products) == 0:
        raise GenericErrorAmazonException

    redis_manager.redis_db.set(category, "items", products)
    # redis_manager.redis_db.set(category, "number_items", item_count)
    redis_manager.redis_db.expire(category, DATABASE_REFRESH_TIME_SECONDS)

    return products
