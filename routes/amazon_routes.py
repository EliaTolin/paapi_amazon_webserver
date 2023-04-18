import celery.states
from celery.exceptions import MaxRetriesExceededError
from flask import Blueprint, request, jsonify
from constant.database import database_constants
from core.amazon_api import *
from helper.response_helper import make_response
from models.exceptions.amazon_exception import *
from models.exceptions.redis_exception import *
from models.exceptions.celery_exception import *
import constant.params.amazon_params_constants as amazon_params
import constant.exception.amazon_error_code_message as amazon_error_code_message
import constant.exception.generic_error_code_message as generic_error_code_message
import constant.routes.amazon_routes_constants as amazon_routes
import constant.tasks.tasks_name_constants as tasks_name
import constant.tasks.tasks_params as tasks_params
import core.tasks.amazon_task as amazon_tasks
from singleton.redis_manager import *
from services.celery_services import celery_app
from helper.error_handler import handle_error
import time

amazon_route = Blueprint(amazon_routes.name, __name__, url_prefix=amazon_routes.url_prefix_route)
amazonApiCore = AmazonApiCore()


def is_running_tasked_name(name_task):
    tasks = celery_app.control.inspect()
    active_tasks = tasks.active()
    for workers in active_tasks:
        for t in active_tasks[workers]:
            if t[tasks_params.task_name_params] and t[tasks_params.task_name_params] == name_task:
                return True
    return False


@amazon_route.route(amazon_routes.get_offers_route, methods=['POST'])
def get_category_offers_route():
    try:
        category = request.values.get(amazon_params.categoryParam, default=None)
        item_count = request.values.get(amazon_params.itemCountParam, type=int, default=10)
        item_page = request.values.get(amazon_params.itemPageParam, type=int, default=1)
        min_saving_percent = request.values.get(amazon_params.minSavingPercentParam, type=int) or None
        exclude_zero_offers = request.values.get(amazon_params.excludeZeroOffersParam, type=bool, default=False)
    except ValueError:
        return make_response(status_code=generic_error_code_message.wrong_type_parameter), 400

    if category is None:
        return make_response(status_code=amazon_error_code_message.empty_category), 400

    products_list = []
    try:
        # Get complete key
        completed_key = category + database_constants.key_suffix_completed_data
        # Check if already exist the key
        if redis_manager.redis_db.exists(category):
            if not int(redis_manager.redis_db.get(completed_key)):
                # Get all tasks
                tasks = celery_app.control.inspect()
                # Get only active tasks
                active_tasks = tasks.active()
                for workers in active_tasks:
                    # Get task
                    for t in active_tasks[workers]:
                        # Check our task for the category
                        if t[tasks_params.task_name_params] and \
                                t[tasks_params.task_name_params] == tasks_name.TASK_GET_OFFERS_AMAZON:
                            task = amazon_tasks.get_category_offers.AsyncResult(t['id'])
                            if task is not None and task.info is not None:
                                if task.info[tasks_params.task_category_params] and \
                                        task.info[tasks_params.task_category_params] == category:
                                    while not task.ready():
                                        time.sleep(1)
                                        if task.status == celery.states.FAILURE:
                                            handle_error(task.info, task.id)
                                        # Check if the task is for this category
                                        elif task.info:
                                            if task.info[tasks_params.task_page_params] and \
                                                    task.info[tasks_params.task_page_params] >= item_page:
                                                total_element = redis_manager.redis_db.llen(category)
                                                if total_element and total_element >= item_page * item_count:
                                                    break
                                    if task.status == celery.states.FAILURE:
                                        raise FailureCeleryException
                            else:
                                if task.status == celery.states.FAILURE:
                                    handle_error(task.info, task.id)

        key_error_too_many = category + database_constants.key_suffix_error_too_many
        if not redis_manager.redis_db.exists(category) or redis_manager.redis_db.exists(key_error_too_many):
            arguments = {"item_count": item_count, "item_page": item_page,
                         "exclude_zero_offers": int(exclude_zero_offers)}
            if category:
                arguments["category"] = category
            if min_saving_percent:
                arguments["min_saving_percent"] = min_saving_percent

            task_amazon = amazon_tasks.get_category_offers.apply_async(kwargs=arguments)
            while not task_amazon.ready():
                time.sleep(1)
                # Check if the task is for this category
                if task_amazon.status == celery.states.FAILURE:
                    handle_error(task_amazon.info, task_amazon.id)
                elif task_amazon.info:
                    if task_amazon.info[tasks_params.task_page_params] and \
                            task_amazon.info[tasks_params.task_page_params] >= item_page:
                        if task_amazon.info[tasks_params.task_total_element] and \
                                task_amazon.info[tasks_params.task_total_element] >= item_page * item_count:
                            break

            if task_amazon.status == celery.states.FAILURE:
                raise FailureCeleryException

        index_start = (item_page - 1) * item_count
        index_finish = (item_page * item_count) - 1
        products_list = redis_manager.redis_db.lrange(category, index_start, index_finish)
        if len(products_list) == 0:
            if item_page > 1:
                return make_response(status_code=amazon_error_code_message.limit_reached_products), 204
            return make_response(status_code=amazon_error_code_message.empty_results), 204
        try:
            return make_response(data=products_list), 200

        except ValueError:
            return make_response(status_code=generic_error_code_message.error_convert_json), 500
        except TypeError:
            return make_response(status_code=generic_error_code_message.error_convert_json), 500

    except InvalidArgumentAmazonException as e:
        return make_response(status_code=e.code_message), 400

    except MissingParameterAmazonException as e:
        return make_response(status_code=e.code_message), 400

    except TooManyRequestAmazonException as e:
        return make_response(status_code=e.code_message), 500

    except RedisConnectionException as e:
        return make_response(status_code=e.code_message), 500

    except CategoryNotExistException as e:
        return make_response(status_code=e.code_message), 400

    except FailureCeleryException as e:
        return make_response(status_code=e.code_message), 400

    except ItemsNotFoundAmazonException as e:
        return make_response(status_code=e.code_message), 204


@amazon_route.route(amazon_routes.search_products_route, methods=['POST'])
def search_product_route():
    wordlist = request.values.get(amazon_params.wordlistParam) or None
    if wordlist is None:
        return make_response(status_code=amazon_error_code_message.empty_wordlist), 400

    # Get parameters
    try:
        actor = request.values.get(amazon_params.actorParam, default=None)
        artist = request.values.get(amazon_params.artistParam, default=None)
        author = request.values.get(amazon_params.authorParam, default=None)
        brand = request.values.get(amazon_params.brandParam, default=None)
        title = request.values.get(amazon_params.titleParam, default=None)
        max_price = request.values.get(amazon_params.maxPriceParam, type=int) or None
        min_price = request.values.get(amazon_params.minPriceParam, type=int) or None
        min_saving_percent = request.values.get(amazon_params.minSavingPercentParam, type=int) or None
        min_reviews_rating = request.values.get(amazon_params.minReviewsRatingParam, type=int) or None
        search_index = request.values.get(amazon_params.searchIndexParam, default=None)
        sort = request.values.get(amazon_params.sortParam, default=None)
        item_count = request.values.get(amazon_params.itemCountParam, type=int, default=10)
        item_page = request.values.get(amazon_params.itemPageParam, type=int, default=1) or None
        exclude_zero_price = request.values.get(amazon_params.excludeZeroPriceParam, type=bool, default=False)
        exclude_zero_offers = request.values.get(amazon_params.excludeZeroOffersParam, type=bool, default=False)
        only_prime_delivery = request.values.get(amazon_params.onlyPrimeDeliveryParam, type=bool, default=False)

    except ValueError:
        return make_response(status_code=generic_error_code_message.wrong_type_parameter), 400

    except TypeError:
        return make_response(status_code=generic_error_code_message.wrong_type_parameter), 400

    try:
        list_products, limit_reached = amazonApiCore.search_products(keywords=wordlist, actor=actor, artist=artist,
                                                                     author=author,
                                                                     brand=brand,
                                                                     title=title, max_price=max_price,
                                                                     min_price=min_price,
                                                                     min_saving_percent=min_saving_percent,
                                                                     min_reviews_rating=min_reviews_rating,
                                                                     search_index=search_index, sort=sort,
                                                                     item_page=item_page,
                                                                     item_count=item_count,
                                                                     exclude_zero_price=exclude_zero_price,
                                                                     exclude_zero_offers=exclude_zero_offers,
                                                                     only_prime_delivery=only_prime_delivery)
    except MissingParameterAmazonException as e:
        return make_response(status_code=e.code_message), 400

    except TooManyRequestAmazonException as e:
        return make_response(status_code=e.code_message), 500

    except RedisConnectionException as e:
        return make_response(status_code=e.code_message), 500

    except CategoryNotExistException as e:
        return make_response(status_code=e.code_message), 400

    except ItemsNotFoundAmazonException as e:
        return make_response(status_code=e.code_message), 204

    if len(list_products) == 0:
        if item_page > 1:
            return make_response(status_code=amazon_error_code_message.limit_reached_products), 204
        return make_response(status_code=amazon_error_code_message.empty_results), 204

    try:
        products_json_list = []
        for el in list_products:
            products_json_list.append(el.to_json())
        if limit_reached:
            return make_response(data=products_json_list, status_code=generic_error_code_message.no_error), 206
        return make_response(data=products_json_list, status_code=generic_error_code_message.no_error), 200

    except ValueError:
        return make_response(status_code=generic_error_code_message.error_convert_json), 500

    except TypeError:
        return make_response(status_code=generic_error_code_message.error_convert_json), 500


@amazon_route.route(amazon_routes.get_products_by_asin, methods=['POST'])
def get_products_by_asin():
    list_asins = request.values.getlist(amazon_params.asinProductsParam)
    try:
        list_products = amazonApiCore.get_products_by_asin(asins=list_asins)

    except MissingParameterAmazonException as e:
        return make_response(status_code=e.code_message), 400

    except TooManyRequestAmazonException as e:
        return make_response(status_code=e.code_message), 500

    except RedisConnectionException as e:
        return make_response(status_code=e.code_message), 500

    except CategoryNotExistException as e:
        return make_response(status_code=e.code_message), 400

    except ItemsNotFoundAmazonException as e:
        return make_response(status_code=e.code_message), 204

    if len(list_products) == 0:
        return make_response(status_code=amazon_error_code_message.empty_results), 204

    try:
        products_json_list = []
        for el in list_products:
            products_json_list.append(el.to_json())
        return make_response(data=products_json_list, status_code=generic_error_code_message.no_error), 200

    except ValueError:
        return make_response(status_code=generic_error_code_message.error_convert_json), 500

    except TypeError:
        return make_response(status_code=generic_error_code_message.error_convert_json), 500


@amazon_route.route(amazon_routes.add_category_preference, methods=['POST'])
def add_category_preference():
    list_search_category = request.values.getlist(amazon_params.listCategoryPreferenceParam)

    if list_search_category is None:
        return make_response(status_code=generic_error_code_message.no_error), 200

    for category in list_search_category:
        redis_manager.redis_db.incr(category + database_constants.key_suffix_preference)
    return make_response(status_code=generic_error_code_message.no_error), 200
