from typing import Tuple, List
from amazon_paapi.sdk.models.sort_by import SortBy
from amazon_paapi.errors.exceptions import TooManyRequests, InvalidArgument, ItemsNotFound
from models.amazon_category import AmazonCategory
from models.exceptions.amazon_exception import *
from models.amazon_model import AmazonItem
from singleton.amazon_manager import amazon_manager
from config import *
import threading
import constant.exception.amazon_error_code_message as amazon_error_code_message


class AmazonApiCore:

    def __init__(self) -> None:
        self.mutex = threading.Lock()

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
                        item_page: int = None, item_count: int = None, exclude_zero_price: bool = False,
                        exclude_zero_offers: bool = False, only_prime_delivery: bool = False) -> \
            Tuple[List[AmazonItem], bool]:

        if min_saving_percent is not None:
            if min_saving_percent <= 0:
                raise InvalidArgument

        is_none = keywords or actor or artist or author or brand or search_index or title

        if is_none is None:
            raise MissingParameterAmazonException

        if search_index is not None:
            if search_index not in AmazonCategory.ITCategory:
                raise CategoryNotExistException

        # Limit the item count
        item_count = MAX_ITEM_COUNT_OFFER if item_count > MAX_ITEM_COUNT_OFFER else item_count
        if item_page > MAX_ITEM_PAGE_OFFER:
            return [], True

        sort_type = self._get_sort_type(sort)
        list_item = []
        limit_reached = False
        try:
            search_results = amazon_manager.amazon_api.search_items(keywords=keywords,
                                                                    actor=actor, artist=artist, author=author,
                                                                    brand=brand,
                                                                    title=title,
                                                                    max_price=max_price, min_price=min_price,
                                                                    # min_saving_percent=min_saving_percent,
                                                                    # min_reviews_rating=min_reviews_rating,
                                                                    search_index=search_index,
                                                                    sort_by=sort_type, item_page=item_page,
                                                                    item_count=item_count)
        except InvalidArgument:
            raise InvalidArgumentAmazonException

        except ItemsNotFound:
            raise ItemsNotFoundAmazonException

        except TooManyRequests:
            raise TooManyRequestAmazonException

        if search_results is None:
            return [], True

        if search_results.items is None:
            return [], True

        if len(search_results.items) == 0:
            return [], True

        if len(search_results.items) != item_count:
            limit_reached = True

        for item in search_results.items:
            try:
                if item.offers is None:
                    continue
                if item.offers.listings[0] is None:
                    continue
                if item.offers.listings[0].price is None:
                    continue

                amazon_item = AmazonItem(item)

                if exclude_zero_price and amazon_item.price_actual == 0.0:
                    continue

                if amazon_item.price_saving_amount_percentage is None:
                    if min_saving_percent is not None:
                        continue
                    if exclude_zero_offers:
                        continue
                elif min_saving_percent is not None:
                    if amazon_item.price_saving_amount_percentage <= min_saving_percent:
                        continue

                if only_prime_delivery is not None:
                    if only_prime_delivery and not amazon_item.prime_delivery:
                        continue

                list_item.append(amazon_item)

            except UrlNotDefinedAmazonException:
                continue

            except Exception:
                raise Exception(amazon_error_code_message.generic_error_amazon)

        return list_item, limit_reached

    @staticmethod
    def get_products_by_asin(asins: List[str]) -> List[AmazonItem]:
        list_item = []
        try:
            products_results = amazon_manager.amazon_api.get_items(asins)
        except InvalidArgument:
            raise InvalidArgumentAmazonException

        except ItemsNotFound:
            raise ItemsNotFoundAmazonException

        except TooManyRequests:
            raise TooManyRequestAmazonException

        for item in products_results.items:
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
                raise Exception(amazon_error_code_message.generic_error_amazon)

        return list_item
