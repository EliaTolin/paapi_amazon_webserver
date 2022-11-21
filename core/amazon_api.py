from amazon_paapi import AmazonApi
from amazon_paapi.sdk.models.sort_by import SortBy
from amazon_paapi.errors.exceptions import TooManyRequests,InvalidArgument
from config import *
from models.amazon_category import AmazonCategory
from models.exceptions.amazon_exception import *
from models.amazon_model import AmazonItem
from core.redis_manager import redis_manager
import threading


class AmazonApiCore:

    def __init__(self) -> None:
        self.mutex = threading.Lock()
        self.amazon = AmazonApi(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_PARTNER_ID, AMAZON_COUNTRY,
                                throttling=THROTTLING_SECONDS)

    @staticmethod
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

    def search_products(self, keywords: str = None, actor: str = None, artist: str = None, author: str = None,
                        brand: str = None,
                        title: str = None,
                        max_price: int = None, min_price: int = None, min_saving_percent: int = None,
                        min_reviews_rating: int = None, search_index: str = None, sort: str = None,
                        item_page: int = None, item_count: int = None) -> list:

        if min_saving_percent is not None:
            if min_saving_percent <= 0:
                raise InvalidArgument

        is_none = keywords or actor or artist or author or brand or search_index or title

        # Limit the item count
        #item_count = MAX_ITEM_COUNT_OFFER if item_count > MAX_ITEM_COUNT_OFFER else item_count
        #item_page = MAX_ITEM_PAGE_OFFER if item_page > MAX_ITEM_PAGE_OFFER else item_page

        if is_none is None:
            raise MissingParameterAmazonException

        sort_type = self._get_sort_type(sort)
        try:
            search_results = self.amazon.search_items(keywords=keywords,
                                                      actor=actor, artist=artist, author=author, brand=brand, title=title,
                                                      max_price=max_price, min_price=min_price,
                                                      min_saving_percent=min_saving_percent,
                                                      min_reviews_rating=min_reviews_rating, search_index=search_index,
                                                      sort_by=sort_type, item_page=item_page, item_count=item_count)
        except InvalidArgument:
            raise InvalidArgumentAmazonException

        list_item = []
        for item in search_results.items:
            try:
                if item.offers is None:
                    continue
                if item.offers.listings[0] is None:
                    continue
                if item.offers.listings[0].price is None:
                    continue

                amazon_item = AmazonItem(item)
                list_item.append(amazon_item)

            except UrlNotDefinedAmazonException:
                continue

            except Exception:
                raise Exception("generic_error")

        return list_item

    def get_category_offers(self, category, item_count: int = 10, item_page: int = 1,
                            min_saving_percent: int = None, exclude_zero_offers: bool = False):
        if (item_count * item_page) > MAX_ITEM_COUNT_OFFER * MAX_ITEM_PAGE_OFFER:
            return []

        if min_saving_percent is not None:
            if min_saving_percent <= 0:
                raise InvalidArgument

        if category not in AmazonCategory.ITCategory:
            raise CategoryNotExistException

        item_count = MAX_ITEM_COUNT_OFFER if item_count > MAX_ITEM_COUNT_OFFER else item_count
        item_page = MAX_ITEM_PAGE_OFFER if item_page > MAX_ITEM_PAGE_OFFER else item_page

        key_error_too_many = category + "_error_too_many"
        if not redis_manager.redis_db.exists(category) or redis_manager.redis_db.exists(key_error_too_many):
            with self.mutex:
                # Check if exist previous error
                page_download = 1
                value_key = redis_manager.redis_db.get(key_error_too_many)
                if value_key is not None:
                    page_download = int(value_key)

                while redis_manager.redis_db.llen(category) < MAX_ITEM_COUNT_OFFER * MAX_ITEM_PAGE_OFFER:
                    try:
                        products = self.search_products(search_index=category, item_count=MAX_ITEM_COUNT_OFFER,
                                                        item_page=page_download,
                                                        min_saving_percent=min_saving_percent)
                        if len(products) == 0:
                            break
                        for product in products:
                            if min_saving_percent is not None:
                                if product.price_saving_amount_percentage is None:
                                    if exclude_zero_offers:
                                        continue
                                elif product.price_saving_amount_percentage < min_saving_percent:
                                    continue
                            redis_manager.redis_db.rpush(category, product.to_json())

                        page_download += 1

                    except MissingParameterAmazonException:
                        raise MissingParameterAmazonException

                    except TooManyRequests:
                        redis_manager.redis_db.set(key_error_too_many, page_download)
                        ttl_category = redis_manager.redis_db.ttl(category)
                        ttl_category = CATEGORY_REFRESH_TIMEOUT_SECONDS if ttl_category < 0 else ttl_category
                        redis_manager.redis_db.expire(key_error_too_many, ttl_category)
                        if page_download > 0:
                            break
                        else:
                            raise TooManyRequestAmazonException
                    else:
                        redis_manager.redis_db.delete(key_error_too_many)
                redis_manager.redis_db.expire(category, CATEGORY_REFRESH_TIMEOUT_SECONDS)

        # print(category+" Finish mutex " + str(threading.get_ident()))
        index_start = (item_page - 1) * item_count
        index_finish = (item_page * item_count) - 1

        return redis_manager.redis_db.lrange(category, index_start, index_finish)
