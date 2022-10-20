from amazon_paapi import AmazonApi
from amazon_paapi.sdk.models.sort_by import SortBy
from config import *
from models.amazon_exception import *
from models.amazon_model import AmazonItem

amazon = AmazonApi(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_PARTNER_ID, 'IT')


# (method) search_items: (item_count: int = None, item_page: int = None, actor: str = None, artist: str = None,
# author: str = None, brand: str = None, keywords: str = None, title: str = None, availability: Availability = None,
# browse_node_id: str = None, condition: Condition = None, currency_of_preference: str = None, delivery_flags: List[
# str] = None, languages_of_preference: List[str] = None, merchant: Merchant = None, max_price: int = None,
# min_price: int = None, min_saving_percent: int = None, min_reviews_rating: int = None, search_index: str = None,
# sort_by: SortBy = None, **kwargs: Any) -> SearchResult

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


def search_products(keywords, actor: str = None, artist: str = None, author: str = None, brand: str = None,
                    title: str = None,
                    max_price: int = None, min_price: int = None, min_saving_percent: int = None,
                    min_reviews_rating: int = None, search_index: str = None, sort: str = None) -> list:
    sort_type = _get_sort_type(sort)

    search_results = amazon.search_items(keywords=keywords,
                                         actor=actor, artist=artist, author=author, brand=brand, title=title,
                                         max_price=max_price, min_price=min_price,
                                         min_saving_percent=min_saving_percent,
                                         min_reviews_rating=min_reviews_rating, search_index=search_index,
                                         sort_by=sort_type)

    list_item = []
    for item in search_results.items:
        try:
            amazon_item = AmazonItem(item)
            list_item.append(amazon_item.to_json().replace("\"", "\'"))

        except UrlNotDefinedAmazonException:
            continue

        except Exception:
            raise Exception("error")
    return list_item
