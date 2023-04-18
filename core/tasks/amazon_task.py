import random
import time
from amazon_paapi.errors.exceptions import TooManyRequests, InvalidArgument, ItemsNotFound
from config import *
from constant.tasks.tasks_name_constants import TASK_GET_OFFERS_AMAZON
from core.amazon_api import AmazonApiCore
from helper.celery_meta_helper import get_meta, get_final_meta
from models.amazon_category import AmazonCategory
from models.exceptions.amazon_exception import *
from singleton.redis_manager import redis_manager
import constant.database.database_constants as database_constants
from services.celery_services import celery_app

amazonApiCore = AmazonApiCore()


@celery_app.task(name=TASK_GET_OFFERS_AMAZON, bind=True, propagate=True, max_retries=5)
def get_category_offers(self, category, item_count: int = 10, item_page: int = 1,
                        min_saving_percent: int = None, exclude_zero_offers: int = 0):
    try:
        if (item_count * item_page) > MAX_ITEM_COUNT_OFFER * MAX_ITEM_PAGE_OFFER:
            self.update_state(state='REVOKED',
                              meta={'error': 'LIMIT_REACHED'})

        if min_saving_percent is not None:
            if min_saving_percent <= 0:
                raise InvalidArgument

        if category not in AmazonCategory.ITCategory:
            raise CategoryNotExistException

    except InvalidArgument as e:
        self.update_state(state="FAILURE", meta={"exc_type": type(e).__name__,
                                                 "exc_message": str(e)})
        raise InvalidArgumentAmazonException

    except CategoryNotExistException as e:
        self.update_state(state="FAILURE", meta={"exc_type": type(ItemsNotFoundAmazonException).__name__,
                                                 "exc_message": ItemsNotFoundAmazonException.code_message})
        raise e

    key_error_too_many = category + database_constants.key_suffix_error_too_many
    start_time = time.perf_counter()
    total_element = 0

    # Check if exist previous error
    completed_key = category + database_constants.key_suffix_completed_data
    redis_manager.redis_db.set(completed_key, 0)
    page_download = 1
    value_key = redis_manager.redis_db.get(key_error_too_many)
    if value_key is not None:
        page_download = int(value_key)
    limit_reached = False

    while redis_manager.redis_db.llen(category) < MAX_ITEM_COUNT_OFFER * MAX_ITEM_PAGE_OFFER:
        try:
            product_lists = []
            products, limit_reached = amazonApiCore.search_products(search_index=category,
                                                                    item_count=MAX_ITEM_COUNT_OFFER,
                                                                    item_page=page_download,
                                                                    min_saving_percent=min_saving_percent,
                                                                    exclude_zero_offers=bool(exclude_zero_offers))
            if len(products) == 0:
                break
            for product in products:
                product_lists.append(product.to_json())

            total_element = total_element + len(product_lists)
            random.shuffle(product_lists)
            redis_manager.redis_db.lpush(category, *product_lists)
            redis_manager.redis_db.expire(category, CATEGORY_REFRESH_TIMEOUT_SECONDS)
            self.update_state(state="PROGRESS",
                              meta=get_meta(page=page_download, total_element=len(product_lists),
                                            category=category))
            page_download += 1

        except MissingParameterAmazonException as e:
            self.update_state(state="FAILURE", meta={"exc_type": type(e).__name__, "exc_message": e.code_message})
            raise MissingParameterAmazonException

        except ItemsNotFoundAmazonException as e:
            self.update_state(state="FAILURE", meta={"exc_type": type(ItemsNotFoundAmazonException).__name__,
                                                     "exc_message": ItemsNotFoundAmazonException.code_message})
            raise ItemsNotFoundAmazonException

        except TooManyRequestAmazonException:
            redis_manager.redis_db.set(key_error_too_many, page_download)
            ttl_category = redis_manager.redis_db.ttl(category)
            ttl_category = CATEGORY_REFRESH_TIMEOUT_SECONDS if ttl_category < 0 else ttl_category
            redis_manager.redis_db.expire(key_error_too_many, ttl_category)
            self.retry(countdown=2)
        else:
            completed_key = category + database_constants.key_suffix_completed_data
            redis_manager.redis_db.set(completed_key, 0)
            ttl_category = redis_manager.redis_db.ttl(category)
            ttl_category = CATEGORY_REFRESH_TIMEOUT_SECONDS if ttl_category < 0 else ttl_category
            redis_manager.redis_db.expire(completed_key, ttl_category)
            redis_manager.redis_db.delete(key_error_too_many)

        if limit_reached:
            break

    redis_manager.redis_db.set(completed_key, 1)
    total_time = start_time - time.perf_counter()

    return get_final_meta(total_time_s=total_time, total_element=total_element, category=category)
